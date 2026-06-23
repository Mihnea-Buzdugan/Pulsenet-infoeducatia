"""
Usage:
    python manage.py generate_embeddings                      # all models
    python manage.py generate_embeddings --model pulse        # specific model
    python manage.py generate_embeddings --batch-size 64      # custom batch size
    python manage.py generate_embeddings --overwrite          # re-embed existing
"""

from django.core.management.base import BaseCommand
from apps.accounts.models import (
    Pulse, Alert, UrgentRequest,
    PulseFeedback, PulseComment,
    Contact, User
)

# Adjust this import to wherever embedding_model lives
from apps.accounts.utils import embedding_model


# ── Text builders — mirrors your signals exactly ──────────────────────────────

def _user_snippet(u: User) -> str:
    """Reusable inline user detail string for FK references."""
    first = u.first_name or ""
    last  = u.last_name  or ""
    return (
        f"{u.username} ({first} {last}, {u.email})"
    )


def _text_for_user(u: User) -> str:
    first = u.first_name or ""
    last  = u.last_name  or ""
    bio   = u.biography  or ""
    return (
        f"User: {u.username}. Name: {first} {last}. "
        f"Email: {u.email}. Bio: {bio}. Skills: {u.get_skills_text()}"
    )


def _text_for_pulse(p: Pulse) -> str:
    desc = p.description or ""
    addr = p.address     or ""
    return (
        f"User: {_user_snippet(p.user)}. Title: {p.title}. Description: {desc}. "
        f"Category: {p.category}. Price: {p.price}. "
        f"Type: {p.get_pulse_type_display()}. Address: {addr}."
    )


def _text_for_alert(a: Alert) -> str:
    desc = a.description or ""
    addr = a.address     or ""
    return (
        f"User: {_user_snippet(a.user)}. Alert: {a.title}. Description: {desc}. "
        f"Category: {a.get_category_display()}. Address: {addr}."
    )


def _text_for_urgent_request(r: UrgentRequest) -> str:
    desc  = r.description or ""
    addr  = r.address     or ""
    price = r.max_price   or 0
    return (
        f"User: {_user_snippet(r.user)}. Urgent Request: {r.title}. Description: {desc}. "
        f"Price: {price}. Category: {r.category}. Address: {addr}."
    )


def _text_for_contact(c: Contact) -> str:
    return (
        f"Complaint/Message: {c.complaint_message}. "
        f"User: {_user_snippet(c.user)}"
    )


def _text_for_pulse_comment(c: PulseComment) -> str:
    return c.content


def _text_for_pulse_feedback(f: PulseFeedback) -> str:
    return str(f.comment)


# ── Registry ──────────────────────────────────────────────────────────────────
# key → (Model, text_fn, select_related_fields)

MODEL_REGISTRY = {
    "user":          (User,           _text_for_user,            []),
    "pulse":         (Pulse,          _text_for_pulse,           ["user"]),
    "alert":         (Alert,          _text_for_alert,           ["user"]),
    "urgentrequest": (UrgentRequest,  _text_for_urgent_request,  ["user"]),
    "contact":       (Contact,        _text_for_contact,         ["user"]),
    "pulsecomment":  (PulseComment,   _text_for_pulse_comment,   []),
    "pulsefeedback": (PulseFeedback,  _text_for_pulse_feedback,  []),
}


# ── Core embed function ───────────────────────────────────────────────────────

def embed_queryset(model_key, overwrite=False, batch_size=32, stdout=None):
    """
    Generate and save ai_embedding for all instances of one model.
    Uses the exact same text format as the post_save signals.
    Returns (updated_count, skipped_count).
    """
    Model, text_fn, related = MODEL_REGISTRY[model_key]

    qs = Model.objects.all()
    if related:
        qs = qs.select_related(*related)
    if not overwrite:
        qs = qs.filter(ai_embedding__isnull=True)

    total = qs.count()
    if stdout:
        stdout.write(f"  {Model.__name__}: {total} objects to embed")

    if total == 0:
        if stdout:
            stdout.write(f"  ✓ {Model.__name__}: nothing to do\n")
        return 0, 0

    updated = 0
    skipped = 0
    ids = list(qs.values_list("pk", flat=True))

    for batch_start in range(0, len(ids), batch_size):
        batch_ids = ids[batch_start : batch_start + batch_size]
        batch_qs  = Model.objects.filter(pk__in=batch_ids)
        if related:
            batch_qs = batch_qs.select_related(*related)

        objects_to_update = []
        texts             = []

        for obj in batch_qs:
            try:
                text = text_fn(obj)
                # Same guard as generate_and_save_embedding — skip empty/None
                if not text or str(text).strip().lower() in ("", "none"):
                    skipped += 1
                    continue
            except Exception as exc:
                if stdout:
                    stdout.write(f"\n    ⚠ Skipping {Model.__name__} pk={obj.pk}: {exc}")
                skipped += 1
                continue

            texts.append(text)
            objects_to_update.append(obj)

        if not texts:
            continue

        # Batch-encode is much faster than one-by-one
        vectors = embedding_model.encode(texts, show_progress_bar=False)

        for obj, vector in zip(objects_to_update, vectors):
            obj.ai_embedding = vector.tolist()

        Model.objects.bulk_update(objects_to_update, ["ai_embedding"])
        updated += len(objects_to_update)

        if stdout:
            done = min(batch_start + batch_size, total)
            stdout.write(f"    → {done}/{total}", ending="\r")

    if stdout:
        stdout.write(f"\n  ✓ {Model.__name__}: {updated} updated, {skipped} skipped\n")

    return updated, skipped


# ── Management command ────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = "Backfill ai_embedding for all embeddable models (mirrors post_save signals)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--model",
            type=str,
            default="all",
            choices=["all"] + list(MODEL_REGISTRY.keys()),
            help="Which model to embed (default: all)",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=32,
            help="Objects per encoding batch (default: 32)",
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            default=False,
            help="Re-embed objects that already have an embedding",
        )

    def handle(self, *args, **options):
        model_arg  = options["model"]
        batch_size = options["batch_size"]
        overwrite  = options["overwrite"]

        targets = list(MODEL_REGISTRY.keys()) if model_arg == "all" else [model_arg]

        self.stdout.write(self.style.SUCCESS(
            f"\n🔧 Embedding: {', '.join(targets)}"
            f" | batch={batch_size} | overwrite={overwrite}\n"
        ))

        total_updated = 0
        total_skipped = 0

        for key in targets:
            updated, skipped = embed_queryset(
                key,
                overwrite=overwrite,
                batch_size=batch_size,
                stdout=self.stdout,
            )
            total_updated += updated
            total_skipped += skipped

        self.stdout.write(self.style.SUCCESS(
            f"✅ Done — updated: {total_updated} | skipped: {total_skipped}\n"
        ))
from functools import lru_cache
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from sentence_transformers import SentenceTransformer
from .models import (
    User, Pulse, PulseFeedback, PulseComment,
    Alert, AlertComment, UrgentRequest, UrgentRequestFeedback, Contact
)

# ---------------------------------------------------------
# WebSocket Broadcast Deletion Signals
# ---------------------------------------------------------

@receiver(post_delete, sender=Pulse)
def broadcast_pulse_deletion(sender, instance, **kwargs):
    """
    Broadcasts a WebSocket message whenever a Pulse is deleted
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "pulses_feed",
        {
            "type": "pulse.deleted",
            "id": instance.id
        }
    )


@receiver(post_delete, sender=UrgentRequest)
def broadcast_request_deletion(sender, instance, **kwargs):
    """
    Broadcasts a WebSocket message whenever an Urgent Request is deleted
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "requests_feed",
        {
            "type": "request.deleted",
            "id": instance.id
        }
    )

@receiver(post_delete, sender=Alert)
def broadcast_alert_deletion(sender, instance, **kwargs):  # Fixed duplicate name typo
    """
    Broadcasts a WebSocket message whenever an Alert is deleted
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "alerts_feed",
        {
            "type": "alert.deleted",
            "id": instance.id
        }
    )

# ---------------------------------------------------------
# AI Embedding Generation Signals (Optimized with Lazy Loading)
# ---------------------------------------------------------

@lru_cache(maxsize=1)
def get_embedding_model():
    """
    Loads and caches the AI model on-demand.
    It will NEVER run during standard Django commands like 'makemigrations'.
    """
    return SentenceTransformer('sentence-transformers/all-mpnet-base-v2')


def generate_and_save_embedding(instance, text_to_embed, model_class):
    """Utility function to generate vector and update the database row."""
    if text_to_embed and text_to_embed.strip():
        # Loads the model the first time it's called, then reuses it
        model = get_embedding_model()
        # Generate the 768-dimension vector
        vector = model.encode(text_to_embed).tolist()
        # Use .update() instead of .save() to avoid infinite signal loops
        model_class.objects.filter(id=instance.id).update(ai_embedding=vector)


@receiver(post_save, sender=User)
def embed_user(sender, instance, **kwargs):
    # Safely handle potential None values
    first = instance.first_name or ""
    last = instance.last_name or ""
    bio = instance.biography or ""
    text = f"User: {first} {last}. Bio: {bio}. Skills: {instance.get_skills_text()}"
    generate_and_save_embedding(instance, text, User)

@receiver(post_save, sender=Pulse)
def embed_pulse(sender, instance, **kwargs):
    desc = instance.description or ""
    addr = instance.address or ""
    text = f"User: {instance.user}. Title: {instance.title}. Description: {desc}. Category: {instance.category}. Price: {instance.price}. Type: {instance.get_pulse_type_display()}. Address: {addr}."
    generate_and_save_embedding(instance, text, Pulse)

@receiver(post_save, sender=Alert)
def embed_alert(sender, instance, **kwargs):
    desc = instance.description or ""
    addr = instance.address or ""
    text = f"User: {instance.user}. Alert: {instance.title}. Description: {desc}. Category: {instance.get_category_display()}. Address: {addr}."
    generate_and_save_embedding(instance, text, Alert)

@receiver(post_save, sender=UrgentRequest)
def embed_urgent_request(sender, instance, **kwargs):
    desc = instance.description or ""
    addr = instance.address or ""
    price = instance.max_price or 0
    text = f"Urgent Request: {instance.title}. Description: {desc}. Price: {price}. Category: {instance.category}. Address: {addr}."
    generate_and_save_embedding(instance, text, UrgentRequest)


@receiver(post_save, sender=Contact)
def embed_contact(sender, instance, **kwargs):
    text = f"Complaint/Message: {instance.complaint_message}. User: {instance.user}"
    generate_and_save_embedding(instance, text, Contact)


@receiver(post_save, sender=PulseComment)
def embed_pulse_comment(sender, instance, **kwargs):
    generate_and_save_embedding(instance, instance.content, PulseComment)


@receiver(post_save, sender=PulseFeedback)
def embed_pulse_feedback(sender, instance, **kwargs):
    generate_and_save_embedding(instance, str(instance.comment), PulseFeedback)
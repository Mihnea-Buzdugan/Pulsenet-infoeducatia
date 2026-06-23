from django.contrib.gis.geos import Point
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from apps.accounts.models import UrgentRequest, User



requests_data = [
    {
        "user_id": 1,
        "title": "Need plumber urgently",
        "description": "Pipe burst in kitchen, need immediate repair.",
        "category": "Plumbing",
        "max_price": Decimal("250.00"),
        "location": Point(27.6014, 47.1585),
        "address": "Strada Palat 1, Iasi",
        "expires_in_hours": 48,
    },
    {
        "user_id": 2,
        "title": "Emergency electrician needed",
        "description": "Power outage in apartment.",
        "category": "Electrical",
        "max_price": Decimal("400.00"),
        "location": Point(27.5879, 47.1739),
        "address": "Bulevardul Stefan cel Mare, Iasi",
        "expires_in_hours": 24,
    },
    {
        "user_id": 3,
        "title": "Need moving help today",
        "description": "Need 2 people to move furniture.",
        "category": "Moving",
        "max_price": Decimal("300.00"),
        "location": Point(27.5700, 47.1600),
        "address": "Tatarasi, Iasi",
        "expires_in_hours": 72,
    },
    {
        "user_id": 4,
        "title": "Urgent babysitter required",
        "description": "Need babysitter for tonight.",
        "category": "Childcare",
        "max_price": Decimal("200.00"),
        "location": Point(27.6100, 47.1650),
        "address": "Copou, Iasi",
        "expires_in_hours": 12,
    },
    {
        "user_id": 5,
        "title": "Dog walker needed",
        "description": "Need someone to walk my dog this evening.",
        "category": "Pets",
        "max_price": Decimal("80.00"),
        "location": Point(27.5950, 47.1500),
        "address": "Nicolina, Iasi",
        "expires_in_hours": 8,
    },
    {
        "user_id": 6,
        "title": "Need car towing service",
        "description": "Car broke down near city center.",
        "category": "Automotive",
        "max_price": Decimal("500.00"),
        "location": Point(27.5800, 47.1670),
        "address": "Piata Unirii, Iasi",
        "expires_in_hours": 6,
    },
    {
        "user_id": 7,
        "title": "Laptop repair ASAP",
        "description": "Laptop not turning on before presentation.",
        "category": "Tech Repair",
        "max_price": Decimal("350.00"),
        "location": Point(27.6200, 47.1700),
        "address": "Campus Tudor Vladimirescu, Iasi",
        "expires_in_hours": 24,
    },
    {
        "user_id": 8,
        "title": "House cleaning needed",
        "description": "Need urgent apartment cleaning.",
        "category": "Cleaning",
        "max_price": Decimal("180.00"),
        "location": Point(27.6000, 47.1550),
        "address": "Podu Ros, Iasi",
        "expires_in_hours": 48,
    },
    {
        "user_id": 9,
        "title": "Need translator urgently",
        "description": "Romanian-English translation for documents.",
        "category": "Translation",
        "max_price": Decimal("220.00"),
        "location": Point(27.5900, 47.1620),
        "address": "Centru, Iasi",
        "expires_in_hours": 120,
    },
    {
        "user_id": 10,
        "title": "Need private driver",
        "description": "Airport pickup required tonight.",
        "category": "Transport",
        "max_price": Decimal("150.00"),
        "location": Point(27.6400, 47.1780),
        "address": "Iasi Airport",
        "expires_in_hours": 10,
    },
    {
        "user_id": 11,
        "title": "Urgent painter needed",
        "description": "Need room painted before event.",
        "category": "Painting",
        "max_price": Decimal("600.00"),
        "location": Point(27.6050, 47.1720),
        "address": "Pacurari, Iasi",
        "expires_in_hours": 96,
    },
    {
        "user_id": 12,
        "title": "Need event photographer",
        "description": "Photographer needed for birthday party.",
        "category": "Photography",
        "max_price": Decimal("700.00"),
        "location": Point(27.6150, 47.1680),
        "address": "Alexandru cel Bun, Iasi",
        "expires_in_hours": 48,
    },
    {
        "user_id": 13,
        "title": "Urgent AC repair",
        "description": "Air conditioner leaking water.",
        "category": "HVAC",
        "max_price": Decimal("450.00"),
        "location": Point(27.5750, 47.1580),
        "address": "Frumoasa, Iasi",
        "expires_in_hours": 24,
    },
    {
        "user_id": 14,
        "title": "Need gardener urgently",
        "description": "Garden cleanup needed before weekend.",
        "category": "Gardening",
        "max_price": Decimal("300.00"),
        "location": Point(27.6250, 47.1800),
        "address": "Bucium, Iasi",
        "expires_in_hours": 72,
    },
    {
        "user_id": 15,
        "title": "Need locksmith now",
        "description": "Locked out of apartment.",
        "category": "Locksmith",
        "max_price": Decimal("200.00"),
        "location": Point(27.5980, 47.1660),
        "address": "Gara, Iasi",
        "expires_in_hours": 4,
    },
]


created_requests = []

for data in requests_data:
    try:
        user = User.objects.get(id=data["user_id"])

        req = UrgentRequest.objects.create(
            user=user,
            title=data["title"],
            description=data["description"],
            is_approved=True,
            is_flagged=False,
            toxicity_score=0.0,
            trust_required=False,
            category=data["category"],
            max_price=data["max_price"],
            currencyType="RON",
            location=data["location"],
            address=data["address"],
            is_active=True,
            expires_at=timezone.now() + timedelta(hours=data["expires_in_hours"]),
        )

        created_requests.append(req)
        print(f"Created: {req.title}")

    except User.DoesNotExist:
        print(f"User with ID {data['user_id']} does not exist")


print(f"\nSuccessfully created {len(created_requests)} urgent requests.")
#!/usr/bin/python3

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from datetime import datetime
import uuid
import sys
sys.path.insert(0, '/root/Holberton/holbertonschool-hbnb/part4/hbnb')


app = create_app()

with app.app_context():
    # Debug: Check all users
    all_users = User.query.all()
    print(f"Total users in DB: {len(all_users)}")
    for u in all_users:
        print(f"  - {u.email}")

    # Récupérer user2
    user2 = User.query.filter_by(_email='user2@user.com').first()

    if not user2:
        print("❌ User2 non trouvé!")
        sys.exit(1)

    print(f"✅ Trouvé: {user2.first_name} {user2.last_name} (ID: {user2.id})")

    # Créer 10 places
    places_data = [
        {
            "title": "Cozy Studio in Paris Center",
            "description": "Beautiful studio with a great view of the Eiffel Tower",
            "number_rooms": 1,
            "number_bathrooms": 1,
            "max_guest": 2,
            "price_by_night": 85.0,
            "latitude": 48.8566,
            "longitude": 2.3522
        },
        {
            "title": "Luxury Apartment Marais",
            "description": "Modern luxury apartment in the heart of Paris Marais district",
            "number_rooms": 2,
            "number_bathrooms": 2,
            "max_guest": 4,
            "price_by_night": 150.0,
            "latitude": 48.8606,
            "longitude": 2.3626
        },
        {
            "title": "Charming House Montmartre",
            "description": "Traditional Parisian house with classic charm near Sacré-Cœur",
            "number_rooms": 3,
            "number_bathrooms": 2,
            "max_guest": 6,
            "price_by_night": 120.0,
            "latitude": 48.8867,
            "longitude": 2.3431
        },
        {
            "title": "Modern Loft Left Bank",
            "description": "Spacious loft with exposed beams and artistic touches",
            "number_rooms": 2,
            "number_bathrooms": 1,
            "max_guest": 4,
            "price_by_night": 130.0,
            "latitude": 48.8419,
            "longitude": 2.3430
        },
        {
            "title": "Rustic Villa Provence",
            "description": "Traditional Provençal villa with garden and outdoor kitchen",
            "number_rooms": 4,
            "number_bathrooms": 3,
            "max_guest": 8,
            "price_by_night": 200.0,
            "latitude": 43.9494,
            "longitude": 4.8055
        },
        {
            "title": "Seaside Cottage Côte d'Azur",
            "description": "Beachfront cottage with direct access to the Mediterranean",
            "number_rooms": 2,
            "number_bathrooms": 2,
            "max_guest": 4,
            "price_by_night": 180.0,
            "latitude": 43.5890,
            "longitude": 7.0760
        },
        {
            "title": "Penthouse with City View",
            "description": "Ultra-modern penthouse with panoramic views of the city",
            "number_rooms": 3,
            "number_bathrooms": 2,
            "max_guest": 6,
            "price_by_night": 250.0,
            "latitude": 48.8593,
            "longitude": 2.2975
        },
        {
            "title": "Cozy Parisian Studio",
            "description": "Intimate studio perfect for couples visiting Paris",
            "number_rooms": 1,
            "number_bathrooms": 1,
            "max_guest": 2,
            "price_by_night": 75.0,
            "latitude": 48.8529,
            "longitude": 2.3499
        },
        {
            "title": "Family Home with Pool",
            "description": "Spacious family home with swimming pool and gardens",
            "number_rooms": 5,
            "number_bathrooms": 3,
            "max_guest": 10,
            "price_by_night": 220.0,
            "latitude": 48.8342,
            "longitude": 2.3856
        },
        {
            "title": "Boutique Hotel Room",
            "description": "Elegant room in a boutique hotel with all amenities",
            "number_rooms": 1,
            "number_bathrooms": 1,
            "max_guest": 2,
            "price_by_night": 110.0,
            "latitude": 48.8699,
            "longitude": 2.3506
        }
    ]

    # Insérer les places
    for i, place_data in enumerate(places_data, 1):
        place = Place(
            title=place_data["title"],
            description=place_data["description"],
            price=place_data["price_by_night"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=user2
        )
        db.session.add(place)
        print(f"✅ Place {i}: {place_data['title']}")

    db.session.commit()
    print(f"\n✨ {len(places_data)} places créées pour {user2.first_name}!")

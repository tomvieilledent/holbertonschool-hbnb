# HBnB — Partie 2 (API REST Flask)

API REST de la plateforme **HBnB** développée avec **Flask** et **Flask-RESTX**.
Cette partie implémente les ressources principales : **Users, Amenities, Places, Reviews**,
avec validation métier, architecture en couches et tests d'endpoints.

---

## Sommaire

- [Objectif](#objectif)
- [Stack technique](#stack-technique)
- [Architecture du projet](#architecture-du-projet)
- [Installation](#installation)
- [Lancer l'application](#lancer-lapplication)
- [Documentation Swagger](#documentation-swagger)
- [Endpoints API](#endpoints-api)
- [Règles de validation](#règles-de-validation)
- [Exemples `curl`](#exemples-curl)
- [Exécuter les tests](#exécuter-les-tests)
- [Limites actuelles](#limites-actuelles)
- [Auteurs](#auteurs)

---

## Objectif

Fournir une API HTTP claire et testable pour gérer :

- les utilisateurs,
- les commodités,
- les logements,
- les avis,

en respectant des validations strictes (formats, bornes, références entre entités).

---

## Stack technique

- **Python 3**
- **Flask**
- **Flask-RESTX** (routing + Swagger)
- **jsonschema**
- **email-validator**
- Persistance en mémoire via `InMemoryRepository`

---

## Architecture du projet

```text
hbnb/
├── app/
│   ├── api/v1/              # Endpoints REST (users, amenities, places, reviews)
│   ├── models/              # Entités métier + validations
│   ├── persistence/         # Repository pattern (in-memory)
│   └── services/            # Facade (logique applicative)
├── config.py
├── run.py                   # Point d'entrée Flask
├── requirements.txt
└── test_endpoints.py        # Tests d'API
```

### Flux global

`Route API` → `Facade` → `Repository` → `Models`

- Les routes appellent la facade.
- La facade orchestre les entités et vérifie les relations.
- Le repository stocke les objets en mémoire.
- Les modèles appliquent les validations de données.

---

## Installation

Depuis le dossier `hbnb` :

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Lancer l'application

```bash
python3 run.py
```

Par défaut, Flask démarre en mode debug sur :

`http://127.0.0.1:5000`

---

## Documentation Swagger

Interface interactive disponible à la racine :

`http://127.0.0.1:5000/`

---

## Endpoints API

Base URL : `http://127.0.0.1:5000/api/v1`

### Users

- `POST /users/` : créer un utilisateur
- `GET /users/` : lister les utilisateurs
- `GET /users/<user_id>` : récupérer un utilisateur
- `PUT /users/<user_id>` : mettre à jour un utilisateur

### Amenities

- `POST /amenities/` : créer une commodité
- `GET /amenities/` : lister les commodités
- `GET /amenities/<amenity_id>` : récupérer une commodité
- `PUT /amenities/<amenity_id>` : mettre à jour une commodité

### Places

- `POST /places/` : créer un logement
- `GET /places/` : lister les logements
- `GET /places/<place_id>` : détail d'un logement (owner, amenities, reviews)
- `PUT /places/<place_id>` : mettre à jour un logement
- `GET /places/<place_id>/reviews` : lister les avis d'un logement

### Reviews

- `POST /reviews/` : créer un avis
- `GET /reviews/` : lister les avis
- `GET /reviews/<review_id>` : récupérer un avis
- `PUT /reviews/<review_id>` : mettre à jour un avis
- `DELETE /reviews/<review_id>` : supprimer un avis

---

## Règles de validation

### User

- `first_name` : string non vide, max 50 caractères
- `last_name` : string non vide, max 50 caractères
- `email` : string non vide, format email valide
- `email` unique dans le système

### Amenity

- `name` : string non vide, max 50 caractères

### Place

- `title` : string non vide, max 100 caractères
- `description` : `None` ou string non vide
- `price` : nombre `>= 0`
- `latitude` : nombre dans `[-90, 90]`
- `longitude` : nombre dans `[-180, 180]`
- `owner_id` : doit référencer un user existant
- `amenities` : liste d'IDs de commodités existantes

### Review

- `text` : string non vide
- `rating` : entier entre 1 et 5
- `user_id` : user existant
- `place_id` : place existante

---

## Exemples `curl`

### 1) Créer un user

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
	-H "Content-Type: application/json" \
	-d '{
		"first_name": "Alice",
		"last_name": "Martin",
		"email": "alice.martin@example.com"
	}'
```

### 2) Créer une amenity

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
	-H "Content-Type: application/json" \
	-d '{"name": "WiFi"}'
```

### 3) Créer une place

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
	-H "Content-Type: application/json" \
	-d '{
		"title": "Studio centre-ville",
		"description": "Calme et lumineux",
		"price": 79.9,
		"latitude": 48.8566,
		"longitude": 2.3522,
		"owner_id": "<USER_ID>",
		"amenities": ["<AMENITY_ID>"]
	}'
```

### 4) Créer une review

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
	-H "Content-Type: application/json" \
	-d '{
		"text": "Super séjour",
		"rating": 5,
		"user_id": "<USER_ID>",
		"place_id": "<PLACE_ID>"
	}'
```

---

## Exécuter les tests

Depuis le dossier `hbnb` :

```bash
python3 -m unittest -v test_endpoints.py
```

Le fichier de tests couvre les cas principaux :

- créations valides,
- champs obligatoires manquants,
- formats invalides,
- mises à jour,
- cas `404` (ressource absente),
- intégrité des relations entre entités.

---

## Limites actuelles

- Persistance **en mémoire** uniquement (pas de base de données).
- Les données sont perdues à chaque redémarrage du serveur.
- Authentification/autorisation non implémentée dans cette partie.

---

## Auteurs

Florian Roosebeke
Tom Vieilledent

### créer un admin ###
source venv/bin/activate
python3 - <<'PY'
from app import create_app, db
from app.services import facade

app = create_app()

with app.app_context():
    email = "admin@example.com"
    user = facade.get_user_by_email(email)

    if user:
        user.is_admin = True
        db.session.commit()
        print("Utilisateur existant promu admin:", email)
    else:
        user = facade.create_user({
            "first_name": "Super",
            "last_name": "Admin",
            "email": email,
            "password": "Admin1234!",
            "is_admin": True
        })
        print("Admin cree:", user.id, email)
PY
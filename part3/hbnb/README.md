# HBnB - Part 3 (API Flask, JWT Bearer, Swagger)

API REST de la plateforme HBnB avec architecture en couches, persistance SQLAlchemy,
authentification JWT Bearer, gestion des permissions (admin/user), et tests automatisés avec pytest.

## Sommaire

- Objectif
- Stack technique
- Architecture du projet
- Documentation technique (partie 1 mise a jour)
- Installation
- Lancer l'application
- Documentation Swagger
- Authentification JWT Bearer
- Endpoints API
- Regles de validation metier
- Exemples curl
- Executer les tests
- Pytest Summary (Last Run)
- Limites actuelles
- Auteurs

## Objectif

Fournir une API HTTP claire, securisee et testable pour gerer:

- les utilisateurs
- les commodites
- les logements
- les avis

avec des validations strictes, des droits d'acces selon le role, et une authentification par token JWT.

## Stack technique

- Python 3
- Flask
- Flask-RESTX (routing + Swagger)
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-JWT-Extended
- email-validator
- pytest

## Architecture du projet

```text
hbnb/
├── app/
│   ├── api/v1/              # Endpoints (auth, users, amenities, places, reviews)
│   ├── models/              # Entites metier + validations
│   ├── persistence/         # Repositories SQLAlchemy
│   └── services/            # Facade (regles applicatives)
├── config.py
├── run.py
├── requirements.txt
├── pytest.ini
└── tests/
    ├── conftest.py
    ├── helpers.py
    ├── test_auth.py
    ├── test_users.py
    ├── test_amenities.py
    ├── test_places.py
    └── test_reviews.py
```

Flux global:

`Route API -> Facade -> Repository -> SQLAlchemy/DB`

## Documentation technique (partie 1 mise a jour)

Cette section reprend la logique documentaire de la partie 1, mise a jour pour le code actuel.

### 1. Architecture 3 couches

- Couche Presentation (API Flask-RESTX): recoit les requetes HTTP, valide les payloads RESTX, renvoie JSON.
- Couche Logique metier (Facade + models): applique les regles metier, controle les relations entre entites.
- Couche Persistance (repositories SQLAlchemy): gere CRUD et sessions DB.

### 2. Pattern Facade

`HBnBFacade` centralise les operations metier:

- Users: create/get/update/list, recherche par email
- Amenities: create/get/update/delete/list
- Places: create/get/update/delete/list + resolution owner/amenities
- Reviews: create/get/update/delete/list + recherche par place

### 3. Entites et relations

- BaseModel: `id`, `created_at`, `updated_at`
- User: first_name, last_name, email unique, password hash, is_admin
- Place: title, description, price, latitude, longitude, owner
- Amenity: name
- Review: text, rating, user, place

Relations principales:

- User 1..n Place
- User 1..n Review
- Place 1..n Review
- Place n..n Amenity

### 4. Regles metier clefs (mises a jour part3)

- JWT requis sur routes protegees
- Admin requis pour creer users (API), creer/modifier/supprimer amenities
- Un user normal ne peut modifier que ses propres ressources authorisees
- `PUT /users/<id>`: un user non admin ne peut pas modifier email/password/is_admin
- `POST /reviews`: interdit sur son propre logement
- `POST /reviews`: un seul avis par user et par place

### 5. Flux API metier (version part3)

- Login:
  - recherche user par email
  - verification du mot de passe hash
  - emission d'un `access_token` JWT avec claim `is_admin`
- Creation place:
  - owner force depuis l'identite JWT
  - validation des donnees (prix/coordonnees/amenities)
- Soumission review:
  - verification place existante
  - refus si owner = auteur
  - refus si review deja existante pour ce user/place

## Installation

Depuis le dossier `hbnb`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-cov
```

## Lancer l'application

```bash
source .venv/bin/activate
python3 run.py
```

URLs par defaut:

- API base: `http://127.0.0.1:5000/api/v1`
- Swagger UI: `http://127.0.0.1:5000/`

## Documentation Swagger

Interface disponible a la racine:

`http://127.0.0.1:5000/`

## Authentification JWT Bearer

Header requis sur routes protegees:

`Authorization: Bearer <token>`

### Creer ou promouvoir un compte admin

```bash
source .venv/bin/activate
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
            "password": "admin",
            "is_admin": True
        })
        print("Admin cree:", user.id, email)
PY
```

### Se connecter et recuperer le token

```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin"}'
```

Reponse attendue:

```json
{
  "access_token": "<jwt_token>"
}
```

### Utiliser le token dans Swagger

1. Ouvrir Swagger
2. Cliquer sur Authorize
3. Coller exactement: `Bearer <token>`
4. Valider puis tester les routes protegees

## Endpoints API

Base URL: `http://127.0.0.1:5000/api/v1`

### Auth

- `POST /auth/login`
- `GET /auth/protected`

### Users

- `POST /users/` (admin only)
- `GET /users/` (public)
- `GET /users/<user_id>` (public)
- `PUT /users/<user_id>` (owner or admin)

### Amenities

- `POST /amenities/` (admin only)
- `GET /amenities/` (public)
- `GET /amenities/<amenity_id>` (public)
- `PUT /amenities/<amenity_id>` (admin only)
- `DELETE /amenities/<amenity_id>` (admin only)

### Places

- `POST /places/` (auth)
- `GET /places/` (public)
- `GET /places/<place_id>` (public)
- `PUT /places/<place_id>` (owner or admin)
- `DELETE /places/<place_id>` (owner or admin)
- `GET /places/<place_id>/reviews` (public)

### Reviews

- `POST /reviews/` (auth)
- `GET /reviews/` (public)
- `GET /reviews/<review_id>` (public)
- `PUT /reviews/<review_id>` (owner or admin)
- `DELETE /reviews/<review_id>` (owner or admin)

## Regles de validation metier

### User

- `first_name`: string non vide, max 50
- `last_name`: string non vide, max 50
- `email`: format valide, unique
- `password`: stocke hash

### Amenity

- `name`: string non vide, max 50

### Place

- `title`: string non vide, max 100
- `description`: string non vide, max 2000
- `price`: nombre strictement positif
- `latitude`: [-90, 90]
- `longitude`: [-180, 180]
- `owner_id`: derive du JWT (pas du payload client)
- `amenities`: ids existants uniquement

### Review

- `text`: string (max 2000)
- `rating`: entier de 1 a 5
- `place_id`: doit exister
- refus si owner du place
- refus si review deja postee par ce user sur cette place

## Exemples curl

### Login admin

```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin"}'
```

### Creer une amenity (admin)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"WiFi"}'
```

### Creer une place (user connecte)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title":"Studio centre-ville",
    "description":"Calme et lumineux",
    "price":79.9,
    "latitude":48.8566,
    "longitude":2.3522,
    "amenities":[]
  }'
```

### Creer une review

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"text":"Super sejour","rating":5,"place_id":"<PLACE_ID>"}'
```

## Executer les tests

Depuis `hbnb`:

```bash
source .venv/bin/activate
pytest
```

Commandes utiles:

```bash
pytest -v -rA
pytest -q -rA
pytest tests/test_auth.py
pytest --cov=app --cov-report=term-missing
```

## Pytest Summary (Last Run)

- 42 passed

Liste (une ligne par test):

- PASSED tests/test_amenities.py::test_amenities_get_list_public_returns_200
- PASSED tests/test_amenities.py::test_amenities_post_requires_auth_returns_401
- PASSED tests/test_amenities.py::test_amenities_post_non_admin_returns_403
- PASSED tests/test_amenities.py::test_amenities_post_admin_creates
- PASSED tests/test_amenities.py::test_amenities_post_invalid_payload_returns_400
- PASSED tests/test_amenities.py::test_amenities_get_one_unknown_returns_404
- PASSED tests/test_amenities.py::test_amenities_put_admin_updates
- PASSED tests/test_amenities.py::test_amenities_put_non_admin_returns_403
- PASSED tests/test_amenities.py::test_amenities_delete_admin_returns_200
- PASSED tests/test_amenities.py::test_amenities_delete_not_found_returns_404
- PASSED tests/test_auth.py::test_login_success_returns_access_token
- PASSED tests/test_auth.py::test_login_bad_credentials_returns_401
- PASSED tests/test_auth.py::test_protected_requires_jwt_returns_401
- PASSED tests/test_auth.py::test_protected_with_token_returns_200
- PASSED tests/test_places.py::test_places_get_list_public_returns_200
- PASSED tests/test_places.py::test_places_post_requires_auth_returns_401
- PASSED tests/test_places.py::test_places_post_user_creates_place
- PASSED tests/test_places.py::test_places_post_invalid_payload_returns_400
- PASSED tests/test_places.py::test_places_get_one_unknown_returns_404
- PASSED tests/test_places.py::test_places_put_non_owner_returns_403
- PASSED tests/test_places.py::test_places_put_owner_updates
- PASSED tests/test_places.py::test_places_delete_non_owner_returns_403
- PASSED tests/test_places.py::test_places_delete_owner_returns_200
- PASSED tests/test_places.py::test_places_reviews_unknown_place_returns_404
- PASSED tests/test_reviews.py::test_reviews_get_list_public_returns_200
- PASSED tests/test_reviews.py::test_reviews_post_requires_auth_returns_401
- PASSED tests/test_reviews.py::test_reviews_post_invalid_payload_returns_400
- PASSED tests/test_reviews.py::test_reviews_post_place_not_found_returns_404
- PASSED tests/test_reviews.py::test_reviews_owner_cannot_review_own_place_returns_400
- PASSED tests/test_reviews.py::test_reviews_user_can_create_review
- PASSED tests/test_reviews.py::test_reviews_put_non_owner_returns_403
- PASSED tests/test_reviews.py::test_reviews_delete_owner_returns_200
- PASSED tests/test_reviews.py::test_reviews_get_unknown_returns_404
- PASSED tests/test_users.py::test_users_get_list_is_public
- PASSED tests/test_users.py::test_users_post_requires_auth_returns_401
- PASSED tests/test_users.py::test_users_post_non_admin_returns_403
- PASSED tests/test_users.py::test_users_post_admin_creates_user
- PASSED tests/test_users.py::test_users_post_invalid_payload_returns_400
- PASSED tests/test_users.py::test_users_get_one_returns_404_for_unknown
- PASSED tests/test_users.py::test_users_put_non_owner_non_admin_returns_403
- PASSED tests/test_users.py::test_users_put_owner_cannot_change_email_returns_400
- PASSED tests/test_users.py::test_users_put_admin_can_update_user

## Limites actuelles

- Pas de pagination sur les listes
- Quelques warnings SQLAlchemy possibles selon version
- Pas de refresh token JWT (access token only)

## Auteurs

Florian Roosebeke
Tom Vieilledent

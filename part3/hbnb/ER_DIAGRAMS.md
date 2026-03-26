# HBnB - ER Diagrams (Mermaid)

This file contains the database ER diagrams for the HBnB Part 3 schema.

## 1. Core Database Schema

```mermaid
erDiagram
    USERS {
        char36 id PK
        varchar first_name
        varchar last_name
        varchar email UK
        varchar password
        boolean is_admin
    }

    PLACES {
        char36 id PK
        varchar title
        text description
        decimal price
        float latitude
        float longitude
        char36 owner_id FK
    }

    REVIEWS {
        char36 id PK
        text text
        int rating
        char36 user_id FK
        char36 place_id FK
    }

    AMENITIES {
        char36 id PK
        varchar name UK
    }

    PLACE_AMENITY {
        char36 place_id PK,FK
        char36 amenity_id PK,FK
    }

    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : receives
    PLACES ||--o{ PLACE_AMENITY : has
    AMENITIES ||--o{ PLACE_AMENITY : has
```

## 2. Extension Example - Reservation

```mermaid
erDiagram
    USERS {
        char36 id PK
        varchar first_name
        varchar last_name
        varchar email UK
        varchar password
        boolean is_admin
    }

    PLACES {
        char36 id PK
        varchar title
        text description
        decimal price
        float latitude
        float longitude
        char36 owner_id FK
    }

    RESERVATIONS {
        char36 id PK
        char36 user_id FK
        char36 place_id FK
        date start_date
        date end_date
        decimal total_price
        varchar status
    }

    USERS ||--o{ PLACES : owns
    USERS ||--o{ RESERVATIONS : makes
    PLACES ||--o{ RESERVATIONS : booked_for
```

## Export (PNG/SVG)

1. Open https://mermaid-js.github.io/mermaid-live-editor/
2. Paste one diagram block.
3. Check the render.
4. Export as PNG or SVG.

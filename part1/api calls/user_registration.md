```mermaid
sequenceDiagram
    autonumber
    participant Client as 👤 Client
    participant API as ⚙️ API Controller
    participant Owner as 👨‍💼 User (Owner)
    participant Place as 🏠 Place (Owned)
    participant DB as 🗄️ Database

    Note over Client, DB: Process: Delete Owner with Cascade

    Client->>API: delateAccount(userId)
    activate API

    API->>DB: fetchUserWithPlaces(userId)
    activate DB
    DB-->>API: User Data + List of Places
    deactivate DB

    API->>Owner: delate()
    activate Owner

    Note right of Owner: Composition logic starts

    loop For each Place in User.places
        Owner->>Place: delate()
        activate Place
        Place->>DB: DELETE FROM amenities WHERE place_id = ...
        Place->>DB: DELETE FROM places WHERE id = ...
        Place-->>Owner: Place & Amenities deleted
        deactivate Place
    end

    Owner->>DB: DELETE FROM users WHERE id = ...
    activate DB
    DB-->>Owner: User deleted
    deactivate DB

    Owner-->>API: Deletion complete
    deactivate Owner

    API-->>Client: 204 No Content (Success)
    deactivate API
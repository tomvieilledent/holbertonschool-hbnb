```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        +UUID id
        +datetime created_at
        +datetime updated_at
    }

    class Utilisateur {
        +string first_name
        +string last_name
        +string email
        +string password
        +bool admin
    }

    class Place {
        +string title
        +string description
        +float price
        +float latitude
        +float longitude
    }

    class Amenity {
        +string name
        +string description
    }

    class Review {
        +int rating
        +string comment
    }

    %% Héritage de la classe parente
    BaseModel <|-- Utilisateur
    BaseModel <|-- Place
    BaseModel <|-- Amenity
    BaseModel <|-- Review

    %% Relations de cycle de vie (Composition)
    Utilisateur "1" *-- "0..*" Place : est propriétaire
    Place "1" *-- "0..*" Amenity : possède

    %% Relations de Review
    Utilisateur "1" -- "0..*" Review : rédige
    Place "1" -- "0..*" Review : est notée par

    %% Relation Client (n'affecte pas l'existence de la place)
    Utilisateur "0..*" -- "0..*" Place : loue
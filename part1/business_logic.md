```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        +UUID id
        +datetime created_at
        +datetime updated_at
        +create()
        +get(id)
        +update(data)
        +delete()
    }

    class User {
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

    %% Inheritance
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Amenity
    BaseModel <|-- Review

    %% Life cycle relations (Composition)
    User "1" *-- "0..*" Place : owns
    Place "1" *-- "0..*" Amenity : contains

    %% Review relations
    User "1" -- "0..*" Review : writes
    Place "1" -- "0..*" Review : is rated by

    %% Booking relation
    User "0..*" -- "0..*" Place : rents
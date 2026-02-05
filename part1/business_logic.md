```mermaid
classDiagram
    class BaseModel {
        <<abstract>>
        +id : UUID
        +created_at : datetime
        +updated_at : datetime
        +create()
        +read()
        +update()
        +delate()
    }

    class User {
        +first_name : string
        +last_name : string
        +email : string
        +password : string
        +admin : bool
    }

    class Place {
        +title : string
        +description : string
        +price : float
        +latitude : float
        +longitude : float
    }

    class Amenity {
        +name : string
        +description : string
    }

    class Review {
        +rating : int
        +comment : string
    }

    %% Inheritance
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Amenity
    BaseModel <|-- Review

    %% Composition: if User owner or Place is deleted, children are deleted
    User "1" *-- "0..*" Place : owns
    Place "1" *-- "0..*" Amenity : contains

    %% Associations: Review and Booking (persist separately or linked)
    User "1" -- "0..*" Review : writes
    Place "1" -- "0..*" Review : is rated by
    User "0..*" -- "0..*" Place : rents
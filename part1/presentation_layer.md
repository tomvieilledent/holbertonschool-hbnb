```mermaid
---
config:
  layout: dagre
---
graph TD
    %% =====================
    %% Packages simulés avec subgraph
    %% =====================

    subgraph Presentation_Layer ["Presentation Layer"]
        UserService
        PlaceService
        ReviewService
        AmenityService
        API_Controller["API Controller"]
    end

    subgraph Business_Logic_Layer ["Business Logic Layer"]
        HBnBFacade["HBnB Facade"]
        User
        Place
        Review
        Amenity
    end

    subgraph Persistence_Layer ["Persistence Layer"]
        UserRepository
        PlaceRepository
        ReviewRepository
        AmenityRepository
        Database["Database"]
    end

    %% =====================
    %% Dépendances / communications
    %% =====================
    API_Controller --> HBnBFacade

    HBnBFacade --> User
    HBnBFacade --> Place
    HBnBFacade --> Review
    HBnBFacade --> Amenity

    User --> UserRepository
    Place --> PlaceRepository
    Review --> ReviewRepository
    Amenity --> AmenityRepository

    UserRepository --> Database
    PlaceRepository --> Database
    ReviewRepository --> Database
    AmenityRepository --> Database

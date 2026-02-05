```mermaid
flowchart TB
  subgraph PL ["Presentation Layer (API)"]
    API["API Endpoints"]
        
  end

  subgraph BL["Business Logic Layer"]
    FACADE["HBnBFacade"]
    MODELS["Models\n(User, Place, Review, Amenity)"]
  end

  subgraph PEL["Persistence Layer"]
    REPO["Repositories / DAO"]
    DB[(Database)]
  end

  API -->|calls| FACADE
  FACADE -->|uses| MODELS
  FACADE -->|CRUD| REPO
  REPO -->|read/write| DB


```mermaid
sequenceDiagram
    participant Client as 👤 Client (Frontend)
    participant API as ⚙️ API / Controller
    participant UserClass as 👤 User Instance
    participant DB as 🗄️ Database

    Client->>API: register(first_name, last_name, email, password)
    
    activate API
    API->>API: Validate email format & password strength
    
    create participant UserClass
    API->>UserClass: new User(data)
    
    activate UserClass
    UserClass->>UserClass: Inherit from BaseModel (Set UUID, created_at)
    UserClass-->>API: Instance created
    deactivate UserClass

    API->>UserClass: create()
    activate UserClass
    UserClass->>DB: INSERT INTO users (id, first_name, email, ...)
    activate DB
    DB-->>UserClass: Success (201 Created)
    deactivate DB
    UserClass-->>API: Persistence confirmed
    deactivate UserClass

    API-->>Client: HTTP 201 Created (User Object)
    deactivate API
```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant API
    participant UserInstance
    participant DB

    Client->>API: POST /register (data)
    activate API
    
    Note over API: Validation logic

    create participant UserInstance
    API->>UserInstance: new(first_name, last_name, email, password)
    activate UserInstance
    Note right of UserInstance: BaseModel sets UUID & created_at
    UserInstance-->>API: instance created
    deactivate UserInstance

    API->>UserInstance: create()
    activate UserInstance
    UserInstance->>DB: INSERT user data
    activate DB
    DB-->>UserInstance: 201 Created
    deactivate DB
    UserInstance-->>API: success
    deactivate UserInstance

    API-->>Client: Return User Object (JSON)
    deactivate API
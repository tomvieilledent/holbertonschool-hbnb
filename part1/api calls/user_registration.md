```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant A as API
    participant U as UserInstance
    participant D as Database

    C->>A: register(data)
    activate A
    
    A->>A: Validate data

    Note over U: BaseModel: Sets UUID & timestamps
    A->>U: Instantiate User
    activate U
    U-->>A: instance ready
    deactivate U

    A->>U: create()
    activate U
    U->>D: INSERT User
    activate D
    D-->>U: Saved
    deactivate D
    U-->>A: success
    deactivate U

    A-->>C: 201 Created (JSON)
    deactivate A
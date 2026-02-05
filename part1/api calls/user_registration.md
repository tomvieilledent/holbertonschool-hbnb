```mermaid
sequenceDiagram
    autonumber
    participant U as 👤 Client
    participant A as ⚙️ API
    participant M as 🏗️ User Instance
    participant D as 🗄️ Database

    U->>A: register(first_name, last_name, email, password)
    activate A

    A->>A: Validate user input (email format, etc.)

    Note over M: Initialization (BaseModel logic)
    create participant M
    A->>M: new User(data)
    activate M
    M->>M: Set UUID & created_at
    M-->>A: User object ready
    deactivate M

    Note over M: Persistence (CRUD method)
    A->>M: create()
    activate M
    M->>D: INSERT INTO users (id, first_name, email, created_at, ...)
    activate D
    D-->>M: Confirmation (Success)
    deactivate D
    M-->>A: User persisted
    deactivate M

    A-->>U: 201 Created (Return User details)
    deactivate A
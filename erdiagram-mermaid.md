erDiagram
    USER {
        int id PK
        string username
        string email
    }

    BOOKMARK {
        int id PK
        string name
        string url
        int user_id FK
    }

    TAG {
        int id PK
        string name
    }

    TAG_INSTANCE {
        int id PK
        int tag_id FK
        int bookmark_id FK
    }

    USER ||--o{ BOOKMARK : ""
    BOOKMARK ||--o{ TAG_INSTANCE : ""
    TAG_INSTANCE }o--|| TAG : ""

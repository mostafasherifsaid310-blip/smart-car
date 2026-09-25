# Entity Relationship Diagram (ERD)

The following ERD represents the main database entities and relationships
implemented in the Smart Car Service System.

```mermaid
erDiagram

    USER ||--o{ CAR : owns

    CAR ||--o{ MAINTENANCE_RECORD : has
    TECHNICIAN ||--o{ MAINTENANCE_RECORD : performs

    MAINTENANCE_RECORD ||--o{ MAINTENANCE_PART : uses
    SPARE_PART ||--o{ MAINTENANCE_PART : included_in

    CAR ||--o{ APPOINTMENT : has
    TECHNICIAN ||--o{ APPOINTMENT : assigned_to

    USER {
        int id PK
        string username
        string email
    }

    CAR {
        int id PK
        int owner_id FK
        string brand
        string model
        int year
        string license_plate UK
        int mileage
        string color
        datetime created_at
    }

    TECHNICIAN {
        int id PK
        string name
        string phone
        string email UK
        string specialization
        int experience_years
        boolean is_available
        datetime created_at
    }

    MAINTENANCE_RECORD {
        int id PK
        int car_id FK
        int technician_id FK
        string service_type
        text description
        date service_date
        int mileage
        decimal cost
        string status
        datetime created_at
    }

    SPARE_PART {
        int id PK
        string name
        string part_number UK
        text description
        decimal price
        int quantity
        int minimum_stock
        datetime created_at
    }

    MAINTENANCE_PART {
        int id PK
        int maintenance_id FK
        int spare_part_id FK
        int quantity_used
    }

    APPOINTMENT {
        int id PK
        int car_id FK
        int technician_id FK
        string service_type
        date appointment_date
        time appointment_time
        string status
        text notes
        datetime created_at
    }

Relationship Summary
A user can own multiple cars.
A car belongs to one user.
A car can have multiple maintenance records.
A technician can perform multiple maintenance records.
A maintenance record can contain multiple spare parts.
A spare part can be used in multiple maintenance records.
A car can have multiple appointments.
A technician can have multiple appointments.


Important Constraints
Car license plates are unique.
Technician emails are unique.
Spare-part numbers are unique.
A technician cannot have two appointments at the same date and time.
The same spare part cannot be added twice to the same maintenance record.
Maintenance-part quantity must be at least 1.    
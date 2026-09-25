# System Architecture

The Smart Car Service System follows a modular Django architecture.
The system is organized into independent Django applications, each
responsible for a specific business domain.

## Architecture Diagram

```mermaid
flowchart TD

    U[User / Browser]

    U --> R[Django URL Router]

    R --> AUTH[Authentication App]
    R --> CAR[Cars App]
    R --> MAIN[Maintenance App]
    R --> PARTS[Spare Parts App]
    R --> TECH[Technicians App]
    R --> APPT[Appointments App]
    R --> DASH[Dashboard App]
    R --> AI[AI Agent App]

    AUTH --> ORM[Django ORM]
    CAR --> ORM
    MAIN --> ORM
    PARTS --> ORM
    TECH --> ORM
    APPT --> ORM
    DASH --> ORM

    ORM --> DB[(PostgreSQL Database)]

    AI --> GEMINI[Google Gemini API]
    AI --> MAIN

    MAIN --> PARTS
    MAIN --> TECH
    APPT --> TECH
    APPT --> CAR
    MAIN --> CAR
    CAR --> AUTH

Main Components
1. User / Browser

The user interacts with the Smart Car Service System through a web browser.

Users can:

Register and log in.
Manage their cars.
View and manage maintenance records.
Manage spare parts.
Book and manage appointments.
View dashboard information.
Interact with the AI maintenance assistant.


2. Django URL Router

The main URL configuration is located in:

config/urls.py

It routes requests to the appropriate Django application.

Main routes include:

/auth/
/cars/
/maintenance/
/spare-parts/
/appointments/
/dashboard/
/technicians/
/ai/


3. Django Applications

The project is divided into multiple applications:

Authentication

Handles:

User registration
Login
Logout
Authentication-related functionality
Cars

Handles:

Car creation
Car updates
Car deletion
Car ownership
Car information
Maintenance

Handles:

Maintenance records
Maintenance services
Technicians assigned to maintenance
Spare parts used during maintenance
Spare Parts

Handles:

Spare-part management
Stock quantities
Minimum stock levels
Part prices
Technicians

Handles:

Technician information
Specializations
Availability
Experience
Appointments

Handles:

Appointment creation
Appointment scheduling
Technician assignment
Appointment status
Dashboard

Provides the main dashboard and summary information for users.

AI Agent

Provides AI-assisted maintenance functionality and communicates with the
Google Gemini API when AI processing is required.

4. Django ORM

The applications use Django ORM to communicate with the database.

The ORM provides:

Database queries
Model relationships
Data validation
CRUD operations
5. PostgreSQL Database

PostgreSQL stores the application's persistent data, including:

Users
Cars
Maintenance records
Technicians
Spare parts
Appointments
6. Google Gemini API

The AI Agent communicates with Google Gemini to provide AI-assisted
maintenance functionality.

The external AI service is isolated inside the AI Agent application.

Application Relationships

The main business relationships are:

A user can own multiple cars.
A car can have multiple maintenance records.
A technician can perform multiple maintenance records.
A maintenance record can use multiple spare parts.
A car can have multiple appointments.
A technician can have multiple appointments.
The AI Agent can use maintenance-related information to provide
AI-assisted responses.


Project Structure
smart-car/
│
├── ai_agent/
├── appointments/
├── authentication/
├── cars/
├── config/
├── dashboard/
├── maintenance/
├── spare_parts/
├── technicians/
├── templates/
├── docs/
│   ├── SRS.md
│   ├── ERD.md
│   └── ARCHITECTURE.md
│
├── manage.py
├── requirements.txt
└── README.md
Architectural Approach

The system uses a modular Django architecture where each application
contains functionality related to a specific domain.

This structure improves:

Maintainability
Separation of responsibilities
Code organization
Scalability
Testing and debugging

The architecture can be extended in the future by adding new Django
applications or external services without significantly changing the
existing modules.    
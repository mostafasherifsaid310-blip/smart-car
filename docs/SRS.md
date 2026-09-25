# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose

The Smart Car Service System is a web-based application developed using Django to manage car service and maintenance operations.

The system provides a centralized platform for managing cars, maintenance records, spare parts, technicians, appointments, users, and AI-assisted interactions.

### 1.2 Scope

The system supports the following main operations:

* User authentication and authorization
* Role-Based Access Control (RBAC)
* Car management
* Car ownership management
* Maintenance record management
* Spare parts management
* Technician management
* Appointment management
* Dashboard and service information
* AI-assisted interactions
* PostgreSQL database management

### 1.3 Intended Users

The system supports different users according to their permissions and roles.

#### Regular Users

Regular users can:

* Authenticate into the system.
* Manage their own cars.
* View information related to their cars.
* Access supported maintenance and service operations.
* Use the AI Agent for supported requests.

#### Authorized Staff

Authorized staff can perform administrative service operations according to their assigned permissions, such as:

* Managing maintenance records.
* Managing spare parts.
* Managing technicians.
* Managing appointments.

#### Administrators

Administrators are responsible for system-level administration, user management, permissions, and other administrative operations according to the application's authorization rules.

---

# 2. Functional Requirements

## 2.1 Authentication

The system shall:

* Allow users to log in.
* Allow users to log out.
* Authenticate users before accessing protected functionality.
* Apply authorization rules to protected operations.

## 2.2 Role-Based Access Control

The system shall:

* Support different user roles and permissions.
* Restrict protected operations based on user authorization.
* Prevent unauthorized users from accessing restricted functionality.

## 2.3 Car Management

The system shall allow authorized users to:

* Create car records.
* View car information.
* Update car information.
* Delete car records.
* Associate cars with their owners.

Each car contains information such as:

* Owner
* Brand
* Model
* Year
* License plate
* Mileage
* Color
* Creation date

## 2.4 Maintenance Management

The system shall allow authorized users to manage maintenance records.

A maintenance record contains:

* Car
* Technician
* Service type
* Description
* Service date
* Mileage
* Cost
* Status
* Creation date

The system shall validate maintenance data and prevent invalid mileage and cost values.

## 2.5 Spare Parts Management

The system shall manage spare parts including:

* Part name
* Part number
* Description
* Price
* Quantity
* Minimum stock
* Creation date

The system shall validate prices and stock quantities.

## 2.6 Maintenance Parts

The system shall record spare parts used during maintenance.

Each usage record contains:

* Maintenance record
* Spare part
* Quantity used

The system shall prevent duplicate maintenance/spare-part combinations and require a valid quantity.

## 2.7 Technician Management

The system shall manage technicians including:

* Name
* Phone
* Email
* Specialization
* Experience years
* Availability
* Creation date

The system shall prevent duplicate technician email addresses.

## 2.8 Appointment Management

The system shall allow appointment records to contain:

* Car
* Technician
* Service type
* Appointment date
* Appointment time
* Status
* Notes
* Creation date

The system shall prevent the same technician from being assigned to two appointments at the same date and time.

## 2.9 Dashboard

The system shall provide dashboard functionality for presenting relevant service and system information to authorized users.

## 2.10 AI Agent

The system shall provide an AI-assisted interface for supported natural-language requests.

The AI Agent shall:

* Interpret supported user requests.
* Detect the requested operation.
* Collect required information through multi-step interactions.
* Execute supported operations through the application.
* Respect authentication and authorization rules.
* Maintain pending actions when additional information is required.

Supported AI operations may include maintenance-related and other service-management requests implemented by the application.

---

# 3. Non-Functional Requirements

## 3.1 Security

The system shall:

* Require authentication for protected functionality.
* Apply authorization and RBAC rules.
* Enforce car ownership security where applicable.
* Keep sensitive configuration outside source code.
* Avoid committing API keys and passwords to the repository.

## 3.2 Performance

The system should provide responsive interaction for normal application operations and database queries.

Database indexes are used on frequently queried fields to improve query performance.

## 3.3 Reliability

The system should:

* Validate user input.
* Enforce database constraints.
* Handle invalid operations safely.
* Maintain data consistency through database relationships and constraints.

## 3.4 Maintainability

The system shall be organized into Django applications based on business functionality.

Main applications include:

* `authentication`
* `cars`
* `maintenance`
* `spare_parts`
* `technicians`
* `appointments`
* `dashboard`
* `ai_agent`

## 3.5 Usability

The system should provide clear interfaces and understandable workflows for common car service operations.

---

# 4. Data Requirements

The main persistent entities are:

### User

Provided by Django's built-in authentication system.

A user can own multiple cars.

### Car

Represents a vehicle owned by a user.

### Technician

Represents a service technician.

### MaintenanceRecord

Represents a maintenance operation performed on a car by a technician.

### SparePart

Represents a spare part available in the system.

### MaintenancePart

Represents a spare part used during a specific maintenance operation.

### Appointment

Represents a scheduled service appointment between a car and a technician.

---

# 5. Entity Relationships

The main relationships are:

* One User can own many Cars.
* One Car can have many Maintenance Records.
* One Technician can perform many Maintenance Records.
* One Maintenance Record can use many Spare Parts through MaintenancePart.
* One Spare Part can be used in many Maintenance Records through MaintenancePart.
* One Car can have many Appointments.
* One Technician can have many Appointments.

---

# 6. Business Rules

The system applies the following rules:

1. A car belongs to a specific user.
2. License plates must be unique.
3. Car mileage cannot be negative.
4. Car year must be between 1900 and 2100.
5. Maintenance mileage cannot be negative.
6. Maintenance cost cannot be negative.
7. Spare-part price cannot be negative.
8. Spare-part quantity cannot be negative.
9. Minimum stock cannot be negative.
10. Technician experience cannot be negative.
11. Technician email must be unique.
12. A maintenance record references one car and one technician.
13. A technician cannot have two appointments at the same date and time.
14. A maintenance record cannot contain the same spare part more than once.
15. Quantity used for a maintenance part must be at least one.

---

# 7. System Architecture

The application follows a Django-based web application architecture.

### Presentation Layer

Responsible for:

* HTML templates
* CSS
* JavaScript
* User interaction

### Application Layer

Implemented using Django applications and views.

Responsibilities include:

* Authentication
* Business logic
* Request handling
* Validation
* Authorization
* AI Agent integration

### Data Layer

Implemented using:

* Django ORM
* PostgreSQL

The data layer stores users, cars, maintenance records, spare parts, technicians, appointments, and related information.

### AI Layer

The AI Agent uses Google GenAI to interpret supported natural-language requests and interact with application functionality.

---

# 8. Technology Stack

* Python
* Django
* PostgreSQL
* Django ORM
* Google GenAI
* psycopg
* python-dotenv
* HTML
* CSS
* JavaScript
* Git
* GitHub

---

# 9. Installation Requirements

The development environment requires:

* Python
* PostgreSQL
* pip
* Git

Python dependencies are listed in:

```text
requirements.txt
```

---

# 10. Project Setup

Clone the repository:

```bash
git clone https://github.com/mostafasherifsaid310-blip/smart-car.git
cd smart-car
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables.

Apply migrations:

```bash
python manage.py migrate
```

Create an administrator:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

---

# 11. Testing

Run Django system checks:

```bash
python manage.py check
```

Run automated tests:

```bash
python manage.py test
```

The project should be tested for:

* Authentication
* Authorization
* Car ownership
* CRUD operations
* Maintenance workflows
* Appointment constraints
* AI Agent workflows
* Invalid input handling

---

# 12. Version Control

The project uses Git and GitHub for version control.

The development workflow includes:

1. Creating a dedicated branch.
2. Making focused commits.
3. Pushing the branch to GitHub.
4. Creating a Pull Request.
5. Reviewing and merging the Pull Request.
6. Deleting the merged branch.

GitHub Issues are used to track tasks and documentation work.

---

# 13. Future Improvements

Potential future improvements include:

* Additional AI-supported operations.
* More comprehensive automated tests.
* Improved reporting and analytics.
* Enhanced notification features.
* Additional service-management functionality.
* Improved monitoring and logging.

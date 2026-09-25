# Smart Car Service System

Smart Car is a Django-based web application for managing car service operations. The system provides tools for managing users, cars, maintenance records, spare parts, technicians, appointments, and an AI-assisted service interface.

## Project Overview

The Smart Car Service System is designed to organize car maintenance operations in one web application.

Users can manage their cars and related service information, while authorized users can manage maintenance records, spare parts, technicians, and appointments according to their permissions.

The system also includes an AI Agent that allows users to interact with the application through natural-language requests for supported operations.

## Main Features

* User authentication and authorization
* Role-Based Access Control (RBAC)
* Car management
* Car ownership security
* Maintenance management
* Spare parts management
* Technician management
* Appointment management
* Dashboard
* AI Agent integration
* PostgreSQL database support
* Form validation and access control
* Automated testing

## AI Agent

The system includes an AI-assisted interface that can understand supported user requests and perform application-related operations.

Examples include:

* Creating maintenance records
* Viewing car information
* Accessing maintenance-related information
* Handling supported appointment requests
* Continuing multi-step operations using pending actions

The AI Agent is integrated with the Django application and works with the application's authentication and authorization rules.

## Technologies

* Python
* Django
* PostgreSQL
* Google GenAI
* psycopg
* python-dotenv
* HTML
* CSS
* JavaScript
* Git
* GitHub

## Project Structure

```text
smart-car/
│
├── ai_agent/
├── appointments/
├── authentication/
├── cars/
├── dashboard/
├── maintenance/
├── spare_parts/
├── technicians/
├── config/
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mostafasherifsaid310-blip/smart-car.git
cd smart-car
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

On Windows:

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and configure the required environment variables.

Example:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

GOOGLE_API_KEY=your_google_api_key
```

Do not commit real passwords, API keys, or other secrets to GitHub.

## Database Setup

Make sure PostgreSQL is installed and running.

Create the required PostgreSQL database, then apply Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create an Administrator

Create a Django superuser:

```bash
python manage.py createsuperuser
```

Follow the terminal instructions to set the username, email, and password.

## Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Testing

Run Django system checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test
```

## Git & GitHub Workflow

The project follows a feature-branch workflow:

1. Create a dedicated branch for a feature, fix, or documentation task.
2. Make focused commits.
3. Push the branch to GitHub.
4. Create a Pull Request.
5. Review and merge the Pull Request into `main`.
6. Delete the merged branch.

Issues are used to track project tasks and documentation work.

## Documentation

Project documentation includes:

* Software Requirements Specification (SRS)
* Entity Relationship Diagram (ERD)
* System Architecture Diagram
* Installation and setup instructions
* Project structure and technical documentation

## Security

The project follows basic security practices including:

* Authentication
* Authorization
* Role-Based Access Control
* User ownership checks
* Environment variables for sensitive configuration
* Protection against committing secrets

## License

This project is developed as an academic/software engineering project.

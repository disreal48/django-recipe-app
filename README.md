# Django Recipe App

This is a Django-based recipe application. You can add, search for, edit or delete cooking-recipes. It automaticly generates a difficulty for each recipe. The project is structured to follow best practices and is ready for both development and production environments.

## Table of Contents

- [Setup](#setup)
- [Using PostgreSQL](#using-postgresql)
- [Using SQLite3](#using-sqlite3)
- [Makefile Commands](#makefile-commands)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/django-recipe-app.git
   cd django-recipe-app
   ```

2. Rename the project directory:

   ```bash
   mv django-recipe-app/ <your-project-name>
   ```

3. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements/dev.txt
   ```

5. Create an `.env` file with the following configurations:

   ```env
   SECRET_KEY=<your-secret-key>
   DB_NAME=<your-db-name>
   DB_USER=postgres
   DB_PWD=postgres
   DB_HOST=127.0.0.1
   DB_PORT=5432
   ```

6. Generate your `SECRET_KEY` using Python:
   ```python
   import secrets
   secrets.token_urlsafe(50)
   ```

## Using PostgreSQL

1. Set up PostgreSQL:

   ```bash
   psql -U postgres
   CREATE ROLE <role-name> WITH PASSWORD '<password>';
   ALTER ROLE <role-name> CREATEDB;
   ALTER ROLE <role-name> LOGIN;
   ```

2. Create the database:

   ```bash
   \c postgres <role-name>
   CREATE DATABASE <db-name>;
   ```

3. Fill in the database values in the `.env` file.

## Using SQLite3

1. If you want to use `sqlite3` as your database, only the `SECRET_KEY` is required in the `.env` file.

2. Adjust the database settings in config/settings/dev.py for SQLite3 by uncommenting the SQLite3 configuration and commenting out the PostgreSQL configuration.

## Makefile Commands

- `make dev-install`: Install development dependencies.
- `make dev-startapp app=<app-name>`Create a new Django app.
- `make makemigrations`: Create new migrations based on the changes detected in your models.
- `make migrate`: Apply the migrations to the database.
- `make runserver`: Run the Django development server.
- `dev-superuser`: Create a superuser

## License

This project is licensed under the MIT License.

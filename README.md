# Library Management System

A simple, professional monolithic Django project for managing a library catalog, student accounts, and book issue/return records.

## Features

- Student signup, login, and logout
- Admin and Student roles
- Dashboard with total books, issued books, available copies, and registered users
- Admin book management: add, edit, and delete books
- Book issue and return workflow
- Student view for issued books
- Search books by title, author, category, or ISBN
- Pagination on book and issue listings
- REST APIs for books, users, and issue records using Django REST Framework
- PostgreSQL database configuration
- Bootstrap 5 responsive UI
- CSRF protection, server-side validation, authentication checks, and role-based access control

## Project Structure

```text
library_management_system/
accounts/
books/
transactions/
templates/
static/
manage.py
requirements.txt
```

## Setup

1. Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a PostgreSQL database.

```bash
createdb library_management
```

4. Configure environment variables.

```bash
cp .env.example .env
```

Then update `.env` values for your local PostgreSQL username and password. Export the variables before running Django, or use your shell profile.

```bash
export DJANGO_SECRET_KEY="replace-this-with-a-long-random-secret"
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
export POSTGRES_DB=library_management
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

5. Run migrations.

```bash
python manage.py migrate
```

6. Create an admin user.

```bash
python manage.py createsuperuser
```

Superusers can access admin-only views even if their library role is not manually set to Admin.

7. Start the development server.

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Free Deployment on Render

This repository includes `render.yaml`, `build.sh`, and `start.sh` for Render deployment.

1. Push this project to a GitHub repository.
2. Create a Render account.
3. In Render, choose **New > Blueprint** and connect the GitHub repository.
4. Render will create:
   - a free Django web service
   - a free PostgreSQL database
   - production environment variables from `render.yaml`
5. After deploy, open the generated `.onrender.com` URL.

Render free services are useful for demos and reviews, but they are not intended for production traffic.

### Render Admin User

The start script runs `python manage.py create_admin` after migrations. Set these environment variables in Render:

```bash
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_EMAIL=admin@example.com
DJANGO_ADMIN_PASSWORD=choose-a-strong-password
```

If you deploy with the included Blueprint for the first time, Render prompts you for `DJANGO_ADMIN_PASSWORD`. For an already-created Render service, add or update these variables from the service's **Environment** page, then redeploy.

## API Endpoints

All API endpoints require authentication.

- `GET /api/books/` - list books
- `POST /api/books/` - create a book as admin
- `GET /api/users/` - list users as admin
- `GET /api/issues/` - list issue records
- `POST /api/issues/` - issue a book as admin
- `POST /api/issues/<id>/return/` - return a book

The DRF login view is available at `/api-auth/login/`.

## Notes

- Student signup creates Student-role users only.
- Admin permissions are granted to users with the Admin role, staff status, or superuser status.
- Book availability is recalculated automatically from quantity and active issue records.

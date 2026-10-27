# Django backend for the Users App (React)

Django + Django REST Framework API for users, contacts, contact types and token auth.

## Setup

    python -m venv .venv
    # Windows: .venv\Scripts\activate     macOS/Linux: source .venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser     # optional, for /admin/
    python manage.py runserver

API base URL (matches `src/api/config.js` in the React app): http://127.0.0.1:8000/api

## Endpoints (all end with a trailing slash)

| Method | URL | Notes |
|---|---|---|
| POST | /api/auth/login/ | `{username, password}` -> `{token, user}` |
| POST | /api/auth/logout/ | header `Authorization: Token <token>` |
| GET | /api/auth/me/ | header `Authorization: Token <token>` |
| GET, POST | /api/users/ | POST is multipart/form-data (avatar = `profile` file) |
| GET, PUT, PATCH, DELETE | /api/users/<id>/ | DELETE is a soft delete (`is_active=False`) |
| GET, POST | /api/contact-types/ | |
| GET, PUT, PATCH, DELETE | /api/contact-types/<id>/ | deleting a type deletes its contacts (CASCADE) |
| GET, POST | /api/contacts/ | POST body: `{owner, type_id, value}` |
| GET, PUT, PATCH, DELETE | /api/contacts/<id>/ | |

## Project layout

    core/        project settings and root urls (api/ is mounted here)
    accounts/    models (BaseUser, ContactType, Contact), serializers, views, urls, tests
    media/users/default.jfif   default avatar used by BaseUser.profile

## Notes

- `AUTH_USER_MODEL = 'accounts.BaseUser'` is set in settings. If you add this to an existing
  project that already ran migrations, delete the old db and migrations first.
- Auth is DRF TokenAuthentication. Only the auth endpoints enforce it; the other endpoints
  are open on purpose (permissions come in a later lesson).
- `ContactSerializer.owner` is writable because there are no permissions yet. Later, make it
  read-only and use `serializer.save(owner=request.user)`.
- CORS allows http://localhost:5173 and http://127.0.0.1:5173 (edit `CORS_ALLOWED_ORIGINS`).
- Run the tests with `python manage.py test`.
- `SECRET_KEY` in settings.py is the development key. Do not deploy it.

# Pulse API — a Django learning project

> A small feedback & roadmap web API (teams post feature requests, users upvote them),
> built to practise Django, REST APIs and the MVC pattern beyond university coursework.
> Work in progress — I'm learning in the open.

> API web de feedback y hoja de ruta (los equipos publican peticiones y los usuarios votan),
> hecha para practicar Django, APIs REST y el patrón MVC más allá de las prácticas de clase.
> En desarrollo — aprendiendo sobre la marcha.

**Stack:** Python 3.14 · Django 6 · Django REST Framework · SQLite

---

## Why this project · Por qué este proyecto

I wanted a project bigger than a class exercise to actually understand how a web backend
fits together: designing the data model, separating concerns (models → serializers →
views), exposing a REST API, and covering it with tests. It's not a real product — it's a
place to learn.

Quería un proyecto más grande que un ejercicio de clase para entender de verdad cómo
encaja un backend web: diseñar el modelo de datos, separar responsabilidades
(modelos → serializers → vistas), exponer una API REST y cubrirla con tests. No es un
producto real, es un sitio para aprender.

## What it does so far · Qué hace por ahora

- Data model with users, organizations, boards, posts, votes and comments.
- Token-based authentication: register, login and a "current user" endpoint.
- REST API to list/create posts and toggle an upvote (one vote per user per post).
- Django admin to browse the data.
- A handful of tests for the domain rules, the API and the auth flow.

## What I learned / practised · Qué he aprendido

- Structuring a Django project into apps and following the MVC/MVT separation.
- Building a REST API with Django REST Framework (serializers, viewsets, routers).
- Modelling relationships (foreign keys, many-to-many through a join model).
- Writing tests with Django's test client.

## Run it locally · Cómo ejecutarlo

```bash
python -m venv .venv
source .venv/Scripts/activate      # Windows Git Bash;  .venv/bin/activate on Linux/macOS
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- API: `http://127.0.0.1:8000/api/`
- Admin: `http://127.0.0.1:8000/admin/` (run `python manage.py createsuperuser` first)

## Main endpoints

Authentication uses DRF tokens: register or log in, then send the token on later
requests as `Authorization: Token <key>`.

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/auth/register/` | Create an account, returns a token |
| `POST` | `/api/auth/login/` | Exchange email + password for a token |
| `GET`  | `/api/auth/me/` | Current user (token required) |
| `GET`  | `/api/boards/` | List boards |
| `GET`  | `/api/posts/?board=<id>` | List posts on a board |
| `POST` | `/api/posts/` | Create a feature request (login required) |
| `POST` | `/api/posts/<id>/vote/` | Toggle your upvote (login required) |
| `GET`  | `/api/comments/?post=<id>` | List comments on a post |

## Tests

```bash
python manage.py test
```

## Ideas for next steps · Siguientes pasos

Things I'd like to add as I learn more: filtering the roadmap by status, subscription
plans (Stripe test mode), and a simple React frontend to consume the API.

---

MIT licensed. Built by [Jorge](https://github.com/Jorgepele) while learning Django.

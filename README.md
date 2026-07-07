# Pulse API — a Django learning project

[![CI](https://github.com/Jorgepele/pulse-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Jorgepele/pulse-api/actions/workflows/ci.yml)

> A small feedback & roadmap web API (teams post feature requests, users upvote them),
> built to practise Django, REST APIs and the MVC pattern beyond university coursework.
> Work in progress — I'm learning in the open.

> API web de feedback y hoja de ruta (los equipos publican peticiones y los usuarios votan),
> hecha para practicar Django, APIs REST y el patrón MVC más allá de las prácticas de clase.
> En desarrollo — aprendiendo sobre la marcha.

**Stack:** Python 3.14 · Django 6 · Django REST Framework · SQLite

---

## Live demo · Demo en vivo

Deployed on Render (free tier — the first request may take ~30 s while the
service wakes up):

- API root: **https://pulse-api-wmuq.onrender.com/**
- Interactive API docs (Swagger): **https://pulse-api-wmuq.onrender.com/api/docs/**

The React frontend that consumes it lives at
**https://pulse-web-lvhx.onrender.com** — log in with `demo@pulse.dev` / `demo12345`.

Desplegado en Render (plan gratis — la primera petición puede tardar ~30 s
mientras el servicio arranca). Frontend que la consume:
https://pulse-web-lvhx.onrender.com (`demo@pulse.dev` / `demo12345`).

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
- REST API to list/create posts, toggle an upvote (one vote per user per post),
  and read/write comments.
- Subscription plans and a (simulated) subscribe endpoint — the SaaS-shaped
  pieces, without taking real payments.
- A `seed_demo` command that fills the database with a demo account, board,
  posts and plans so the API has something to show.
- Django admin to browse the data.
- 23 tests covering the domain rules, the API, auth and billing.

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
python manage.py seed_demo      # optional: demo account + example data
python manage.py runserver
```

- API: `http://127.0.0.1:8000/api/`
- Admin: `http://127.0.0.1:8000/admin/` (run `python manage.py createsuperuser` first)
- Demo login after `seed_demo`: `demo@pulse.dev` / `demo12345`

## Main endpoints

Interactive API docs (Swagger UI) are served at `/api/docs/`, generated from an
OpenAPI schema at `/api/schema/`.

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
| `POST` | `/api/comments/` | Add a comment (login required) |
| `GET`  | `/api/plans/` | List subscription plans (public) |
| `GET`/`POST` | `/api/billing/subscription/` | Read or set the org's plan (demo, no payment) |

## Tests

```bash
python manage.py test
```

Tests also run on every push via GitHub Actions (see the CI badge above).

## Deploy · Despliegue

The project is set up to deploy on [Render](https://render.com) (env-based
settings, WhiteNoise, gunicorn). Step-by-step guide in [DEPLOY.md](DEPLOY.md).

## Ideas for next steps · Siguientes pasos

Things I'd like to add as I learn more: replacing the simulated billing with a real
Stripe test-mode integration, filtering the roadmap by status, and porting the core
to Rails and Laravel to compare how MVC maps across frameworks. The React frontend
lives in [pulse-web](https://github.com/Jorgepele/pulse-web).

---

MIT licensed. Built by [Jorge](https://github.com/Jorgepele) while learning Django.

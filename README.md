# Pulse API — Feedback & Roadmap SaaS

> A multi-tenant SaaS backend where teams collect feature requests, let users upvote them, and publish a public roadmap. Built with Django REST Framework.
>
> Backend SaaS multi-tenant donde los equipos recogen peticiones de funcionalidades, permiten votarlas y publican una hoja de ruta pública. Hecho con Django REST Framework.

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white">
  <img alt="Django" src="https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white">
  <img alt="DRF" src="https://img.shields.io/badge/DRF-3.17-A30000">
  <img alt="Tests" src="https://img.shields.io/badge/tests-passing-brightgreen">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
</p>

---

## 🇬🇧 English

### What it demonstrates
- **Multi-tenant architecture** — every board and post belongs to an `Organization`, users join via `Membership` roles.
- **Clean MVC/MVT layering** — models (domain) → serializers (boundary) → views (controllers) → URLs (routing).
- **Custom user model** authenticated by email.
- **REST API** with a stateful vote-toggle action, filtering and pagination.
- **Subscription plans** (Free/Pro) modeled for Stripe test-mode integration.
- **Tested** — domain + API tests run in CI.

### Domain model
```
User ──owns──> Organization <──Membership──> User
                    │
                    ├── Board ──> Post ──> Vote (1 per user)
                    │                └──> Comment
                    └── Subscription ──> Plan
```

### Quick start
```bash
python -m venv .venv
source .venv/Scripts/activate      # Windows Git Bash;  use .venv/bin/activate on Unix
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
- API root: `http://127.0.0.1:8000/api/`
- Admin: `http://127.0.0.1:8000/admin/`
- Health: `http://127.0.0.1:8000/`

### Key endpoints
| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/api/boards/` | List boards |
| `GET`  | `/api/posts/?board=<id>` | List posts on a board |
| `POST` | `/api/posts/` | Create a feature request (auth) |
| `POST` | `/api/posts/<id>/vote/` | Toggle your upvote (auth) |
| `GET`  | `/api/comments/?post=<id>` | List comments |

### Tests
```bash
python manage.py test
```

---

## 🇪🇸 Español

### Qué demuestra
- **Arquitectura multi-tenant** — cada tablero y post pertenece a una `Organization`; los usuarios se unen con roles vía `Membership`.
- **Capas MVC/MVT limpias** — modelos (dominio) → serializers (frontera) → vistas (controladores) → URLs (enrutado).
- **Modelo de usuario propio** autenticado por email.
- **API REST** con acción de voto con estado (toggle), filtrado y paginación.
- **Planes de suscripción** (Free/Pro) modelados para integración con Stripe en modo test.
- **Con tests** — dominio + API ejecutados en CI.

### Arranque rápido
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Consulta la tabla de endpoints en la sección en inglés.

---

Part of the [Pulse portfolio](../PORTFOLIO.md): `pulse-api` (Django) · `pulse-web` (React) · `pulse-rails` · `pulse-laravel` · `fp-kit`.

# Deploying Pulse to Render

Pulse is two services: the Django API (`pulse-api`) and the React frontend
(`pulse-web`). Both include a `render.yaml` blueprint. The free tier is enough
for a demo.

> **Note on data:** the free tier uses SQLite on an ephemeral disk, so the
> database is re-created and re-seeded on every deploy (see `buildCommand`).
> That's fine for a demo. For persistence, add a Render PostgreSQL instance and
> point Django at it via `DATABASE_URL` (needs `dj-database-url` + a Postgres
> driver) — a good next step, not required to go live.

## 1. Deploy the API

1. Push this repo to GitHub (already done).
2. In Render: **New → Blueprint**, connect the `pulse-api` repo. Render reads
   `render.yaml` and creates the web service.
3. Render sets `SECRET_KEY` automatically and `DEBUG=False`. Leave
   `ALLOWED_HOSTS` as `.onrender.com`.
4. Deploy. When it's live, note the URL, e.g. `https://pulse-api.onrender.com`.
   Check `https://pulse-api.onrender.com/` returns `{"status": "ok"}`.

## 2. Deploy the frontend

1. In Render: **New → Blueprint**, connect the `pulse-web` repo.
2. Set the `VITE_API_URL` environment variable to your API URL from step 1
   (e.g. `https://pulse-api.onrender.com`). Deploy.
3. Note the frontend URL, e.g. `https://pulse-web.onrender.com`.

## 3. Wire the two together

Back in the **pulse-api** service, set the environment variable:

```
CORS_ALLOWED_ORIGINS = https://pulse-web.onrender.com
```

(optionally also `CSRF_TRUSTED_ORIGINS` with the same value). Redeploy the API.

## 4. Verify

Open the frontend URL, log in with the seeded demo account
(`demo@pulse.dev` / `demo12345`), and check the board loads, voting works and
you can subscribe to a plan.

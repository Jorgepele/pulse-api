# 0004 — SQLite in production, on purpose

**Status:** accepted · **Date:** 2026-07-07

## Context

Pulse is deployed on Render's free tier so that anyone reading the README can click a link
and use it. The free tier gives an ephemeral filesystem and spins the service down after
inactivity. A managed Postgres would be the normal choice for a real product.

## Decision

Ship SQLite, and treat the deployed database as **disposable**. `seed_demo` recreates the
demo organization, board, posts and the `demo@pulse.dev` account on each deploy.

## Consequences

- The demo is free to run and needs no external service. Nothing to configure, nothing to
  expire, nothing to pay for.
- **Data written by visitors is lost on redeploy.** For a demo whose whole point is to be
  poked at by strangers, that is a feature, not a bug: it resets itself.
- The first request after a cold start is slow, because Render has to wake the service.
  This surprises people who click the link and think it is broken. The READMEs say so.
- SQLite serializes writes. With one demo visitor at a time this never shows; under real
  concurrency it would be the first thing to replace.
- Because the schema is recreated rather than migrated in place, a bad migration would
  hide here and only appear on a real database. Migrations are still written and committed
  properly for exactly that reason.

Switching to Postgres would mean a Render Postgres add-on and teaching
`config/settings.py` to read a `DATABASE_URL` — today the SQLite path is hardcoded there,
unlike the other settings, which do come from the environment. That inconsistency is
known and not yet fixed.

---

**En una frase:** SQLite en producción porque la demo es desechable y se resiembra en cada
despliegue; el precio es perder los datos de los visitantes y no aguantar concurrencia real.

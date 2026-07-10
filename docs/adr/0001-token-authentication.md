# 0001 — Token authentication instead of sessions or JWT

**Status:** accepted · **Date:** 2026-07-03

## Context

Pulse is a JSON API consumed by a separate React frontend (`pulse-web`), deployed on
a different origin. Django's default is session authentication: a cookie plus a CSRF
token. That works when Django renders the pages, but across origins it means CORS with
credentials, `SameSite` cookie rules, and CSRF tokens on every write.

The obvious alternatives were sessions, DRF's built-in `TokenAuthentication`, and JWT.

## Decision

Use DRF's `TokenAuthentication`. The client sends `Authorization: Token <key>` on every
request. The token is created at register/login, stored in the database, and looked up
on each request.

Session authentication is *also* enabled, but only so the browsable API stays usable
during development.

## Consequences

- The frontend just keeps a string and puts it in a header. No cookies, no CSRF.
- Every authenticated request costs one extra database lookup for the token. That is
  the trade-off against JWT, which is verified by signature without touching the database.
- Tokens do not expire and are not rotated. A leaked token is valid until deleted.
  A production system would add expiry, rotation and a logout that revokes the token.
- The token lives in `localStorage` in the frontend, which is readable by any script on
  the page. An `HttpOnly` cookie would resist XSS better, at the cost of bringing CSRF
  back. This is the honest weak point of the setup.

## Why not JWT

JWT is stateless, which is a real advantage when several services must verify a token
without sharing a database. Pulse is one service and one database, so statelessness buys
nothing here and costs the ability to revoke a token immediately.

---

**En una frase:** token en cabecera en vez de sesiones, porque el frontend vive en otro
origen; el coste es una consulta por petición y que un token filtrado no caduca.

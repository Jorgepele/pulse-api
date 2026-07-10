# Architecture decision records · Registros de decisión

Short notes on **why** Pulse is built the way it is. Each one records the context,
the decision, what it costs, and what I would reconsider. They exist so the choices
can be explained rather than defended after the fact.

Notas breves sobre **por qué** Pulse está construido así: contexto, decisión, coste y
qué reconsideraría. Existen para poder explicar las decisiones, no para justificarlas
a posteriori.

| # | Decision |
|---|----------|
| [0001](0001-token-authentication.md) | Token authentication instead of sessions or JWT |
| [0002](0002-tenant-visibility.md) | One queryset defines what a tenant can see |
| [0003](0003-simulated-billing.md) | Billing is simulated; real Stripe is opt-in |
| [0004](0004-sqlite-on-render.md) | SQLite in production, on purpose |
| [0005](0005-ports-to-rails-and-laravel.md) | The same domain, ported to Rails and Laravel |

> These are a student's decisions, taken while learning. Where a production system
> would choose differently, the ADR says so.

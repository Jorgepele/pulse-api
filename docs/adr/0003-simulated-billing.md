# 0003 — Billing is simulated; real Stripe is opt-in

**Status:** accepted · **Date:** 2026-07-06, extended 2026-07-09

## Context

Pulse is meant to look like a small SaaS, and a SaaS has plans and subscriptions. But a
public demo that anyone can click through cannot take real payments, and a portfolio
project should not require a reviewer to hold a Stripe account to see the flow work.

## Decision

Two paths, chosen by configuration rather than by branching in the frontend:

- **Default (no keys).** `SubscriptionView` writes a `Subscription` row with status
  `trialing`. No payment is taken. The demo shows the whole flow: pick a plan, become a
  subscriber, see it reflected in the UI.
- **With `STRIPE_SECRET_KEY` set.** `CheckoutView` creates a real Stripe Checkout session
  in test mode and returns its URL. Stripe calls `StripeWebhookView` when payment
  completes, and *that* is what activates the subscription. Without the key, `CheckoutView`
  answers `501 Not Implemented` and the simulated path stays in charge.

## Consequences

- The demo is self-contained and cannot be broken by an expired Stripe key.
- The real integration is written, reviewed and unit-tested with the Stripe SDK mocked
  (`billing/tests.py`), but **it has never run against Stripe's servers.** That is stated
  in `billing/BILLING.md` and it is worth repeating: tested is not the same as verified.
- The subscription is activated by the **webhook**, not by the browser returning to
  `success_url`. The browser can be closed, or lied to; the webhook is Stripe telling the
  server what happened. Its signature is verified against `STRIPE_WEBHOOK_SECRET`, because
  otherwise anyone who knows the URL could grant themselves a subscription.
- `SubscriptionView` subscribes `request.user.organizations.first()`. With one org per
  user that is fine; the day a user belongs to two, the endpoint needs to be told which.

---

**En una frase:** el billing por defecto es simulado para que la demo funcione sin claves,
y Stripe real se activa solo si existe `STRIPE_SECRET_KEY`; la suscripción la activa el
webhook (firmado), nunca la vuelta del navegador.

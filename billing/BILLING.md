# Billing: demo mode and real Stripe

Pulse has two billing modes. The public demo runs in **simulated** mode; the
code also supports **real Stripe Checkout** in test mode when you configure it.

> Honest note: the real Stripe path has unit tests (the Stripe SDK is mocked),
> but it has not been run against live Stripe from this project yet — that needs
> your own Stripe test keys. The steps below are what it takes to go live.

## Simulated mode (default)

With no Stripe keys set, `POST /api/billing/subscription/` records a
`Subscription` row (status `trialing`) without taking a payment. This is what
the deployed demo uses, so pricing and "subscribe" work with no Stripe account.

## Real Stripe Checkout (test mode)

When `STRIPE_SECRET_KEY` is set, two endpoints become useful:

- `POST /api/billing/checkout/` (auth) — body `{"plan": "<slug>"}`. Creates a
  Stripe Checkout session for the plan's price and returns `{"checkout_url": …}`.
  The client redirects the user there to pay.
- `POST /api/billing/webhook/` — Stripe calls this. On `checkout.session.completed`
  it marks the organization's subscription `active`. The request signature is
  verified with `STRIPE_WEBHOOK_SECRET`.

### Setup

1. Create a [Stripe](https://stripe.com) account and stay in **test mode**.
2. Create a product + recurring price for each paid plan. Copy each price id
   (`price_…`) into the matching `Plan.stripe_price_id` (via the Django admin).
3. Set environment variables:
   - `STRIPE_SECRET_KEY` — your test secret key (`sk_test_…`).
   - `STRIPE_WEBHOOK_SECRET` — the signing secret of the webhook (`whsec_…`).
   - `STRIPE_SUCCESS_URL` / `STRIPE_CANCEL_URL` — where Stripe returns the user
     (your frontend URLs).
4. Add a webhook endpoint in Stripe pointing at `…/api/billing/webhook/` and
   subscribe it to `checkout.session.completed`. For local testing, the
   [Stripe CLI](https://stripe.com/docs/stripe-cli) can forward events:
   `stripe listen --forward-to localhost:8000/api/billing/webhook/`.
5. Use a [test card](https://stripe.com/docs/testing) (e.g. `4242 4242 4242 4242`).

### Tests

```bash
python manage.py test billing
```

The Stripe tests mock the SDK (`stripe.checkout.Session.create` and
`stripe.Webhook.construct_event`), so they run offline and need no keys.

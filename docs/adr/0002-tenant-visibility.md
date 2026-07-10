# 0002 — One queryset defines what a tenant can see

**Status:** accepted · **Date:** 2026-07-10

## Context

Pulse is multi-tenant: an organization owns boards, which own posts, which own votes and
comments. For a while "multi-tenant" only meant that the `organization` foreign key
existed. Nothing enforced it. `BoardViewSet` listed `Board.objects.all()`, the
`is_public` flag was serialized but never read, and any caller — including an anonymous
one — could read every private board of every organization. Writes were as open: the
serializers accepted any `organization`, `board` or `post` id you sent them.

Scattering `if user in board.organization.members` checks across views and serializers
would have worked, and would have been forgotten in exactly one place.

## Decision

The rule lives in a single queryset method, `BoardQuerySet.visible_to(user)`:

> A board is visible if it is **public**, or if the user **belongs to the organization**
> that owns it.

Everything else derives from it. Posts and comments are filtered by
`board__in=Board.objects.visible_to(user)`. The serializers validate writes against the
same queryset. Boards can only be created inside an organization you are a member of.

Posting and commenting on a *public* board stays open to any signed-in user: Pulse is a
public roadmap in the style of Canny, and that is the product.

## Consequences

- One place to read, one place to change, one place to get wrong. Reviewing tenant
  isolation means reading nine lines.
- Every post and comment query carries a subquery over boards. On SQLite at this size it
  does not matter; at scale you would denormalize `organization_id` onto `Post`.
- On reads, an invisible board or post is a **404, not a 403**. This is deliberate: a 403
  confirms the resource exists, which leaks the thing we are trying to hide. On writes,
  DRF turns the serializer's rejection into a 400, whose message ("This board does not
  exist.") is worded not to confirm anything either.
- The membership join means `visible_to` needs `.distinct()`, and a distinct queryset
  under pagination needs an explicit ordering — hence `Board.Meta.ordering`.

The same rule is ported to `pulse-rails` (`Board.visible_to` scope) and `pulse-laravel`
(`Board::scopeVisibleTo`), so the three implementations can be compared side by side.

---

**En una frase:** la regla de visibilidad entre tenants vive en un único queryset del que
cuelga todo lo demás; devolvemos 404 y no 403 para no confirmar que el recurso existe.

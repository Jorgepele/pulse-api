# 0005 — The same domain, ported to Rails and Laravel

**Status:** accepted · **Date:** 2026-07-08

## Context

Pulse exists as a portfolio. The job it is applying to asks for Django, Rails and Laravel,
among others. The tempting move is three unrelated toy apps, one per framework, each
shallow enough to hide that the author has never used two of them.

## Decision

Build the domain **once**, properly, in Django (`pulse-api`), and then port the same
domain to Rails (`pulse-rails`) and Laravel (`pulse-laravel`): the same entities
(Organization, Membership, Board, Post, Vote, Comment), the same token auth, the same
vote-toggle semantics, the same tenant visibility rule, the same JSON shapes.

The ports deliberately **do not** include billing. Porting Stripe three times would teach
nothing that porting the domain does not already teach.

## Consequences

- The three repos are directly comparable. The same `visible_to` rule reads as a Django
  `QuerySet` method, a Rails `scope` and an Eloquent local scope; the same N+1 fix is
  `annotate`, `includes` and `withCount`. That comparison is the actual content.
- What the ports demonstrate is that **MVC maps across ecosystems**, and that I can read a
  framework's conventions well enough to express a known design in it. They do **not**
  demonstrate Rails or Laravel experience, and the READMEs must not imply otherwise.
- Three implementations means three test suites and three CI pipelines to keep green, and
  every domain change has to be made three times — as this ADR's own `visible_to` rule was.
- Convention over configuration becomes visible rather than theoretical: Rails infers the
  join table and the foreign keys, Django wants them spelled out, Laravel sits in between.

---

**En una frase:** un solo dominio portado a tres frameworks para poder compararlos de
verdad; demuestra que MVC se traslada entre ecosistemas, no que domine Rails o Laravel.

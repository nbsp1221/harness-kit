---
title: gstack
repo: https://github.com/garrytan/gstack
source_repo: https://github.com/garrytan/gstack
source_ref: e23ff28
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
category: methodology-plugin
status: reviewed
last_reviewed: 2026-04-21
priority: high
fit_for_harness_kit: medium
host_focus:
  - claude-code
  - codex
---

# gstack

## Summary

In this first research pass, `gstack` looks like a full role-based engineering operating system with a browser harness, learning logs, dashboards, and host-aware setup. It is not a minimal starter. For `harness-kit`, its value lies in staged routing, durable state, and persistent learning patterns rather than in copying the full surface.

## Why It Matters

- It is a highly visible public harness project in the current ecosystem.
- It shows how far role decomposition and persistent state can go before a harness becomes strongly opinionated.
- It offers valuable review, QA, release, browser, and learning patterns even if `harness-kit` does not adopt the full operating model.

## Snapshot

- Repository: `garrytan/gstack`
- Source ref: `e23ff28`
- Primary positioning: role-based engineering OS and browser-integrated harness
- Host focus: Claude Code first, with host detection and Codex-related compatibility
- Approximate scale: large public project with high community visibility
- Maintenance signal: high
- Install surface: setup script, symlinked skills, host-aware bootstrap, browser services

## Core Thesis

The harness should behave like an engineering organization, not a single prompt. Specialized roles, staged routing, persistent state, and durable learnings improve execution quality and continuity across sessions.

## Architecture

Important architectural areas:

- `README.md`, `AGENTS.md`, `CLAUDE.md`, and `ARCHITECTURE.md` define the overall operating model
- `BROWSER.md` defines the browser harness and daemon layer
- role and stage surfaces live in skill directories such as `autoplan/`, `review/`, `qa/`, and `ship/`
- setup and bootstrap behavior live in `setup` and `bin/*`
- learning and history surfaces live in `learn/` and learning-related scripts under `bin/`

## Workflow Model

The workflow model is staged, re-entrant, and route-driven.

Observed core stages:

- planning and planning review
- implementation and routing
- code review
- QA
- ship and deployment
- learn and state capture

The lesson for `harness-kit` is not “create many roles,” but “make stage boundaries explicit and persistent.”

## Bootstrap Model

Bootstrap is stateful and adaptive.

Observed characteristics:

- setup builds and symlinks skills
- host type is detected
- naming and routing are configured
- first-run prompts and onboarding behavior are injected
- browser and related helper services are part of the broader environment

For `harness-kit`, the durable lesson is to make bootstrap deterministic and host-aware, but probably quieter and smaller than gstack's full onboarding ceremony.

## Verification And Control

The control model is first-class and concrete.

Observed strengths:

- persistent browser daemon
- bearer-token auth and ref-based selection for browser interaction
- layered prompt-injection defense
- explicit QA and ship stages
- durable state logs for learnings, timeline, and checkpoints

This is a strong control-plane reference in the target set, but it is also one of the broadest.

## Memory And Compounding

Memory and compounding are concrete, not just aspirational.

Observed patterns:

- append-only learnings
- timeline and checkpoint logging
- searchable learning history
- session intelligence design docs

This is a clear reference for durable, file-backed or log-backed learning in the target set.

## Strengths

- Strong role separation and stage routing
- Good source for QA, release, and browser-integrated verification patterns
- Durable learning and timeline patterns are stronger than in many methodology-first repos
- Good source for studying "thin harness, fat skills" in practice

## Weaknesses

- Much broader than a lean internal starter
- Role count and browser surface may exceed what `harness-kit` needs
- First-run prompts and telemetry nudges could add friction if copied directly
- Browser and security surface introduce extra operational weight

## What To Steal

- stage-specific routing and verification gates
- deterministic host-aware bootstrap
- persistent learnings, timeline, and checkpoint persistence
- selected QA, ship, and review patterns

## What Not To Steal

- full browser and security surface in v1 unless truly needed
- first-run prompt stack and proactive nudges for a minimal local starter
- the entire role catalog as a default harness surface

## Open Questions

- Which 20 percent of gstack creates 80 percent of the value for a smaller starter?
- Does `harness-kit` want durable cross-session state at gstack's level, or only a lighter learning log?
- How much of the browser surface is essential versus productized convenience?

## Evidence

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `ARCHITECTURE.md`
- `BROWSER.md`
- `autoplan/SKILL.md`
- `review/SKILL.md`
- `qa/SKILL.md`
- `ship/SKILL.md`
- `setup`
- `bin/dev-setup`
- `bin/gstack-update-check`
- `learn/SKILL.md`
- `bin/gstack-learnings-log`
- `bin/gstack-learnings-search`
- `docs/designs/SELF_LEARNING_V0.md`
- `docs/designs/SESSION_INTELLIGENCE.md`

---
title: target-name
repo: https://github.com/example/example
source_repo: https://github.com/example/example
source_ref: abc1234
capture_date: YYYY-MM-DD
source_pass: 2026-04-21-deep-pass
status: draft
depth: dossier
---

# Target Name Dossier

## Executive Summary

Write the shortest possible summary that still lets a future reader recover the big picture.

## Repository Positioning

- What the project claims to be
- What it appears to be in practice
- Where it sits in the harness landscape
- Why it matters to `harness-kit`

## Source Snapshot

- Source repo:
- Source ref:
- Capture date:
- Host focus:
- Primary languages:
- Install surfaces:

## Install And Bootstrap Trace

Reconstruct the path from clone/install to first usable run.

Include:

- install entry points
- setup scripts
- generated files
- user-global changes
- repo-local changes
- first-run assumptions

## Artifact Inventory

List important generated or owned artifacts.

Suggested shape:

| Artifact | Scope | Producer | Purpose | Notes |
|---|---|---|---|---|

## Architecture Map

Document the major architectural areas and their responsibilities.

Suggested shape:

| Area | Key paths | Responsibility | Why it matters |
|---|---|---|---|

## Workflow Surface

Document the actual user-facing workflow surface:

- commands
- skills
- hooks
- workflows
- agents
- tasks
- dashboards or UI

## State, Memory, And Compounding

Explain:

- what state exists
- where it lives
- how it is updated
- how it is resumed
- how learnings compound over time

## Verification, Permissions, And Recovery

Explain:

- quality gates
- permission model
- safety checks
- failure recovery
- cleanup or migration behavior

## Code Hotspots

List the code paths a future reader should inspect first.

Suggested shape:

| File | Why it matters | Key concept |
|---|---|---|

## Design Lessons For Harness Kit

### What To Steal

- ...

### What Not To Steal

- ...

### Unclear Or Conditional Lessons

- ...

## Open Questions

- ...

## Evidence Map

Use repo-relative paths, not ephemeral local paths.

Include enough evidence that a future reader can quickly re-open the upstream code and verify claims.

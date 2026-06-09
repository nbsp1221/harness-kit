---
title: OpenHarness
repo: https://github.com/HKUDS/OpenHarness
source_repo: https://github.com/HKUDS/OpenHarness
source_ref: 4dd7b76
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
category: runtime-platform
status: reviewed
last_reviewed: 2026-04-21
priority: medium
fit_for_harness_kit: medium
host_focus:
  - multi-host
---

# OpenHarness

## Summary

In this first research pass, `OpenHarness` looks closer to a general open runtime substrate than a lean project starter. It matters because it exposes a broad architecture surface around permissions, hooks, memory, tasks, profiles, and coordination. The right use of this benchmark is to learn platform boundaries and selectively borrow local durability and safety patterns.

## Why It Matters

- It shows what a more complete open harness platform can look like.
- It offers useful ideas for permissions, lifecycle hooks, profiles, and markdown-first memory.
- It is also a boundary marker for what `wayrail` should probably not become in v1.

## Snapshot

- Repository: `HKUDS/OpenHarness`
- Source ref: `4dd7b76`
- Primary positioning: core harness layer with `ohmo` built on top
- Host focus: multi-host and open harness compatibility
- Approximate scale: active public project
- Maintenance signal: medium to high
- Install surface: Python package, CLI startup, and broader runtime setup

## Core Thesis

The harness is the runtime around the model: profiles, auth, permissions, hooks, memory, tasks, and orchestration. The repo explicitly separates the core harness layer from product-specific opinion on top of it.

## Architecture

Important architectural areas:

- `README.md` defines the harness framing
- `ohmo/**` shows the product or user-facing layer on top of the harness
- `src/openharness/config/**` defines profile, auth, and settings behavior
- `src/openharness/permissions/**` and `src/openharness/hooks/**` define control and safety
- `src/openharness/memory/**` and `src/openharness/services/session_storage.py` define persistence
- `src/openharness/tasks/**` and `src/openharness/coordinator/**` define coordination

## Workflow Model

The repo is more runtime substrate than prescriptive development loop.

The main workflow lesson is structural:

- bootstrap and runtime are separate phases
- provider choice is treated as workflow choice
- coordination and tasks exist as reusable primitives rather than only as commands

This makes OpenHarness more useful as an architecture reference than as a direct template for `wayrail`'s lifecycle.

## Bootstrap Model

Bootstrap and runtime are deliberately separated.

Observed patterns:

- workflow or profile setup with one active profile
- explicit auth and model specialization
- runtime startup after setup
- separation between setup-time workspace logic and runtime execution

This is useful because `wayrail` will likely need a clean boundary between project bootstrap and ongoing execution.

## Verification And Control

The clearest safety story in this pass is at tool-execution time, not at the UI layer.

Observed mechanisms:

- hard path denies
- permission modes
- pre and post hook execution
- user prompts around risky actions

The ordering matters. `wayrail` should copy “tool gate first” rather than over-invest in outer presentation.

## Memory And Compounding

Persistent memory is markdown-first and compounding state is intentionally serialized.

Observed patterns:

- memory files and paths
- manager and memdir abstractions
- session storage carrying state forward

This is useful because it gives `wayrail` a low-friction durability model without requiring a database or opaque blob store.

## Strengths

- Broad architecture coverage
- Useful source for runtime control and permissions ideas
- Good profile and auth separation
- Good markdown-first memory patterns

## Weaknesses

- Larger scope than `wayrail` likely needs
- Better to learn from than to copy directly
- Claude-shaped coordination details may not generalize
- Duplicate state stores could become accidental complexity if copied without care

## What To Steal

- profile-backed setup with one active profile
- markdown memory files plus a small index
- tool-gated permissions with pre and post hooks
- background tasks with output logs and status

## What Not To Steal

- legacy compatibility layers unless truly needed
- Claude-specific coordinator markers and XML task notifications
- duplicate state stores across workspace, session, config, and memory unless the separation is intentional
- shell-command hooks as the default extension mechanism for everything

## Open Questions

- Does `wayrail` need background task primitives in v1?
- Which pieces of OpenHarness are substrate and which are product-specific opinion?
- Are the observed session restore and compaction patterns reusable without the broader runtime?

## Evidence

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `ohmo/workspace.py`
- `ohmo/cli.py`
- `ohmo/runtime.py`
- `src/openharness/config/settings.py`
- `src/openharness/cli.py`
- `src/openharness/permissions/checker.py`
- `src/openharness/engine/query.py`
- `src/openharness/hooks/executor.py`
- `src/openharness/commands/registry.py`
- `src/openharness/memory/paths.py`
- `src/openharness/memory/manager.py`
- `src/openharness/memory/memdir.py`
- `src/openharness/services/session_storage.py`
- `src/openharness/coordinator/coordinator_mode.py`
- `src/openharness/tasks/manager.py`
- `src/openharness/prompts/context.py`

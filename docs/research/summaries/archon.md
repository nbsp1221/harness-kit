---
title: Archon
repo: https://github.com/coleam00/Archon
source_repo: https://github.com/coleam00/Archon
source_ref: 7ea3214
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
category: workflow-engine
status: reviewed
last_reviewed: 2026-04-21
priority: high
fit_for_harness_kit: high
host_focus:
  - codex
  - claude-code
---

# Archon

## Summary

In this first research pass, `Archon` looks like the best workflow-engine benchmark in the target set. It treats harness engineering as deterministic, YAML-defined workflow execution with validation, approvals, resume semantics, and explicit lifecycle operations. It is broader than `harness-kit` v1, but very valuable as a design reference.

## Why It Matters

- `harness-kit` cares about standardized startup and predictable execution.
- Archon encodes workflows as durable artifacts instead of prompt habits.
- It is the best benchmark for understanding where a starter ends and a workflow engine begins.

## Snapshot

- Repository: `coleam00/Archon`
- Source ref: `7ea3214`
- Primary positioning: workflow engine and harness builder for AI coding
- Host focus: multiple coding agents
- Approximate scale: significant and active public project
- Maintenance signal: high
- Install surface: CLI, config overlays, workflows, and broader platform components

## Core Thesis

Agent work becomes reliable when workflows, transitions, and execution context are encoded as deterministic configuration instead of left to conversational drift.

## Architecture

Important architectural areas:

- `README.md` and `CLAUDE.md` establish the workflow-engine framing
- `packages/workflows/**` implements YAML loading, validation, discovery, storage, and run semantics
- `packages/core/**` handles orchestration and lifecycle operations
- `packages/server/**` exposes workflow lifecycle endpoints
- `scripts/install.sh` and `scripts/validate-setup.sh` show install and validation expectations
- `migrations/**` shows the persistence model for runs, sessions, history, and codebase state

## Workflow Model

The workflow model is declarative YAML DAG execution with loops, approvals, validation, and resume semantics.

Important takeaways:

- workflows are authored as explicit graphs
- transitions are validated before execution
- run state is durable
- resume semantics are part of the design, not an afterthought

If `harness-kit` wants a reliable workflow control plane later, this is the best benchmark in the current set to learn from.

## Bootstrap Model

Bootstrap and configuration use a three-layer precedence model:

- bundled defaults
- home-scoped globals
- repo-local overrides

This is one of Archon's most relevant ideas for `harness-kit`, because it shows how to preserve reusable defaults without losing repository ownership.

## Verification And Control

Control is strict:

- workflow definitions are parsed and validated before save or execution
- lifecycle endpoints gate resume and abandon explicitly
- node types like prompt, bash, command, loop, and approval are first-class

This is a much better benchmark for deterministic control than an ad hoc prompt router.

## Memory And Compounding

Memory and state are database-backed and designed for resume, audit, and per-codebase execution history.

Observed patterns:

- workflow run storage
- immutable sessions
- message history
- codebase-scoped environment configuration

This is powerful, but materially heavier than a file-backed local starter.

## Strengths

- Strongest model for explicit state transitions in the target set
- Excellent source for deterministic workflow thinking
- Overlay precedence model is directly reusable
- Resume and validation semantics are clearer than in most prompt-driven systems

## Weaknesses

- Heavier than a lean starter
- Database and server architecture may be premature for `harness-kit` v1
- Broad adapter and platform surface can obscure the core lessons if copied too literally

## What To Steal

- YAML DAG workflows with first-class node types
- bundled < global < project precedence
- validate-before-save and resume-from-completed-node semantics
- explicit lifecycle controls rather than vague conversational state

## What Not To Steal

- database-heavy architecture unless truly needed
- broad platform and adapter complexity before the local workflow contract is proven
- configuration sprawl without a narrow schema and precedence rules

## Open Questions

- Should `harness-kit` mirror Archon's global overlay model or stay repo-scoped only in v1?
- Does `harness-kit` need a workflow engine core later, or only a lighter starter layer?
- Which parts of Archon's surface are essential benchmark material versus unrelated product scope?

## Evidence

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `CLAUDE.md`
- `scripts/install.sh`
- `scripts/validate-setup.sh`
- `packages/workflows/src/schemas/workflow.ts`
- `packages/workflows/src/loader.ts`
- `packages/workflows/src/workflow-discovery.ts`
- `packages/workflows/src/store.ts`
- `packages/workflows/src/schemas/workflow-run.ts`
- `packages/workflows/src/validator.ts`
- `packages/core/src/orchestrator/orchestrator.ts`
- `packages/core/src/operations/workflow-operations.ts`
- `packages/server/src/routes/api.ts`
- `packages/server/src/routes/api.workflows.test.ts`
- `migrations/001_initial_schema.sql`
- `migrations/008_workflow_runs.sql`
- `migrations/010_immutable_sessions.sql`
- `migrations/014_message_history.sql`
- `migrations/020_codebase_env_vars.sql`

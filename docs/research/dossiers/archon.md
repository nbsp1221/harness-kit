---
title: archon
repo: https://github.com/coleam00/Archon
source_repo: https://github.com/coleam00/Archon
source_ref: 7ea3214
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
status: reviewed
depth: dossier
---

# Archon Dossier

## Executive Summary

`Archon` is the clearest workflow-engine benchmark in the current research set. It is broader than `wayrail` v1, but it provides the best reference for:

- declarative workflow artifacts
- config precedence
- validation-before-execution
- durable run and event state
- lifecycle operations such as resume, approval, and cleanup

For `wayrail`, the most reusable ideas are:

- bundled < global < project precedence
- DAG workflow structure
- explicit lifecycle controls
- resumable execution semantics

The least reusable parts for v1 are:

- database-backed runtime history
- server and web surface
- multi-platform adapter breadth

## Repository Positioning

Archon is not a prompt methodology repo. It is a workflow engine and harness builder.

That means it exists at a different layer from:

- `compound-engineering-plugin`
- `superpowers`

Its value to `wayrail` is therefore architectural rather than stylistic.

It answers questions like:

- how do workflows become durable artifacts?
- how do different scopes override each other?
- how is resume made deterministic?
- how do we avoid overlapping writes into the same worktree or path?

## Source Snapshot

- Source repo: `https://github.com/coleam00/Archon`
- Source ref: `7ea3214`
- Capture date: `2026-04-21`
- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- Host focus: multiple coding agents
- Primary languages: TypeScript, SQL, shell, docs
- Install surfaces: source install, shell installer, Homebrew, Docker, binary install

## Install And Bootstrap Trace

Archon has two big install categories.

### Source Install

Observed flow:

1. clone repo
2. install dependencies with Bun
3. run setup or environment provisioning
4. use CLI or web surfaces

### Binary / Quick Install

Observed flow:

1. platform-aware download
2. checksum verification
3. install into configured directory
4. initialize runtime environment

### Env Bootstrap

Before command dispatch:

- `~/.archon/.env` can load
- `<cwd>/.archon/.env` can load
- providers are registered

This means Archon’s runtime contract starts before workflow execution. Configuration precedence is part of bootstrap, not an afterthought.

### Setup Writes

The setup path intentionally writes:

- Archon-owned env files
- not the raw repo `.env`

This is an important boundary lesson for `wayrail`.

## Artifact Inventory

| Artifact | Scope | Producer | Purpose | Notes |
|---|---|---|---|---|
| `.archon/workflows/` | user or repo | workflow authoring | custom workflow definitions | precedence-sensitive |
| `.archon/commands/` | user or repo | command authoring | custom commands | workflow-adjacent |
| bundled default workflows | packaged defaults | build/generation | default workflow catalog | lower precedence |
| generated bundled defaults | build artifact | generation script | compiled-in defaults | bootstrap convenience |
| workflow runs table | DB | runtime | run lifecycle state | durable execution history |
| workflow events table | DB | runtime | resumable node events | event memory |
| immutable sessions table | DB | runtime | session audit trail | lifecycle history |
| codebase env vars table | DB | runtime | per-codebase env injection | scoped config |
| isolation environments table | DB | runtime | worktree ownership ledger | cleanup safety |
| installer scripts | distribution | release tooling | bootstrap to machine | multiple paths |
| homebrew formula | distribution | release tooling | brew install | binary install path |
| Docker and deploy files | distribution/runtime | repo | containerized launch | broader platform story |

## Architecture Map

| Area | Key paths | Responsibility | Why it matters |
|---|---|---|---|
| CLI bootstrap | `packages/cli/src/cli.ts` | env loading, provider registration, dispatch | process entry |
| CLI commands | `packages/cli/src/commands/*` | workflow, isolation, setup, other commands | operator surface |
| workflow schemas | `packages/workflows/src/schemas/*` | typed workflow and run models | durable artifact shape |
| workflow loader | `packages/workflows/src/loader.ts` | YAML parsing and DAG validation | correctness gate |
| workflow discovery | `packages/workflows/src/workflow-discovery.ts` | bundled/global/project precedence | config policy |
| workflow store | `packages/workflows/src/store.ts` | run and event persistence interface | lifecycle durability |
| executor | `packages/workflows/src/executor.ts` | run orchestration and resume | runtime engine |
| DAG executor | `packages/workflows/src/dag-executor.ts` | node execution and approval pause | node-level control |
| persistence layer | `packages/core/src/db/*` | DB writes and run state | durable runtime contract |
| cleanup service | `packages/core/src/services/cleanup-service.ts` | safe teardown | destructive guard |
| server | `packages/server/src/*` | API surface | non-CLI access |
| web | `packages/web/src/*` | UI surface | operator experience |

## Workflow Surface

### CLI Surface

Observed capabilities include:

- list workflows
- run workflows
- resume workflows
- approve or reject workflows
- manage isolation
- configure setup

This means the workflow engine is directly controllable without the web UI.

### Web and Adapter Surface

Archon also exposes workflow surfaces through:

- web
- GitHub
- Slack
- Telegram
- Discord

This breadth is not needed for `wayrail` v1, but it shows the advantage of durable workflow artifacts: many surfaces can reuse them.

### Workflow Discovery

Workflow selection is filesystem-driven and precedence-driven.

That means:

- same-name overrides are meaningful
- repo-local workflows can supersede shared defaults
- configuration is legible because it is file-based

## State, Memory, And Compounding

Archon’s memory model is operational rather than note-like.

### Run Lifecycle State

Stored state includes:

- workflow status
- current step index
- metadata
- timestamps
- working path

This is a strong example of durable workflow execution state.

### Event Memory

The event table stores:

- node completions
- resume-relevant outputs
- UI-relevant history

This is important because resume depends on event replay, not just on top-level workflow status.

### Isolation and Session Linkage

State is not only about workflows. It is also about:

- worktree ownership
- isolation environment lifecycle
- conversation linkage
- codebase-scoped env injection

That makes Archon a serious runtime system, not just a workflow DSL.

## Verification, Permissions, And Recovery

Archon’s control surfaces are among the clearest in the set.

### Validation Before Execution

`loader.ts` rejects:

- malformed workflows
- duplicate node IDs
- unknown references
- cycles
- legacy incompatible shapes

This is exactly the kind of hard gate `wayrail` should imitate conceptually.

### Path and Isolation Safety

Execution uses:

- working-path locks
- isolation environment tracking
- stale-pending detection
- safe cleanup checks

This matters because compounding state is expensive to corrupt.

### Recovery

Recovery includes:

- resumable run lookup
- event replay
- approval pause and resume
- explicit abandon paths

This is far beyond v1 scope for `wayrail`, but still an excellent reference.

## Code Hotspots

| File | Why it matters | Key concept |
|---|---|---|
| `packages/cli/src/cli.ts` | first bootstrap sequence | env and provider precedence |
| `packages/cli/src/commands/setup.ts` | setup-owned env writes | bootstrap boundary |
| `packages/workflows/src/workflow-discovery.ts` | precedence and override logic | bundled < global < project |
| `packages/workflows/src/loader.ts` | workflow parsing and DAG validation | preflight correctness |
| `packages/workflows/src/executor.ts` | run orchestration and path locking | lifecycle control |
| `packages/workflows/src/dag-executor.ts` | node execution, approval, loop resume | durable progress |
| `packages/workflows/src/store.ts` | run and event storage bridge | persistent run state |
| `packages/core/src/db/workflows.ts` | run-state DB contract | resumable execution |
| `packages/core/src/db/workflow-events.ts` | event persistence | replayable compounding state |
| `packages/core/src/db/isolation-environments.ts` | worktree ledger | cleanup and ownership |
| `packages/core/src/services/cleanup-service.ts` | safe teardown | destructive guard |
| `migrations/008_workflow_runs.sql` | workflow run schema | persisted lifecycle |
| `migrations/012_workflow_events.sql` | event schema | replay support |
| `migrations/020_codebase_env_vars.sql` | per-codebase env schema | scoped runtime config |

## Design Lessons For Wayrail

### What To Steal

- bundled < global < project precedence
- explicit workflow artifacts instead of hidden conversational routing
- validate-before-run discipline
- path and isolation guards
- resumable lifecycle as a future direction

### What Not To Steal

- DB-backed runtime in v1
- broad multi-surface platform before the starter contract is proven
- too much adapter breadth before the core local workflow model exists

### Unclear Or Conditional Lessons

- a lighter local workflow artifact system may be enough for `wayrail`
- some lifecycle operations like resume and rerun may belong in v2 or later

## Open Questions

- How much of Archon’s power depends on the DB versus the workflow model itself?
- What is the minimum viable subset of its precedence model for a starter?
- Does `wayrail` need named workflow nodes at all in v1?

## Appendix A: Structure Pass Notes

### Install / Bootstrap

- source setup and quick install are separate
- env bootstrap occurs before command dispatch
- setup writes Archon-owned env files rather than app `.env`

### Artifact Inventory

- workflow and command definitions
- durable persistence schema
- packaging and deployment surfaces

### Architecture Map

- CLI bootstrap and command router
- workflow engine
- persistence and cleanup
- isolation and platform adapters

### Workflow Surface

- CLI workflow controls
- web and external platform surfaces
- deterministic discovery and routing

### State / Memory

- run lifecycle and resumption
- event memory
- isolation/session linkage
- per-codebase env injection

## Appendix B: Code Hotspot Notes

### Bootstrap Hotspots

- `packages/cli/src/cli.ts`
- `packages/cli/src/commands/setup.ts`

### Workflow Engine Hotspots

- `packages/workflows/src/workflow-discovery.ts`
- `packages/workflows/src/loader.ts`
- `packages/workflows/src/executor.ts`
- `packages/workflows/src/dag-executor.ts`
- `packages/workflows/src/store.ts`

### Persistence / Control Hotspots

- `packages/core/src/db/workflows.ts`
- `packages/core/src/db/workflow-events.ts`
- `packages/core/src/db/isolation-environments.ts`
- `packages/core/src/services/cleanup-service.ts`
- `migrations/008_workflow_runs.sql`
- `migrations/012_workflow_events.sql`
- `migrations/020_codebase_env_vars.sql`

## Appendix C: Detailed Bootstrap Notes

### Install Variety

Archon supports:

- source install
- shell installer
- binary install
- Homebrew
- Docker-adjacent deployment

This breadth is not relevant to `wayrail` v1 directly, but it does show how a workflow engine grows once it becomes a platform.

### Config Precedence As Bootstrap

The most important bootstrap lesson is not the installer itself. It is the order:

- bundled defaults
- home-scoped overrides
- repo-local overrides
- env loading before dispatch

This is the real “setup contract.”

### Why Archon-Owned Env Matters

Setup writes `.archon/.env`, not the app’s own `.env`.

That is a strong pattern:

- harness state should be owned by the harness
- app state should be owned by the app

## Appendix D: Detailed File Role Notes

- `packages/cli/src/cli.ts`
  Process entry and env/provider bootstrap.
- `packages/cli/src/commands/setup.ts`
  Harness-owned env writer.
- `packages/cli/src/commands/workflow.ts`
  CLI workflow operations.
- `packages/cli/src/commands/isolation.ts`
  Worktree/isolation operations.
- `packages/workflows/src/workflow-discovery.ts`
  Precedence and override logic.
- `packages/workflows/src/loader.ts`
  YAML parser and DAG validation.
- `packages/workflows/src/executor.ts`
  Run orchestration and path locking.
- `packages/workflows/src/dag-executor.ts`
  Node execution and pause/resume semantics.
- `packages/workflows/src/store.ts`
  Run/event persistence bridge.
- `packages/workflows/src/router.ts`
  Workflow selection and dispatch support.
- `packages/core/src/db/workflows.ts`
  Persistent run contract.
- `packages/core/src/db/workflow-events.ts`
  Replayable event memory.
- `packages/core/src/db/isolation-environments.ts`
  Worktree ownership ledger.
- `packages/core/src/db/conversations.ts`
  Session linkage.
- `packages/core/src/services/cleanup-service.ts`
  Safe destructive cleanup.
- `migrations/008_workflow_runs.sql`
  Run schema.
- `migrations/012_workflow_events.sql`
  Event schema.
- `migrations/020_codebase_env_vars.sql`
  Per-codebase env schema.

## Appendix E: Why Archon Is Still Different From A Starter

Archon is useful because it cleanly shows where a starter ends and a workflow platform begins.

Starter responsibilities:

- bootstrap
- contracts
- defaults
- validation expectations

Archon responsibilities:

- persistent workflow runs
- event replay
- path locking
- isolation ledgers
- UI and API surfaces

This distinction is important because it keeps `wayrail` from drifting into platform scope too early.

## Appendix F: High-Yield Follow-Up Questions

- Which subset of node types would actually matter for `wayrail` if it ever gained workflow artifacts?
- How much of the resume logic depends on the DB, and how much depends only on the workflow graph plus event log?
- Does `wayrail` need named workflow runs at all, or only step/checkpoint artifacts?
- Which cleanup guarantees are most worth copying before any workflow engine exists?
- What is the smallest precedence model that still captures the useful part of bundled < global < project?

## Appendix G: Minimal Archon Slice For Wayrail

If `wayrail` only copied the smallest useful Archon slice, it would likely include:

- precedence rules
- validation-before-run discipline
- workflow artifact thinking
- path-lock and cleanup caution as design principles

## Evidence Map

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `CLAUDE.md`
- `scripts/install.sh`
- `package.json`
- `packages/cli/src/cli.ts`
- `packages/cli/src/commands/setup.ts`
- `packages/cli/src/commands/workflow.ts`
- `packages/cli/src/commands/isolation.ts`
- `packages/workflows/src/schemas/workflow.ts`
- `packages/workflows/src/schemas/workflow-run.ts`
- `packages/workflows/src/workflow-discovery.ts`
- `packages/workflows/src/loader.ts`
- `packages/workflows/src/store.ts`
- `packages/workflows/src/event-emitter.ts`
- `packages/workflows/src/executor.ts`
- `packages/workflows/src/dag-executor.ts`
- `packages/workflows/src/router.ts`
- `packages/core/src/db/workflows.ts`
- `packages/core/src/db/workflow-events.ts`
- `packages/core/src/db/isolation-environments.ts`
- `packages/core/src/db/conversations.ts`
- `packages/core/src/services/cleanup-service.ts`
- `packages/server/src/routes/api.ts`
- `packages/server/src/routes/api.workflows.test.ts`
- `migrations/001_initial_schema.sql`
- `migrations/008_workflow_runs.sql`
- `migrations/010_immutable_sessions.sql`
- `migrations/012_workflow_events.sql`
- `migrations/014_message_history.sql`
- `migrations/020_codebase_env_vars.sql`

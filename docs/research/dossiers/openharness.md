---
title: openharness
repo: https://github.com/HKUDS/OpenHarness
source_repo: https://github.com/HKUDS/OpenHarness
source_ref: 4dd7b76
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
status: reviewed
depth: dossier
---

# OpenHarness Dossier

## Executive Summary

`OpenHarness` is a runtime substrate more than a starter. It includes:

- Python CLI runtime
- React terminal UI
- permissions and hooks
- memory and compaction
- task and agent orchestration
- a separate long-lived `ohmo` personal-agent stack

For `wayrail`, the value is not in copying the whole platform. The value is in studying:

- profile and auth separation
- tool-gated control
- session persistence and compaction
- file-based memory
- the boundary between core harness and personal-agent layer

## Repository Positioning

OpenHarness is unusual in the target set because it explicitly separates:

- the core harness layer
- the `ohmo` layer built on top of it

This is a strong conceptual lesson. It suggests a clean split between:

- generic runtime substrate
- opinionated product or operator layer

That makes it valuable architecturally even when it is too broad for `wayrail` v1.

## Source Snapshot

- Source repo: `https://github.com/HKUDS/OpenHarness`
- Source ref: `4dd7b76`
- Capture date: `2026-04-21`
- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- Host focus: multi-host
- Primary languages: Python, TypeScript/React, shell, PowerShell
- Install surfaces: Python package install, curl/PowerShell installers, dev install, `ohmo` workspace bootstrap

## Install And Bootstrap Trace

OpenHarness has one of the broadest bootstrap surfaces in the set.

### Core CLI Install

Observed options:

- curl one-liner
- PowerShell one-liner
- editable dev installs
- package entrypoints like `oh`, `openh`, `openharness`

The install scripts:

- provision Python
- manage venvs
- install package
- link commands into PATH

### Frontend / React TUI Bootstrap

The React terminal is part of the real product surface, not just a demo.

Observed behavior:

- frontend lives under `frontend/terminal`
- Python runtime launches the React frontend
- frontend dependencies can install lazily at runtime if missing

This means bootstrap depends on:

- Python
- Node/npm
- runtime resolution of frontend assets

### `ohmo` Bootstrap

`ohmo` is not a tiny wrapper. It seeds:

- `BOOTSTRAP.md`
- `identity.md`
- `user.md`
- `soul.md`
- `memory/MEMORY.md`
- `state.json`
- `gateway.json`

under its own workspace root.

That means OpenHarness really has two boot sequences:

1. core harness install
2. personal-agent workspace initialization

## Artifact Inventory

| Artifact | Scope | Producer | Purpose | Notes |
|---|---|---|---|---|
| `src/openharness/*` | core runtime | source | CLI, engine, tools, commands, UI, memory, hooks, state, auth | primary harness surface |
| `frontend/terminal/*` | UI | source/runtime | React terminal | packaged interactive surface |
| `src/openharness/ui/backend_host.py` | UI backend | runtime | structured host for frontend | bridges React and Python |
| `src/openharness/services/session_storage.py` | persistence | runtime | latest/session JSON snapshots | durable conversation state |
| `src/openharness/services/compact/__init__.py` | compaction | runtime | memory condensation and checkpointing | compounding engine |
| `src/openharness/memory/*` | memory | runtime | memory paths, index, manager | file-based memory |
| `src/openharness/permissions/*` | control | runtime | path, command, tool permission checks | safety core |
| `src/openharness/hooks/*` | control | runtime | lifecycle hooks | enforcement surface |
| `src/openharness/tasks/*` | orchestration | runtime | background task execution | task subsystem |
| `src/openharness/tools/agent_tool.py` | orchestration | runtime | agent subprocess tool | delegation entry |
| `src/openharness/tools/task_create_tool.py` | orchestration | runtime | task subprocess tool | background task entry |
| `src/openharness/commands/registry.py` | UX surface | runtime | slash-command registration | user workflow API |
| `ohmo/*` | product layer | source/runtime | workspace, gateway, session, memory | second architecture |
| `scripts/install.sh` | bootstrap | distribution | Unix install | first-class install path |
| `scripts/install.ps1` | bootstrap | distribution | Windows install | first-class install path |
| `scripts/install_dev.sh` | bootstrap | dev workflow | editable development install | contributor path |
| `docs/SHOWCASE.md` | docs | source | real-world usage patterns | onboarding asset |

## Architecture Map

| Area | Key paths | Responsibility | Why it matters |
|---|---|---|---|
| entry and dispatch | `src/openharness/__main__.py`, `src/openharness/cli.py` | CLI entry | process start |
| UI launch | `src/openharness/ui/react_launcher.py`, `src/openharness/ui/backend_host.py`, `src/openharness/ui/runtime.py` | React TUI and backend | interactive control plane |
| query loop | `src/openharness/engine/query_engine.py`, `query.py`, `messages.py`, `stream_events.py` | tool and model loop | core runtime |
| tools | `src/openharness/tools/*` | shell tasks, agents, operations | active work surface |
| permissions | `src/openharness/permissions/*` | policy checks | hard control gate |
| hooks | `src/openharness/hooks/*` | lifecycle extensions | enforcement and automation |
| persistence | `src/openharness/services/session_storage.py`, `session_backend.py` | snapshots and restore | durable state |
| compaction | `src/openharness/services/compact/__init__.py` | condensation and carryover | compounding engine |
| memory | `src/openharness/memory/*` | file-based memory | durable knowledge |
| state | `src/openharness/state/*` | app/runtime state | observable configuration |
| tasks | `src/openharness/tasks/*` | background orchestration | async work |
| `ohmo` stack | `ohmo/workspace.py`, `runtime.py`, `gateway/*`, `session_storage.py` | long-lived personal-agent layer | second architecture |

## Workflow Surface

### Slash Commands

Observed slash-command registry includes:

- `/compact`
- `/memory`
- `/resume`
- `/session`
- `/tasks`
- `/agents`
- `/bridge`
- `/config`
- `/provider`
- `/model`
- `/theme`
- `/output-style`
- `/fast`
- `/effort`
- `/passes`
- `/turns`
- `/continue`
- `/autopilot`
- `/ship`

This is a strong sign that OpenHarness is a runtime product, not only a library.

### React TUI Interaction

The TUI can:

- open selection modals
- restore state
- surface task and bridge status
- reflect key runtime settings

This means the workflow is partly encoded in interactive UI state, not only in commands.

### Background Tasks And Delegation

OpenHarness includes:

- background shell tasks
- local agent subprocesses
- task manager
- command registry integrations for task and agent control

This is far beyond `wayrail` v1 scope, but it is useful as a model of what a mature runtime can own.

### `ohmo` Gateway Workflows

`ohmo` maps chat messages to:

- per-session runtimes
- session-key bundle reuse
- `/stop`
- `/restart`

This makes `ohmo` a genuine conversational runtime on top of OpenHarness, not just branding.

## State, Memory, And Compounding

This is the deepest part of the repo.

### UI and Session State

Observed state includes:

- model
- provider
- auth
- permission mode
- fast mode
- effort
- passes
- MCP counts
- bridge sessions
- output style
- keybindings

This is not just app settings. It is live runtime state.

### Session Persistence

Snapshots persist:

- messages
- usage
- system prompt
- summary
- selective tool metadata

with:

- `latest.json`
- `session-<id>.json`

restore paths.

### Compaction Engine

OpenHarness does real compaction, not just “summaries.”

Observed compounding mechanisms:

- microcompact
- context collapse
- session-memory condensation
- checkpoint metadata
- carryover of task focus state and verified work

This is one of the strongest substrate-level compounding designs in the benchmark set.

At the current dossier depth, the compaction flow can be summarized as:

1. query loop updates carryover metadata
2. compaction service condenses context and preserves checkpoint-like state
3. session persistence stores resumable artifacts and summaries

### File-Based Memory

Memory is:

- file-based
- hashed per project/workspace
- injected via `MEMORY.md`

This is especially relevant to `wayrail`, because it shows a path between:

- no memory
- and a heavy DB-backed memory service

### `ohmo` Continuity

`ohmo` adds:

- workspace identity
- user profile
- session history
- session-key-scoped latest snapshots
- gateway state

under `.ohmo`.

This makes `ohmo` a rich continuity layer.

Known gap at the current dossier depth:

- the exact ownership boundary between core-harness compaction artifacts and `ohmo` continuity artifacts is still partially reconstructed rather than fully enumerated

## Verification, Permissions, And Recovery

OpenHarness places control at tool execution time.

### Permission and Hook Layer

Observed:

- hard path denies
- policy checks on tool/path/command
- hooks with block-on-failure semantics

This ordering is important. It means the repo trusts inner control points more than outer UX.

### Query Loop Persistence

The query loop itself updates carryover metadata:

- goals
- read files
- verified work
- skills
- async agents
- plan mode

before model execution continues.

This is how ephemeral work becomes durable state.

### Recovery

Recovery exists at multiple layers:

- session restore
- compaction checkpoints
- UI runtime bundle restore
- `ohmo` gateway runtime reuse

This is powerful, but also far heavier than a starter.

## Code Hotspots

| File | Why it matters | Key concept |
|---|---|---|
| `scripts/install.sh` | Unix install bootstrap | machine provisioning |
| `scripts/install.ps1` | Windows install bootstrap | machine provisioning |
| `src/openharness/ui/react_launcher.py` | lazy frontend setup and launch | runtime bootstrap fallback |
| `src/openharness/config/settings.py` | profile and settings loading | active profile model |
| `src/openharness/auth/manager.py` | auth source control | credential resolution |
| `src/openharness/cli.py` | provider/model switching and CLI entry | operator surface |
| `src/openharness/permissions/checker.py` | permission enforcement | hard path and command gates |
| `src/openharness/hooks/loader.py` | hook loading | lifecycle extension surface |
| `src/openharness/hooks/executor.py` | hook execution | block-on-failure control |
| `src/openharness/services/session_storage.py` | durable snapshots | conversation persistence |
| `src/openharness/memory/paths.py` | memory path resolution | file-based knowledge layout |
| `src/openharness/memory/manager.py` | memory index and writes | memory injection |
| `src/openharness/tasks/manager.py` | task orchestration | background work control |
| `src/openharness/tools/agent_tool.py` | agent subprocess tool | delegation entry |
| `src/openharness/tools/task_create_tool.py` | shell task creation | async work |
| `src/openharness/commands/registry.py` | slash command API | workflow surface |
| `src/openharness/engine/query.py` | carryover state and compaction trigger | compounding engine entry |
| `src/openharness/services/compact/__init__.py` | compaction core | state condensation |
| `src/openharness/ui/runtime.py` | restore and snapshot path | UI/runtime persistence |
| `ohmo/workspace.py` | personal-agent workspace seed | `.ohmo` bootstrap |
| `ohmo/session_storage.py` | gateway session reuse | continuity |
| `ohmo/gateway/runtime.py` | per-session runtime bundles | chat runtime |
| `ohmo/gateway/service.py` | gateway control plane | availability and recovery |

## Design Lessons For Wayrail

### What To Steal

- file-based memory with a small index
- clear profile and auth separation
- tool-gated permissions before outer UX
- session snapshots and lightweight restore
- the conceptual split between core harness and personal-agent layer

### What Not To Steal

- full React/TUI stack in v1
- broad task and agent orchestration platform
- `ohmo`-like personal-agent product surface too early
- lazy frontend install complexity unless truly needed

### Unclear Or Conditional Lessons

- `ohmo` may eventually be a separate downstream product layer for `wayrail`, but probably not in v1
- auto-compaction is attractive, but a lighter checkpoint and learnings approach may be enough initially

## Open Questions

- Should `wayrail` ever grow a separate “personal layer” on top of the core harness?
- How much of OpenHarness’s compaction logic can be simplified into starter-level artifacts?
- Is profile/auth separation necessary in v1 or only once multiple providers matter?

## Appendix A: Structure Pass Notes

### Install / Bootstrap

- first-class install path for CLI and `ohmo`
- frontend launch is part of runtime bootstrap
- `ohmo` seeds its own workspace state

### Artifact Inventory

- core harness runtime
- React terminal UI
- `ohmo` stack
- install/docs/media surfaces

### Architecture Map

- entry and UI dispatch
- query loop and tool execution
- persistence and compaction
- personal-agent stack

### Workflow Surface

- slash commands
- React TUI interaction model
- background tasks and delegation
- `ohmo` gateway workflows

### State / Memory

- UI/session state snapshot
- conversation persistence
- compounding metadata and auto-compaction
- durable memory files
- `ohmo` continuity layer

## Appendix B: Code Hotspot Notes

### Bootstrap Hotspots

- `scripts/install.sh`
- `scripts/install.ps1`
- `src/openharness/ui/react_launcher.py`
- `src/openharness/config/settings.py`
- `src/openharness/auth/manager.py`
- `src/openharness/cli.py`

### Control Hotspots

- `src/openharness/permissions/checker.py`
- `src/openharness/hooks/loader.py`
- `src/openharness/hooks/executor.py`
- `src/openharness/commands/registry.py`

### State / Compounding Hotspots

- `src/openharness/services/session_storage.py`
- `src/openharness/memory/paths.py`
- `src/openharness/memory/manager.py`
- `src/openharness/engine/query.py`
- `src/openharness/services/compact/__init__.py`
- `src/openharness/ui/runtime.py`
- `ohmo/workspace.py`
- `ohmo/session_storage.py`
- `ohmo/gateway/runtime.py`
- `ohmo/gateway/service.py`

## Appendix C: Detailed Bootstrap Notes

### Machine Bootstrap

The install scripts do real environment provisioning:

- Python checks
- venv creation or reuse
- package installation
- command linking

This is important because many harness repos assume the runtime exists already.

### Frontend Bootstrap

OpenHarness also needs:

- Node
- npm
- frontend assets
- runtime launch coordination between Python and React

This is one of the clearest examples of a harness with a real UI stack.

### `ohmo` Bootstrap

`ohmo` adds its own first-run seed files and workspace root.

This makes it a layered product:

- core harness
- personal-agent layer

That split is useful to remember when deciding what `wayrail` should or should not own.

## Evidence Map

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `pyproject.toml`
- `scripts/install.sh`
- `scripts/install_dev.sh`
- `scripts/install.ps1`
- `frontend/terminal/package.json`
- `frontend/terminal/src/App.tsx`
- `frontend/terminal/src/hooks/useBackendSession.ts`
- `src/openharness/__main__.py`
- `src/openharness/cli.py`
- `src/openharness/ui/react_launcher.py`
- `src/openharness/ui/backend_host.py`
- `src/openharness/ui/runtime.py`
- `src/openharness/ui/protocol.py`
- `src/openharness/ui/app.py`
- `src/openharness/ui/textual_app.py`
- `src/openharness/config/settings.py`
- `src/openharness/auth/manager.py`
- `src/openharness/permissions/checker.py`
- `src/openharness/hooks/loader.py`
- `src/openharness/hooks/executor.py`
- `src/openharness/engine/query.py`
- `src/openharness/engine/messages.py`
- `src/openharness/services/session_storage.py`
- `src/openharness/services/session_backend.py`
- `src/openharness/services/compact/__init__.py`
- `src/openharness/memory/paths.py`
- `src/openharness/memory/manager.py`
- `src/openharness/memory/memdir.py`
- `src/openharness/tasks/manager.py`
- `src/openharness/tools/agent_tool.py`
- `src/openharness/tools/task_create_tool.py`
- `src/openharness/commands/registry.py`
- `ohmo/workspace.py`
- `ohmo/cli.py`
- `ohmo/runtime.py`
- `ohmo/session_storage.py`
- `ohmo/gateway/service.py`
- `ohmo/gateway/bridge.py`
- `ohmo/gateway/runtime.py`
- `docs/SHOWCASE.md`

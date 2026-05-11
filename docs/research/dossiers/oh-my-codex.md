---
title: oh-my-codex
repo: https://github.com/Yeachan-Heo/oh-my-codex
source_repo: https://github.com/Yeachan-Heo/oh-my-codex
source_ref: d56148c
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
status: reviewed
depth: dossier
---

# Oh My Codex Dossier

## Executive Summary

`oh-my-codex` is the strongest Codex-native orchestration benchmark in the current set. It wraps Codex CLI in a local-first control layer with:

- setup and doctor flows
- managed config and hooks
- explicit state authority
- durable `.omx` state and wiki artifacts
- session-scoped compatibility layers

For `harness-kit`, the highest-value lessons are:

- install-time scaffolding should define the runtime contract
- state authority must be explicit
- global config and project state must stay distinct
- local-first compounding can be file-backed and still be strong

The main danger in copying from OMX is over-coupling to:

- tmux and session-manager assumptions
- Codex-specific launch paths
- legacy compatibility scaffolding that may only exist to preserve old behavior

## Repository Positioning

OMX is not a general agent runtime platform in the way OpenHarness is. It is a workflow and control layer around Codex:

- hooks
- skills
- prompts
- teams
- HUD or state surfaces
- project-local state

This makes it extremely relevant for `harness-kit` because the likely initial host context is Codex itself.

In practice, OMX occupies three layers:

1. bootstrap and installation layer
2. runtime state and control layer
3. knowledge and history compounding layer

## Source Snapshot

- Source repo: `https://github.com/Yeachan-Heo/oh-my-codex`
- Source ref: `d56148c`
- Capture date: `2026-04-21`
- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- Host focus: Codex
- Primary languages: TypeScript, Rust, docs
- Install surfaces: npm global install, `omx setup`, generated config, project-local `.omx` state

## Install And Bootstrap Trace

OMX’s install path already acts like a runtime builder.

### Global Bootstrap

Observed documented path:

1. install Codex and OMX globally
2. run `omx`
3. run `omx setup`
4. run `omx doctor`

There are also auto-refresh paths:

- version bump hooks
- `postinstall`
- `omx update`

This matters because installation is not merely package placement. It is expected to mutate the Codex-visible environment.

### Scope-Aware Setup

The setup surface distinguishes:

- user scope
- project scope
- legacy scope migration

And writes managed files for:

- prompts
- skills
- MCP config
- AGENTS scaffolding
- `.codex/hooks.json`
- `.codex/config.toml`

This is a key lesson for `harness-kit`: bootstrap is part of the product contract.

### Why `doctor` Matters But Is Not Enough

The repo’s own structure suggests a distinction between:

- install sanity
- authenticated runtime readiness

This is important. `harness-kit` should probably mirror that distinction:

- `setup`
- `doctor`
- `ready`

instead of treating one check as everything.

## Artifact Inventory

| Artifact | Scope | Producer | Purpose | Notes |
|---|---|---|---|---|
| `.codex/config.toml` | user or project | setup | host config | managed install surface |
| `.codex/hooks.json` | user or project | setup | hook registration | runtime contract |
| generated prompts | user or project | setup | workflow prompts | managed content |
| generated skills | user or project | setup | workflow skills | managed content |
| AGENTS scaffolding | project | setup | repo contract | setup-owned |
| `.omx/state/*.json` | project runtime | runtime | authoritative state | local-first |
| `.omx/state/sessions/<id>/*.json` | session runtime | runtime | session overlays | local-first |
| `.omx/logs/` | runtime | runtime | logs | durable state |
| `.omx/plans/` | runtime | workflow | stored plans | compounding support |
| `.omx/wiki/` | runtime | wiki subsystem | knowledge store | markdown-first memory |
| `.omx/hooks/` | runtime | setup/runtime | local hooks or hook state | runtime boundary |
| `skills/` | source content | repo | workflow material | reusable content pack |
| `templates/` | source content | repo | generated templates | packaging content |
| `src/catalog/manifest.json` | source content | repo | content index | discovery |
| `docs/prompt-guidance-fragments/` | source content | repo | reusable guidance | workflow material |

## Architecture Map

| Area | Key paths | Responsibility | Why it matters |
|---|---|---|---|
| CLI control plane | `src/cli/omx.ts`, `src/cli/setup.ts`, `src/cli/hooks.ts`, `src/cli/agents-init.ts` | install, refresh, hook management, mode commands | operator surface |
| state path resolver | `src/mcp/state-paths.ts` | scope-aware state resolution | authoritative path logic |
| compatibility state bridge | `src/state/skill-active.ts` | visible multi-skill state plus session/root copies | compounding write surface |
| state transition engine | `src/state/workflow-transition.ts`, `src/state/workflow-transition-reconcile.ts` | mode transitions | lifecycle control |
| wiki storage | `src/wiki/storage.ts`, `src/wiki/query.ts` | markdown knowledge store | file-backed compounding |
| session history | `src/session-history/search.ts` | transcript retrieval | recall surface |
| catalog reader | `src/catalog/reader.ts` | content discovery | packaged workflow inventory |
| autoresearch runtime | `src/autoresearch/runtime.ts`, `src/autoresearch/skill-validation.ts` | specialized workflow engine | nontrivial sub-workflows |
| subagent tracker | `src/subagents/tracker.ts` | delegation tracking | coordination surface |
| HUD state | `src/hud/state.ts` | visible session state | operator observability |

## Workflow Surface

### Canonical In-Session Path

Observed pattern:

- `$deep-interview`
- `$ralplan`
- `$team` or `$ralph`

with allowlisted transitions and overlap rules.

This matters because OMX is not only “here are some prompts.” It has a structured route through work modes.

### Operator Commands

The operator command layer handles:

- setup
- state
- hooks
- teams
- updates
- diagnostics

This strongly suggests `harness-kit` should think in two layers:

- in-session workflow
- operator control plane

### Why This Matters

Without the operator layer:

- project-local state drifts
- hook registration drifts
- managed files drift

and the workflow layer becomes less trustworthy.

## State, Memory, And Compounding

This is OMX’s strongest area.

### State Authority

Observed:

- root vs session precedence
- per-mode JSON state
- compatibility state such as `skill-active`
- explicit state-path validation

This is a major design lesson for `harness-kit`: state needs a canonical authority model.

### Local Wiki

`.omx/wiki` is important because it proves a useful middle ground:

- durable
- local
- file-based
- queryable

This is far easier to bootstrap than a memory service and probably enough for v1 or v2.

### Session Search

Persistent transcript or session search adds a different compounding layer:

- not just “what rules do I have?”
- but “what actually happened in prior runs?”

That is valuable for `harness-kit`, though possibly later than v1.

## Verification, Permissions, And Recovery

OMX’s control surfaces are mostly about:

- state correctness
- setup correctness
- safe writes
- resume behavior

### High-Value Recovery Points

- `src/mcp/state-paths.ts`
  prevents invalid state paths and controls scope
- `src/state/skill-active.ts`
  writes normalized state across root and session layers
- `src/wiki/storage.ts`
  atomic writes plus lock directories

These are small but crucial. They show that compounding state must be protected against corruption.

### Why This Matters

`harness-kit` may never build a runtime as rich as OMX, but it should still borrow:

- clear scope resolution
- atomic writes
- explicit repair or clear semantics

## Code Hotspots

| File | Why it matters | Key concept |
|---|---|---|
| `src/cli/omx.ts` | first code path on launch | env/provider bootstrap |
| `src/cli/setup.ts` | managed install and refresh writer | bootstrap ownership |
| `src/cli/hooks.ts` | hook control | runtime contract |
| `src/cli/agents-init.ts` | generated content init | setup output |
| `src/mcp/state-paths.ts` | canonical state-path resolver | scope and authority |
| `src/state/skill-active.ts` | compatibility state bridge | root/session writes |
| `src/state/workflow-transition.ts` | state transition engine | lifecycle control |
| `src/state/workflow-transition-reconcile.ts` | transition reconciliation | repair semantics |
| `src/wiki/storage.ts` | durable wiki writes | atomic memory |
| `src/wiki/query.ts` | wiki retrieval | local knowledge recall |
| `src/session-history/search.ts` | transcript search | compounding via history |
| `src/catalog/reader.ts` | content discovery | packaged workflow inventory |
| `src/autoresearch/runtime.ts` | specialized workflow engine | complex sub-workflow |
| `src/subagents/tracker.ts` | delegation tracking | agent coordination |
| `src/hud/state.ts` | visible operator state | observability |

## Design Lessons For Harness Kit

### What To Steal

- explicit state authority model
- project-local versus global boundary clarity
- atomic file-backed compounding
- setup that owns generated files while preserving user-managed entries
- separate install sanity checks from actual runtime readiness

### What Not To Steal

- over-coupling to Codex, tmux, or session-manager specifics
- compatibility scaffolding without a removal plan
- large runtime and team features before the starter layer is stable

### Unclear Or Conditional Lessons

- local wiki compounding is strong, but `harness-kit` may not need it in v1
- the full team runtime may belong in a later runtime layer, not in the starter

## Open Questions

- How much of the workflow transition logic is truly generic versus tied to OMX’s role system?
- Does `harness-kit` need transcript search in v1, or only lightweight learnings and checkpoints?
- Which OMX compatibility layers are migration-only?

## Appendix A: Structure Pass Notes

### Install / Bootstrap

- global install plus `omx setup`
- scope-aware managed writes
- doctor and update paths

### Artifact Inventory

- `.omx/state`
- `.omx/logs`
- `.omx/plans`
- `.omx/wiki`
- generated prompts and skills
- AGENTS scaffolding

### Architecture Map

- CLI/control plane
- state/reconciliation
- memory/knowledge
- specialized workflow engines

### Workflow Surface

- canonical in-session path
- operator commands

### State / Memory

- mode state and compatibility
- compounding knowledge via wiki and history

## Appendix B: Code Hotspot Notes

### Bootstrap Hotspots

- `src/cli/omx.ts`
- `src/cli/setup.ts`
- `src/cli/hooks.ts`
- `src/cli/agents-init.ts`

### State Hotspots

- `src/mcp/state-paths.ts`
- `src/state/skill-active.ts`
- `src/state/workflow-transition.ts`
- `src/state/workflow-transition-reconcile.ts`

### Compounding Hotspots

- `src/wiki/storage.ts`
- `src/wiki/query.ts`
- `src/session-history/search.ts`
- `src/catalog/reader.ts`

## Appendix C: Detailed Bootstrap Notes

### Global Install Expectations

OMX assumes more than package presence.

Observed bootstrap expectations:

- Codex is installed
- OMX is installed
- setup mutates Codex-visible config
- doctor inspects the environment
- update can refresh managed assets

This means `omx setup` is closer to an installer plus migrator than a convenience command.

### Project Scope Expectations

Project-scoped setup matters because it can write:

- AGENTS scaffolding
- project hooks
- project-visible config
- `.omx` state roots

This is likely the most reusable pattern for `harness-kit`.

### Why Local State Matters

OMX is strongest when it keeps local authority explicit:

- `.omx/state`
- `.omx/wiki`
- session overlays

That is the practical reason the product can compound without pretending it has a central memory service.

## Appendix D: Detailed File Role Notes

- `src/cli/omx.ts`
  Bootstraps providers and environment before any command runs.
- `src/cli/setup.ts`
  Main bootstrap writer for managed files.
- `src/cli/hooks.ts`
  Hook lifecycle control.
- `src/cli/agents-init.ts`
  Generated content and initialization helper.
- `src/mcp/state-paths.ts`
  Canonical path resolver. Most important state file.
- `src/state/skill-active.ts`
  Compatibility bridge and dual-copy write path.
- `src/state/workflow-transition.ts`
  Transition allow/deny logic.
- `src/state/workflow-transition-reconcile.ts`
  Recovery and reconciliation around transitions.
- `src/wiki/storage.ts`
  Atomic file-backed wiki writes with locking.
- `src/wiki/query.ts`
  Retrieval path for local knowledge.
- `src/session-history/search.ts`
  Search surface for prior execution history.
- `src/catalog/reader.ts`
  Content inventory and discovery path.
- `src/autoresearch/runtime.ts`
  Specialized workflow runtime.
- `src/autoresearch/skill-validation.ts`
  Research/validation support path.
- `src/subagents/tracker.ts`
  Delegation tracker.
- `src/hud/state.ts`
  Visible session or operator state.

## Appendix E: Detailed State Boundary Notes

### Root Versus Session Scope

OMX is useful because it does not hide this distinction.

Observed conceptual split:

- root-scoped truth for broader project state
- session-scoped overlays for active runs
- compatibility state for legacy or visible surfaces

This is more mature than simply storing one `state.json`.

### Wiki Versus History

The repo also separates:

- wiki knowledge
- session-history search

That is a meaningful design move because “durable knowledge” and “searchable execution history” are not the same thing.

## Appendix F: High-Yield Follow-Up Questions

- What exact allow/deny table exists in `workflow-transition.ts`?
- Which files define the canonical set of modes?
- What is the minimum viable subset of `.omx/wiki` worth copying into `harness-kit`?
- How much of the `doctor` command is static inspection versus live execution validation?
- Which compatibility layers are still actively exercised by tests or docs, and which are just legacy baggage?

## Appendix G: Minimal OMX Slice For Harness Kit

If `harness-kit` only copied the smallest useful OMX slice, it would likely include:

- setup with clear owned-file boundaries
- state authority and scope resolution
- atomic local wiki writes
- explicit distinction between install sanity and runtime readiness

## Evidence Map

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `package.json`
- `src/cli/omx.ts`
- `src/cli/setup.ts`
- `src/cli/hooks.ts`
- `src/cli/agents-init.ts`
- `src/mcp/state-paths.ts`
- `src/state/skill-active.ts`
- `src/state/workflow-transition.ts`
- `src/state/workflow-transition-reconcile.ts`
- `src/wiki/storage.ts`
- `src/wiki/query.ts`
- `src/session-history/search.ts`
- `src/catalog/reader.ts`
- `src/autoresearch/runtime.ts`
- `src/autoresearch/skill-validation.ts`
- `src/subagents/tracker.ts`
- `src/hud/state.ts`
- `docs/STATE_MODEL.md`
- `docs/codex-native-hooks.md`
- `docs/prompt-guidance-contract.md`
- `docs/reference/project-wiki.md`
- `docs/reference/ralph-parity-matrix.md`

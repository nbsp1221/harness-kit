---
title: compound-engineering-plugin
repo: https://github.com/EveryInc/compound-engineering-plugin
source_repo: https://github.com/EveryInc/compound-engineering-plugin
source_ref: 4c57508
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
status: reviewed
depth: dossier
---

# Compound Engineering Plugin Dossier

## Executive Summary

`compound-engineering-plugin` is best understood as a multi-host packaging and workflow-distribution system for a staged engineering method, not as a standalone runtime. It distributes skills, agents, docs, and conversion logic across multiple targets, and the install surface is one of its most important design areas. For `harness-kit`, the most reusable parts are:

- explicit lifecycle stages with artifact handoffs
- manifest-backed install and cleanup
- target-specific bundle writers
- path-safety checks around generated artifacts
- session-history extraction and documentation-backed compounding

The least reusable parts for `harness-kit` v1 are:

- broad cross-host packaging before the local contract is stable
- shared-root artifact ownership patterns
- treating documentation-heavy compounding as a substitute for a true memory substrate

## Repository Positioning

The repo presents itself as an official compound engineering plugin. In practice, it occupies three roles at once:

1. a methodology pack
2. a plugin conversion toolchain
3. a host-specific installer and cleanup surface

That distinction matters because the repo's visible philosophy can distract from its most important engineering contribution: controlled bundle generation and migration across different host layouts.

For `harness-kit`, this makes `compound-engineering-plugin` more useful as a benchmark for:

- staged lifecycle packaging
- target-aware install behavior
- generated-file ownership boundaries
- upgrade and cleanup safety

than as a benchmark for:

- long-lived runtime state
- daemon orchestration
- background agents

## Source Snapshot

- Source repo: `https://github.com/EveryInc/compound-engineering-plugin`
- Source ref: `4c57508`
- Capture date: `2026-04-21`
- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- Host focus: multi-host
- Primary languages: TypeScript plus plugin content
- Install surfaces: plugin marketplace, Bun CLI, target-specific install and conversion

## Install And Bootstrap Trace

The install story has two different layers.

### Layer 1: Distribution Install

This gets the plugin or package into a host-visible location.

Observed forms:

- marketplace-style plugin install for supported hosts
- local or GitHub-based plugin resolution
- Bun CLI entrypoint through `src/index.ts`
- target-specific install writers through `src/commands/install.ts`

The critical point is that installation is not generic. The install command:

- parses target arguments
- resolves whether the plugin comes from local, branch, or bundled source
- decides whether `--all` or `--also` targets need to be written
- validates scope
- dispatches into target-specific writers

This means the repo treats installation as a real engineering surface, not as a one-line copy step.

### Layer 2: Per-Project Bootstrap

The repo’s public workflow expects a second step after plugin installation: `/ce-setup`.

That means:

- install does not fully initialize project behavior
- the project bootstrap is intentionally separate from the package bootstrap
- `compound-engineering-plugin` distinguishes “plugin available” from “project prepared”

For `harness-kit`, this is a major lesson. We should not collapse:

- host install
- repo bootstrap
- first project diagnosis

into one action unless the resulting ownership boundaries stay obvious.

### Install Path Trace

High-level trace reconstructed from the code and docs:

1. choose source package or plugin bundle
2. choose target host
3. resolve output root for the target
4. validate scope and supported target combination
5. write skills, prompts, agents, and manifests
6. ensure target-specific compatibility artifacts such as Codex agents files
7. record managed artifacts so cleanup can later distinguish owned from foreign files
8. run project-local `/ce-setup` after installation

### Why This Matters

The install path already contains most of the architectural discipline `harness-kit` needs:

- target-aware output
- managed ownership
- cleanup symmetry
- post-install repo bootstrap

## Artifact Inventory

| Artifact | Scope | Producer | Purpose | Notes |
|---|---|---|---|---|
| `.claude-plugin/marketplace.json` | distribution | repo source | marketplace metadata | release boundary |
| `plugins/compound-engineering/.claude-plugin/plugin.json` | target content | plugin source | plugin manifest | host install surface |
| `plugins/compound-engineering/README.md` | target content | plugin source | describes shipped workflow surface | high-level payload description |
| `plugins/compound-engineering/AGENTS.md` | target content | plugin source | agent layout and host guidance | important for generated behavior |
| `plugins/compound-engineering/skills/**` | target content | plugin source | skills surface | major behavior payload |
| `plugins/compound-engineering/agents/**` | target content | plugin source | agents surface | review and specialized work |
| `src/index.ts` | CLI source | Bun CLI | command entrypoint | top-level dispatcher |
| `src/commands/install.ts` | CLI source | install command | install orchestration | bootstrap choke point |
| `src/commands/cleanup.ts` | CLI source | cleanup command | remove stale managed artifacts | symmetry with install |
| `src/commands/convert.ts` | CLI source | conversion command | host conversion | repackaging surface |
| `src/targets/codex.ts` | target writer | install pipeline | Codex-specific bundle writes | high-risk write path |
| `src/targets/opencode.ts` | target writer | install pipeline | OpenCode bundle writes | layout and backup logic |
| `src/targets/managed-artifacts.ts` | shared infra | target writers | managed ownership and cleanup safety | defense-in-depth |
| `src/utils/resolve-output.ts` | shared infra | install pipeline | target root resolution | canonical output path logic |
| `src/utils/codex-agents.ts` | Codex compatibility | install pipeline | create/update Codex agents bootstrap | persistent compatibility surface |
| `tests/manifest-path-safety.test.ts` | tests | repo source | path containment guard | critical install safety |
| `tests/plugin-legacy-artifacts.test.ts` | tests | repo source | legacy allowlist correctness | upgrade safety |
| `tests/legacy-cleanup.test.ts` | tests | repo source | cleanup correctness | stale artifact pruning |
| `tests/session-history-scripts.test.ts` | tests | repo source | session-history extraction tooling | compounding support |
| `plugins/compound-engineering/skills/ce-session-inventory/scripts/*` | tooling | shipped plugin | parse session metadata | cross-tool history |
| `plugins/compound-engineering/skills/ce-session-extract/scripts/*` | tooling | shipped plugin | extract session details | history-based compounding |

## Architecture Map

| Area | Key paths | Responsibility | Why it matters |
|---|---|---|---|
| CLI entrypoint | `src/index.ts` | top-level command routing | all behavior starts here |
| Install orchestration | `src/commands/install.ts` | resolve source, target, and scope; invoke writers | bootstrap choke point |
| Convert orchestration | `src/commands/convert.ts` | transform plugin content for targets | same payload, different host surface |
| Cleanup orchestration | `src/commands/cleanup.ts` | remove stale managed content safely | install symmetry and migration safety |
| Output resolution | `src/utils/resolve-output.ts` | canonical output roots | prevents target confusion |
| Target registry | `src/targets/index.ts` | select writer and scope behavior | central target fan-out |
| Codex writer | `src/targets/codex.ts` | prompts, skills, agents, config, manifests | strongest Codex benchmark here |
| OpenCode writer | `src/targets/opencode.ts` | layout, backup, file writes | second strongest writer surface |
| Managed ownership layer | `src/targets/managed-artifacts.ts` | path-safety and artifact manifests | most important cleanup safety layer |
| Compatibility writer | `src/utils/codex-agents.ts` | AGENTS bootstrap for Codex | persistent compatibility shim |
| Legacy memory layer | `src/data/plugin-legacy-artifacts.ts` | old names and cleanup allowlists | upgrade memory encoded in code |
| Workflow docs | `docs/solutions/**` | method and packaging rationale | real operating knowledge |

## Workflow Surface

The workflow surface is not only code. It is split between:

- shipped skills and agents
- public plugin README
- session tools
- review personas
- compounding support files

### Core Loop

Observed commands or capabilities in the shipped plugin surface include:

- `/ce-ideate`
- `/ce-brainstorm`
- `/ce-plan`
- `/ce-work`
- `/ce-code-review`
- `/ce-debug`
- `/ce-compound`
- `/ce-compound-refresh`
- `/ce-optimize`

These imply a staged lifecycle:

1. idea or problem framing
2. planning
3. execution
4. review or repair
5. compounding or optimization

### Research And Context Surface

The plugin also exposes context-recovery and research helpers, including:

- session-related commands
- slack research
- learnings researcher
- repo research analyst

That means compounding is not just “save notes.” It also includes retrieval surfaces that help future sessions re-open context.

### Review Surface

The plugin groups a number of review roles, including:

- correctness
- security
- testing
- adversarial
- maintainability

This suggests the plugin wants “compound engineering” to mean:

- staged work
- multiple review perspectives
- persistence of useful learnings

## State, Memory, And Compounding

This repo is weaker as a native memory benchmark than as a compounding practice benchmark.

### What Exists

- historical artifact allowlists and cleanup memory encoded in source
- session-history extraction tooling
- documentation about learnings, lifecycle, and refresh

### What Appears To Be Missing

- a visible runtime memory service
- a dedicated local or remote memory database
- a state daemon or long-lived compaction substrate

### Memory Surfaces That Do Matter

#### Legacy Artifact Memory

`src/data/plugin-legacy-artifacts.ts` is effectively product memory encoded as code:

- it remembers historical skill, agent, and command surfaces
- cleanup uses it to back up or prune old content safely

This matters because it proves a strong engineering principle: upgrade memory belongs in code, not only in release notes.

#### Session History Compounding

The session extraction tooling indicates a different kind of memory:

- parse sessions from multiple tools
- extract branch, cwd, model, session IDs
- derive reusable context from prior runs

This is not a general-purpose memory store, but it is a real compounding mechanism.

### Practical Lesson

`harness-kit` should copy:

- structured learnings and lifecycle artifacts
- session-history extraction if useful
- migration memory encoded in code

`harness-kit` should not assume:

- that this repo already solved durable memory as a substrate

## Verification, Permissions, And Recovery

The strongest verification and control ideas here are around install safety and ownership recovery.

### Install Safety

The repo uses:

- target-aware output resolution
- scope validation
- manifest path safety tests
- ownership-aware cleanup

This is more mature than typical prompt-pack repos.

### Cleanup Symmetry

`src/commands/cleanup.ts` mirrors the same roots and layouts used during install. That matters because cleanup bugs are usually ownership bugs:

- deleting too much
- missing stale content
- confusing shared and managed files

The repo protects against this with:

- explicit managed manifests
- path checks
- legacy artifact allowlists

### Recovery Model

Recovery here is less about session resume and more about:

- install drift
- stale artifacts
- migration between naming generations

That makes this repo especially valuable as a bootstrap and upgrade benchmark.

## Code Hotspots

| File | Why it matters | Key concept |
|---|---|---|
| `src/commands/install.ts` | main bootstrap choke point | target-aware install orchestration |
| `src/utils/resolve-output.ts` | canonical output root resolution | host path policy |
| `src/targets/index.ts` | registry from target to writer | target fan-out |
| `src/targets/codex.ts` | most important persistent write path for Codex | prompts, skills, agents, config, manifest cleanup |
| `src/targets/opencode.ts` | strong second writer surface | layout, backup, migration behavior |
| `src/targets/managed-artifacts.ts` | shared safety layer | ownership, manifests, cleanup filtering |
| `src/utils/codex-agents.ts` | Codex compatibility shim | persistent AGENTS bootstrap |
| `src/commands/cleanup.ts` | install symmetry and cleanup safety | managed removal |
| `src/data/plugin-legacy-artifacts.ts` | encoded historical memory | safe upgrade boundaries |
| `tests/manifest-path-safety.test.ts` | install safety proof | path containment |
| `tests/plugin-legacy-artifacts.test.ts` | legacy allowlist proof | cleanup correctness |
| `tests/legacy-cleanup.test.ts` | stale artifact pruning proof | migration safety |
| `tests/session-history-scripts.test.ts` | history extraction proof | compounding support |

## Design Lessons For Harness Kit

### What To Steal

- explicit stage separation with different artifact types
- install and cleanup symmetry
- manifest-backed ownership
- path-safety checks for generated content
- migration memory encoded in code
- session-history extraction as a compounding aid

### What Not To Steal

- broad multi-host packaging too early
- shared-root writes before ownership rules are solid
- assuming doc-heavy compounding equals a durable memory substrate

### Unclear Or Conditional Lessons

- Codex agent file generation is useful, but the exact AGENTS bootstrap pattern may depend on how `harness-kit` defines its own repo contract.
- Session-history parsing may be worth it later, but probably not in v1 unless compounding becomes central immediately.

## Open Questions

- What exactly is persisted by `ce-compound` and `ce-compound-refresh`?
- How much of the session-history flow is operationally important versus exploratory?
- Which target writers beyond Codex and OpenCode contain unique logic rather than shared patterns?

## Appendix A: Structure Pass Notes

### Install / Bootstrap

- Native install is marketplace-first, with a separate Bun CLI path for conversion and a Codex-specific split between skills and agents.
- Evidence: `README.md`, `src/index.ts`, `src/commands/install.ts`, `src/utils/resolve-output.ts`, `src/targets/index.ts`.
- `/ce-setup` is the project bootstrap after install.
- Evidence: `README.md`.

### Artifact Inventory

- Distribution metadata lives in marketplace and plugin manifests.
- Runtime content bundle is mostly skills, agents, and docs under the shipped plugin subtree.
- Session-history tooling exists in shipped scripts and tests.

### Architecture Map

- CLI and orchestration: `src/index.ts`, `src/commands/*`
- Parse-convert-write pipeline: parsers, converters, types, targets
- Managed cleanup and path scoping: target writers plus managed-artifact safety

### Workflow Surface

- Core loop includes ideate, brainstorm, plan, work, code review, debug, compound, and refresh.
- Research and retrieval commands exist alongside execution and review surfaces.

### State / Memory

- Legacy artifact memory is encoded in source.
- Session-history compounding is history-driven and cross-tool.
- Exact `ce-compound` persisted shape still needs deeper verification.

## Appendix B: Code Hotspot Notes

### Install / Bootstrap Hotspots

- `src/commands/install.ts`
- `src/utils/resolve-output.ts`
- `src/targets/index.ts`
- `src/targets/codex.ts`
- `src/targets/opencode.ts`
- `src/utils/codex-agents.ts`

### Verification / Control Hotspots

- `src/commands/cleanup.ts`
- `src/targets/managed-artifacts.ts`
- `tests/manifest-path-safety.test.ts`
- `tests/plugin-legacy-artifacts.test.ts`
- `tests/legacy-cleanup.test.ts`

### Compounding / Memory Hotspots

- `src/data/plugin-legacy-artifacts.ts`
- `tests/session-history-scripts.test.ts`
- `plugins/compound-engineering/skills/ce-session-inventory/scripts/*`
- `plugins/compound-engineering/skills/ce-session-extract/scripts/*`

## Appendix C: Detailed Install Trace Notes

### Step 1: Determine install source

- local path install is supported
- branch-based fetch is supported
- bundled plugin install is supported
- GitHub source resolution is supported

This matters because provenance affects both conversion behavior and cleanup ownership.

### Step 2: Determine target

Observed target classes in the code:

- Codex
- OpenCode
- Pi
- Gemini
- Kiro
- other supported conversion targets

The repo does not assume one host layout. That is why `src/targets/index.ts` exists as a dispatch layer.

### Step 3: Resolve target root

`resolve-output.ts` acts as a policy file for:

- where prompts go
- where skills go
- where agents go
- which scope is valid

This should be read before any target writer because it defines the directory contract.

### Step 4: Perform writes

Target writers then:

- create directories
- write generated artifacts
- update or merge config files
- update managed manifests

This is why target writers are more important than README install instructions.

### Step 5: Register compatibility artifacts

Codex in particular gets extra handling through:

- agent bootstrapping
- AGENTS file generation or updating
- config merge behavior

This is the practical difference between “copy content” and “make the host actually usable.”

### Step 6: Enable cleanup symmetry

Every install path needs a cleanup path that:

- knows which files it owns
- knows which legacy files may exist
- refuses out-of-scope deletion

This is one of the most important reusable lessons in the repo.

## Appendix D: Detailed File Role Notes

- `src/index.ts`
  Top-level CLI entry. Good first file to read if you need to see command boundaries.
- `src/commands/install.ts`
  Central bootstrap orchestrator. Most important install file.
- `src/commands/convert.ts`
  Tells you how plugin content becomes host-specific content.
- `src/commands/cleanup.ts`
  Mirrors install behavior and reveals ownership assumptions.
- `src/targets/index.ts`
  Registry of target writers and target capabilities.
- `src/utils/resolve-output.ts`
  Directory policy layer. Important for scope and root reasoning.
- `src/targets/codex.ts`
  Most useful target writer for `harness-kit`, since Codex matters immediately.
- `src/targets/opencode.ts`
  Useful comparison writer because it has different output semantics.
- `src/targets/managed-artifacts.ts`
  Best file for understanding safe cleanup.
- `src/utils/codex-agents.ts`
  Best file for understanding Codex compatibility writes.
- `src/data/plugin-legacy-artifacts.ts`
  Best file for understanding upgrade memory encoded as data.
- `tests/manifest-path-safety.test.ts`
  Best file for understanding install safety expectations.
- `tests/plugin-legacy-artifacts.test.ts`
  Best file for understanding how seriously the repo treats legacy cleanup.
- `tests/legacy-cleanup.test.ts`
  Best file for understanding stale artifact removal rules.
- `tests/session-history-scripts.test.ts`
  Best file for understanding compounding via history extraction.
- `plugins/compound-engineering/README.md`
  Best high-level view of shipped workflow surface.
- `plugins/compound-engineering/AGENTS.md`
  Best high-level view of shipped agent and skill structure.
- `plugins/compound-engineering/skills/**`
  Real workflow payload.
- `plugins/compound-engineering/agents/**`
  Real review and execution payload.

## Evidence Map

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `src/index.ts`
- `src/commands/install.ts`
- `src/commands/convert.ts`
- `src/commands/cleanup.ts`
- `src/commands/list.ts`
- `src/commands/plugin-path.ts`
- `src/utils/resolve-output.ts`
- `src/utils/codex-agents.ts`
- `src/targets/index.ts`
- `src/targets/codex.ts`
- `src/targets/opencode.ts`
- `src/targets/managed-artifacts.ts`
- `src/data/plugin-legacy-artifacts.ts`
- `tests/manifest-path-safety.test.ts`
- `tests/plugin-legacy-artifacts.test.ts`
- `tests/legacy-cleanup.test.ts`
- `tests/session-history-scripts.test.ts`
- `plugins/compound-engineering/README.md`
- `plugins/compound-engineering/AGENTS.md`
- `plugins/compound-engineering/skills/**`
- `plugins/compound-engineering/agents/**`

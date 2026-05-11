---
title: gstack
repo: https://github.com/garrytan/gstack
source_repo: https://github.com/garrytan/gstack
source_ref: e23ff28
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
status: reviewed
depth: dossier
---

# gstack Dossier

## Executive Summary

`gstack` is a broad engineering operating system built around roles, a browser daemon, repo policy injection, and durable project memory. It is not a minimal prompt pack and not just a skill library. For `harness-kit`, the high-value lessons are:

- deterministic host-aware bootstrap
- stage routing backed by skills and tools
- persistent browser and project state
- append-only learnings, timeline, and checkpoint artifacts
- repo-level enforcement for team usage

The main risk in copying from `gstack` is importing too much:

- browser infrastructure
- telemetry and prompt nudges
- a very large role surface

## Repository Positioning

The repo frames itself as an exact setup, but in practice it is a full environment:

- skills and commands
- browser runtime
- state trees under `.gstack` and `~/.gstack`
- repo-level enforcement hooks
- learning and taste capture

This makes it less useful as a direct v1 template and more useful as:

- a reference for rich runtime control
- a reference for persistent memory and checkpointing
- a reference for team bootstrap and repo policy

## Source Snapshot

- Source repo: `https://github.com/garrytan/gstack`
- Source ref: `e23ff28`
- Capture date: `2026-04-21`
- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- Host focus: Claude Code first, plus host-aware compatibility
- Primary languages: shell, TypeScript, docs, generated binaries
- Install surfaces: repo clone, `./setup`, optional `--team`, browser binary build

## Install And Bootstrap Trace

The install path is working-tree based, not package based.

### Global Install

High-level flow:

1. clone repo into skill directory
2. run `./setup`
3. build or refresh browser and related binaries as needed
4. relink skills
5. detect host-specific conditions
6. register/update session-start and team behavior as needed

Important traits:

- `bun` is a real dependency
- browser tooling is part of the main install, not a side extension
- Codex migrations can happen during setup
- prefix and config behavior are persisted

### Team Mode

`gstack-team-init` turns the system from a personal setup into repo policy.

Observed effects:

- project `CLAUDE.md` routing is written
- `.claude/hooks/check-gstack.sh` is added
- required mode can block work when the global install is missing

This is significant because it shows a strong pattern for `harness-kit`:

- personal install
- repo adoption
- required or optional enforcement

### Ongoing Update Path

Update behavior is not passive.

Observed surfaces:

- `bin/gstack-update-check`
- `bin/gstack-session-update`
- `bin/gstack-relink`

This means bootstrap is not one moment. It is maintained over time.

## Artifact Inventory

| Artifact | Scope | Producer | Purpose | Notes |
|---|---|---|---|---|
| `SKILL.md` | repo root | source | root skill | top-level activation |
| `docs/skills.md` | repo docs | source | skill catalog | workflow map |
| `ARCHITECTURE.md` | repo docs | source | runtime architecture | browser and state model |
| `BROWSER.md` | repo docs | source | browser harness contract | action API |
| `ETHOS.md` | repo docs | source | product philosophy | workflow framing |
| `setup` | installer | source | install, build, relink, migrate | primary bootstrap |
| `bin/gstack-team-init` | repo policy | source | team bootstrap | repo enforcement |
| `bin/gstack-config` | config control | source | read/write config | canonical config interface |
| `bin/gstack-update-check` | update control | source | nags and cache TTL | session-start behavior |
| `bin/gstack-session-update` | update control | source | background update flow | maintenance |
| `browse/dist/browse` | runtime binary | build output | browser daemon entry | generated artifact |
| `design/dist/design` | build output | build | design helper | part of tool surface |
| `.gstack/browse.json` | project state | runtime | browser session state | authoritative project browser state |
| `.gstack/browse-console.log` | project state | runtime | console log persistence | browser runtime state |
| `.gstack/browse-network.log` | project state | runtime | network trace | browser runtime state |
| `.gstack/browse-dialog.log` | project state | runtime | dialog trace | browser runtime state |
| `timeline.jsonl` | memory | script | project timeline | append-only |
| `learnings.jsonl` | memory | script | durable learnings | searchable |
| `taste-profile.json` | memory | script | preference/taste state | decay-aware |
| `~/.gstack/projects/$SLUG/checkpoints/*.md` | checkpoint layer | skills/scripts | recoverable work state | markdown recovery |
| `[gstack-context]` WIP commit flow | checkpoint layer | workflow | git-backed recovery | repo-integrated |

## Architecture Map

| Area | Key paths | Responsibility | Why it matters |
|---|---|---|---|
| bootstrap installer | `setup` | build, migrate, relink, verify | install choke point |
| team policy | `bin/gstack-team-init` | repo routing and enforcement | turns personal install into shared policy |
| config control | `bin/gstack-config` | canonical config read/write | persistent settings authority |
| update control | `bin/gstack-update-check`, `bin/gstack-session-update`, `bin/gstack-relink` | upgrade and relink flow | ongoing bootstrap maintenance |
| browser daemon | `browse/src/server.ts` | long-lived Chromium server | core runtime engine |
| browser manager | `browse/src/browser-manager.ts` | cookies, tabs, contexts | continuity and restore |
| tab state | `browse/src/tab-session.ts` | refs, HTML replay, snapshot state | persistent page context |
| token registry | `browse/src/token-registry.ts` | auth and ref linkage | browser authority |
| command API | `browse/src/commands.ts`, `meta-commands.ts`, `read-commands.ts`, `write-commands.ts` | action vocabulary | explicit browser control surface |
| security layer | `browse/src/security.ts`, `browse/src/audit.ts` | browser controls and audit | runtime safety |
| project memory writers | `bin/gstack-timeline-log`, `bin/gstack-learnings-log`, `bin/gstack-taste-update` | durable learning state | long-term compounding |
| workflow skill library | role and stage dirs | staged work and routing | user-facing engineering OS |

## Workflow Surface

### Main Skill Set

Observed public surfaces include:

- `office-hours`
- `plan-ceo-review`
- `plan-eng-review`
- `plan-design-review`
- `design-consultation`
- `design-shotgun`
- `design-html`
- `review`
- `qa`
- `ship`
- `land-and-deploy`
- `canary`
- `benchmark`
- `cso`
- `document-release`
- `retro`
- `browse`
- `setup-browser-cookies`
- `autoplan`
- `learn`
- `codex`
- `careful`
- `freeze`
- `guard`
- `unfreeze`
- `open-gstack-browser`
- `setup-deploy`
- `gstack-upgrade`
- `context-save`
- `context-restore`

### Browser Command Layer

The browser surface is not implied. It is explicit.

Observed commands include:

- `snapshot`
- `click`
- `fill`
- `goto`
- `pdf`
- `responsive`
- `handoff`
- `resume`
- `connect`
- `disconnect`
- `watch`
- `state`

This is important because many “workflow” repos still rely on vague browser instructions. `gstack` instead has a real action API.

### Memory And Recovery Skills

Observed:

- `context-save`
- `context-restore`
- `learn`
- `retro`

This makes memory and recovery part of the product surface, not only internal machinery.

## State, Memory, And Compounding

`gstack` is one of the richest state models in the target set.

### Browser Session State

Persisted artifacts include:

- `browse.json`
- console logs
- network logs
- dialog logs
- tab state and replayable content

This means browser use is durable and inspectable, not ephemeral.

### Project Memory

Observed persistent memory surfaces:

- `timeline.jsonl`
- `learnings.jsonl`
- `taste-profile.json`

Notably:

- learnings are searchable
- taste is updated and decays
- timeline is append-only

This is much more concrete than a generic “memory” claim.

### Checkpoint Recovery

Observed recovery artifacts:

- markdown checkpoints under project slug directories
- WIP git-based context flow
- session-start rehydration via recent artifacts and checkpoints

This means `gstack` supports reconstruction through:

- files
- git
- session logs

instead of depending only on long conversational context.

Known gap at the current dossier depth:

- the exact checkpoint frontmatter/schema used by `context-save` and `context-restore` is still not reconstructed here
- this dossier is stronger on checkpoint existence and recovery model than on checkpoint field-level format

## Verification, Permissions, And Recovery

`gstack`'s control model is spread across:

- bootstrap and config scripts
- browser daemon code
- security and audit modules
- QA and ship stages
- update and relink tooling

### High-Value Control Surfaces

- `bin/gstack-settings-hook`
  atomic modification of Claude settings and SessionStart hooks
- `bin/gstack-update-check`
  update nagging plus TTL, snooze, and remote validation
- `browse/src/server.ts`
  authoritative browser state writes and runtime logs
- `browse/src/security.ts`
  browser safety surface

### Recovery Surface

Recovery is not one function. It is distributed:

- update and relink
- context save and restore
- checkpoints
- learning logs
- browser daemon persistence

This is why `gstack` feels like an OS rather than a skill pack.

## Code Hotspots

| File | Why it matters | Key concept |
|---|---|---|
| `setup` | main install and migration gate | bootstrap installer |
| `bin/gstack-config` | canonical config interface | persistent settings authority |
| `bin/gstack-update-check` | update policy gate | version nags and TTL |
| `bin/gstack-session-update` | background update flow | ongoing maintenance |
| `bin/gstack-team-init` | repo policy injection | team enforcement |
| `bin/gstack-settings-hook` | atomic hook registration | session-start control |
| `bin/gstack-relink` | skill relinking | bootstrap repair |
| `browse/src/config.ts` | `.gstack` path derivation | project state root |
| `browse/src/server.ts` | browser runtime state writer | authoritative runtime state |
| `browse/src/browser-manager.ts` | cookie/context restore | continuity |
| `browse/src/tab-session.ts` | per-tab refs and replay | page persistence |
| `browse/src/commands.ts` | action API | explicit browser control |
| `bin/gstack-timeline-log` | append-only project timeline | compounding state |
| `bin/gstack-learnings-log` | durable learnings writer | searchable memory |
| `bin/gstack-learnings-search` | memory retrieval | reuse of learnings |
| `bin/gstack-taste-update` | preference persistence | decayed taste model |

## Design Lessons For Harness Kit

### What To Steal

- deterministic host-aware bootstrap
- repo-level enforcement modes
- append-only learnings and checkpoints
- explicit action API behind browser or tool-driven surfaces
- configuration as a real product interface

### What Not To Steal

- the full browser daemon in v1 unless genuinely required
- first-run nudges and high-friction prompt stack
- the entire role catalog as a default harness

### Unclear Or Conditional Lessons

- `taste-profile.json` is interesting, but `harness-kit` may not need user-taste modeling in v1
- browser runtime persistence is powerful, but may be a downstream runtime layer rather than starter logic

## Open Questions

- What exact checkpoint frontmatter schema do `context-save` and `context-restore` use?
- How much of the browser layer is essential to the product and how much is convenience?
- Which parts of the telemetry layer are operationally necessary versus advisory?

## Appendix A: Structure Pass Notes

### Install / Bootstrap

- install path is repo clone plus `./setup`
- optional `--team` bootstrap and hook registration
- host detection and relink are first-class

### Artifact Inventory

- broad workflow skill library
- browser runtime binaries
- persistent state tree under `.gstack` and `~/.gstack`

### Architecture Map

- browser daemon
- command surface
- install and update control plane

### Workflow Surface

- large skill catalog
- explicit browser command layer
- memory and recovery skills

### State / Memory

- browser session state
- timeline, learnings, taste state
- checkpoints and git-backed recovery

## Appendix B: Code Hotspot Notes

### Bootstrap Hotspots

- `setup`
- `bin/gstack-config`
- `bin/gstack-update-check`
- `bin/gstack-team-init`
- `bin/gstack-settings-hook`
- `bin/gstack-relink`

### Runtime Hotspots

- `browse/src/config.ts`
- `browse/src/server.ts`
- `browse/src/browser-manager.ts`
- `browse/src/tab-session.ts`
- `browse/src/commands.ts`

### Memory Hotspots

- `bin/gstack-timeline-log`
- `bin/gstack-learnings-log`
- `bin/gstack-learnings-search`
- `bin/gstack-taste-update`

## Appendix C: Detailed Bootstrap Notes

### Setup Responsibilities

The `setup` script is doing much more than simple installation.

Observed responsibilities include:

- validating toolchain presence
- building browser-related binaries when stale
- persisting prefix settings
- relinking skills
- migrating direct Codex installs
- checking Chromium availability
- integrating optional team mode

This means `setup` is the real bootstrap spec for the product.

### Team Mode Responsibilities

`gstack-team-init` is worth treating as a second installer because it:

- edits repo policy
- injects hooks
- adds routing instructions
- can block work in required mode

This is a clear pattern for `harness-kit`: personal setup and repo adoption should probably be separate operations.

### Update Responsibilities

The update flow is not incidental.

Observed concerns:

- version awareness
- upgrade nags
- session-start update checks
- relinking after prefix/config changes

This gives `gstack` a maintenance story, not just a startup story.

## Appendix D: Detailed File Role Notes

- `setup`
  First file to read for install reality.
- `bin/gstack-config`
  Canonical settings read/write interface.
- `bin/gstack-update-check`
  Update policy and TTL logic.
- `bin/gstack-session-update`
  Ongoing maintenance path.
- `bin/gstack-team-init`
  Repo-level adoption and enforcement.
- `bin/gstack-settings-hook`
  Atomic SessionStart hook registration.
- `bin/gstack-relink`
  Skill materialization and repair.
- `browse/src/config.ts`
  `.gstack` path resolution and state root logic.
- `browse/src/server.ts`
  Single highest-yield runtime file for browser state writes.
- `browse/src/browser-manager.ts`
  Context continuity, cookies, restore.
- `browse/src/tab-session.ts`
  Per-tab refs and replay model.
- `browse/src/commands.ts`
  Action vocabulary definition.
- `browse/src/meta-commands.ts`
  Higher-order control commands.
- `browse/src/read-commands.ts`
  Non-mutating browser reads.
- `browse/src/write-commands.ts`
  Mutating browser operations.
- `browse/src/security.ts`
  Browser safety boundaries.
- `browse/src/audit.ts`
  Browser audit/logging support.
- `bin/gstack-timeline-log`
  Append-only project timeline writer.
- `bin/gstack-learnings-log`
  Durable learning writer.
- `bin/gstack-learnings-search`
  Durable learning retrieval.
- `bin/gstack-taste-update`
  Preference/taste persistence with decay.
- `learn/SKILL.md`
  High-level memory and learning surface.
- `context-save/SKILL.md`
  Checkpoint write semantics.
- `context-restore/SKILL.md`
  Checkpoint restore semantics.

## Evidence Map

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `docs/skills.md`
- `ARCHITECTURE.md`
- `BROWSER.md`
- `ETHOS.md`
- `CONTRIBUTING.md`
- `TODOS.md`
- `setup`
- `bin/gstack-config`
- `bin/gstack-update-check`
- `bin/gstack-session-update`
- `bin/gstack-team-init`
- `bin/gstack-settings-hook`
- `bin/gstack-relink`
- `browse/src/server.ts`
- `browse/src/browser-manager.ts`
- `browse/src/tab-session.ts`
- `browse/src/token-registry.ts`
- `browse/src/config.ts`
- `browse/src/commands.ts`
- `browse/src/meta-commands.ts`
- `browse/src/read-commands.ts`
- `browse/src/write-commands.ts`
- `browse/src/security.ts`
- `browse/src/audit.ts`
- `learn/SKILL.md`
- `context-save/SKILL.md`
- `context-restore/SKILL.md`
- `bin/gstack-timeline-log`
- `bin/gstack-learnings-log`
- `bin/gstack-learnings-search`
- `bin/gstack-taste-update`

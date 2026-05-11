---
title: superpowers
repo: https://github.com/obra/superpowers
source_repo: https://github.com/obra/superpowers
source_ref: b557648
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
status: reviewed
depth: dossier
---

# Superpowers Dossier

## Executive Summary

`superpowers` is a behavior-shaping methodology system with a small set of hard gates and a larger set of supporting skills, adapters, hooks, and transcript-backed tests. It is not just a library of prompts. Its real core is:

- bootstrap reachability
- a root dispatcher skill
- gated workflow skills
- transcript-based verification
- file-backed brainstorm state

For `harness-kit`, the most reusable lessons are:

- bootstrap early enough to affect the first turn
- encode lifecycle gates as files, not vibes
- verify through transcripts and explicit evidence
- keep host adapters thin

## Repository Positioning

The repo presents itself as a complete software development methodology for coding agents. The actual system shape supports that claim because it includes:

- core skills
- workflow control skills
- installation docs per host
- plugin manifests
- hooks
- runtime tests
- a small stateful companion server for brainstorming

That makes it a strong benchmark for:

- lifecycle discipline
- adapter strategy
- verification practices

and a weaker benchmark for:

- central memory substrate
- runtime state machine depth
- persistent task platform

## Source Snapshot

- Source repo: `https://github.com/obra/superpowers`
- Source ref: `b557648`
- Capture date: `2026-04-21`
- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- Host focus: Claude Code first, adapters elsewhere
- Primary languages: markdown skills, shell, JS adapter code, hook scripts
- Install surfaces: clone/symlink, plugin manifests, OpenCode plugin path, hooks

## Install And Bootstrap Trace

The install story is harness-specific, not generic.

### Claude / Codex Style Install

Observed flow:

1. clone repo
2. expose `skills/` in a known discovery path
3. restart the host so discovery reloads

This makes install more like filesystem bootstrap than package bootstrap.

### OpenCode Style Install

Observed flow:

1. point OpenCode config at the repo
2. let Bun load or reinstall the plugin
3. have the plugin inject:
   - skills path
   - bootstrap context through the OpenCode transform path

This is different in kind from the symlink path and proves that the repo already thinks in adapter terms.

### Hook-Based Bootstrap

Legacy or parallel bootstrap still exists through:

- `hooks/session-start`
- `hooks/run-hook.cmd`
- hook manifests for Claude/Cursor

This means bootstrap reachability is one of the most important operational concepts in the repo:

- if bootstrap fails, the methodology effectively disappears

## Artifact Inventory

| Artifact | Scope | Producer | Purpose | Notes |
|---|---|---|---|---|
| `skills/using-superpowers/SKILL.md` | core behavior | source | root dispatcher | activation gate |
| `skills/brainstorming/SKILL.md` | workflow control | source | pre-implementation design gate | one of the strongest gates |
| `skills/writing-plans/SKILL.md` | workflow control | source | exact implementation plans | artifact generation |
| `skills/subagent-driven-development/SKILL.md` | workflow control | source | same-session delegated execution | subagent loop |
| `skills/test-driven-development/SKILL.md` | workflow control | source | test-first implementation | engineering discipline |
| `skills/verification-before-completion/SKILL.md` | workflow control | source | evidence before closure | anti-self-report gate |
| `skills/using-git-worktrees/SKILL.md` | isolation | source | worktree bootstrap | clean workspace boundary |
| `skills/requesting-code-review/SKILL.md` | review | source | bounded review request | quality stage |
| `skills/receiving-code-review/SKILL.md` | review | source | review handling | critique discipline |
| `skills/finishing-a-development-branch/SKILL.md` | completion | source | merge/PR finish flow | branch closure |
| `commands/brainstorm.md` | compatibility shim | source | deprecated wrapper | points to skills |
| `commands/write-plan.md` | compatibility shim | source | deprecated wrapper | points to skills |
| `commands/execute-plan.md` | compatibility shim | source | deprecated wrapper | points to skills |
| `agents/code-reviewer.md` | compatibility shim | source | review wrapper | still supported |
| `.claude-plugin/plugin.json` | host manifest | source | Claude plugin registration | install contract |
| `.cursor-plugin/plugin.json` | host manifest | source | Cursor plugin registration | install contract |
| `.opencode/plugins/superpowers.js` | adapter | source | OpenCode bootstrap and transform-based context injection | code-driven bootstrap |
| `hooks/hooks.json` | hook manifest | source | SessionStart mapping | reachability |
| `hooks/run-hook.cmd` | Windows bridge | source | shell compatibility | cross-platform |
| `skills/brainstorming/scripts/server.cjs` | stateful companion | source | brainstorm server | file-backed state |
| `tests/skill-triggering/*` | tests | source | trigger verification | transcript-backed behavior |
| `docs/testing.md` | test contract | source | integration-testing guidance | verification model |

## Architecture Map

| Area | Key paths | Responsibility | Why it matters |
|---|---|---|---|
| bootstrap/adaptation | `README.md`, `.codex/INSTALL.md`, `docs/README.codex.md`, `docs/README.opencode.md`, `hooks/session-start`, `.opencode/plugins/superpowers.js` | host-specific startup | determines reachability |
| root skill dispatcher | `skills/using-superpowers/SKILL.md` | skill priority and activation | central policy gate |
| lifecycle gate set | brainstorming, writing-plans, TDD, verification, subagent-driven-dev, finishing branch | staged engineering method | actual methodology core |
| review system | request/receive review skills, agent wrapper | critique loop | quality boundary |
| workspace isolation | `skills/using-git-worktrees/SKILL.md` | clean workspace creation | prevents dirty execution |
| brainstorm companion | `skills/brainstorming/scripts/*` | file-backed brainstorm state | only obvious runtime state |
| manifests and hooks | plugin manifests, hook manifests, `run-hook.cmd` | adapter registration | host bootstrap correctness |
| test harness | `tests/**`, `docs/testing.md` | transcript-based verification | evidence culture |

## Workflow Surface

The workflow surface is a fixed pipeline with hard gates.

### Canonical Flow

Observed stages:

1. brainstorm
2. isolate workspace
3. write plan
4. execute plan with subagents or checkpoints
5. use TDD
6. request review
7. receive review and fix
8. verify before completion
9. finish development branch

This is much more explicit than “use good engineering habits.”

### Why This Matters

Each stage:

- has a file-backed skill
- has a clear artifact expectation
- blocks the next stage when necessary

That is exactly the kind of behavior `harness-kit` needs to encode.

### Workflow Components

| Component | Role | Why it matters |
|---|---|---|
| `brainstorming` | design/spec gate | prevents implementation before design |
| `using-git-worktrees` | workspace isolation | protects clean execution |
| `writing-plans` | exact task plan | operational artifact |
| `subagent-driven-development` | same-session delegation loop | compounding execution |
| `test-driven-development` | test-first implementation | behavior discipline |
| `requesting-code-review` | external critique stage | explicit review gate |
| `receiving-code-review` | critique handling | avoids performative compliance |
| `verification-before-completion` | final evidence gate | distrust self-report |
| `finishing-a-development-branch` | branch completion | structured exit |

## State, Memory, And Compounding

`superpowers` has less central runtime state than a platform like OpenHarness, but more file-backed operational state than a pure prompt pack.

### Session Bootstrap Memory

Observed:

- SessionStart hook injects `using-superpowers`
- OpenCode plugin injects bootstrap context through the transform path
- Codex docs rely on filesystem skill discovery

This suggests a file/bootstrap-driven memory model rather than a service-backed memory model.

Known gap at the current dossier depth:

- the OpenCode mechanism should be read as transform-based bootstrap context injection, not a stronger guarantee about full first-message rewrite semantics

### File-Backed Brainstorm State

The main obvious runtime state is under the brainstorming companion:

- per-session directories
- content files
- state/events
- pid/log files
- persistent `.superpowers/brainstorm/` dirs

This is important because it proves there is at least one real durable state path, not just static docs.

### Compounding Model

Compounding appears to come from:

- versioned methodology files
- self-contained plans
- repeated review gates
- transcript-backed verification
- repeated subagent task extraction and review loops

This is compounding through artifacts and discipline rather than through a dedicated memory database.

## Verification, Permissions, And Recovery

The most important verification lesson in `superpowers` is: do not trust the agent’s own claim that it is done.

### Verification Surfaces

- `verification-before-completion`
- `docs/testing.md`
- transcript-based integration tests
- hook-based bootstrap checks

### Why This Matters

The repo verifies:

- skill triggering
- bootstrap injection
- session behavior
- subagent workflow behavior

through tests and logs rather than through prose alone.

### Recovery Surfaces

Recovery is lighter than in a runtime platform, but still present through:

- restart/reload via bootstrap
- plan re-entry through written plans
- worktree isolation
- review-driven correction
- brainstorm session state

## Code Hotspots

| File | Why it matters | Key concept |
|---|---|---|
| `hooks/session-start` | first-hop bootstrap injection | session bootstrap |
| `hooks/run-hook.cmd` | Windows compatibility | cross-platform reachability |
| `.opencode/plugins/superpowers.js` | OpenCode bootstrap and transform-based context injection | adapter-driven startup |
| `skills/using-superpowers/SKILL.md` | root dispatcher and priority model | central policy gate |
| `skills/using-git-worktrees/SKILL.md` | isolation gate | workspace hygiene |
| `skills/writing-plans/SKILL.md` | exact plan generation | artifact discipline |
| `skills/subagent-driven-development/SKILL.md` | same-session delegation loop | compounding work execution |
| `skills/requesting-code-review/SKILL.md` | review request contract | quality gate |
| `skills/verification-before-completion/SKILL.md` | final evidence requirement | anti-self-report |
| `skills/finishing-a-development-branch/SKILL.md` | completion boundary | exit discipline |
| `skills/brainstorming/scripts/start-server.sh` | brainstorm session bootstrap | file-backed state |
| `skills/brainstorming/scripts/server.cjs` | event and state writes | persistent brainstorm memory |
| `skills/brainstorming/scripts/stop-server.sh` | retention semantics | durable vs temp cleanup |
| `hooks/hooks.json` | SessionStart registration | bootstrap reachability |
| `.claude-plugin/plugin.json` | plugin registration | host install contract |
| `.cursor-plugin/plugin.json` | Cursor registration | host install contract |
| `docs/testing.md` | transcript-based verification contract | evidence discipline |

## Design Lessons For Harness Kit

### What To Steal

- hard-gated lifecycle stages
- bootstrap that runs before the first meaningful response
- transcript-backed verification
- thin host adapters over a shared method
- file-backed operational state where needed

### What Not To Steal

- overly sharp contributor rhetoric unless intentional
- large core support for project-specific or personal customizations
- pretending a full semantic memory layer exists when the system is actually file/bootstrap driven

### Unclear Or Conditional Lessons

- the brainstorm companion server is useful, but `harness-kit` may not need a server at all if dossier/spec state can stay static
- OpenCode plugin behavior and legacy hook behavior may still be transitional rather than a final architecture

## Open Questions

- Does `superpowers` need a real memory subsystem, or is file-backed compounding enough for its design?
- Are manifests generated from one source or maintained separately?
- How much hidden state exists outside the brainstorm server path?

## Appendix A: Structure Pass Notes

### Install / Bootstrap

- Claude/Codex style install is repo clone plus skill exposure and restart
- OpenCode uses plugin bootstrap and transform-based context injection
- SessionStart hooks still exist for some hosts
- manifests declare behavior per harness

### Artifact Inventory

- 14 core skills
- compatibility shims
- operational docs
- host manifests
- test suite with 47 files

### Architecture Map

- bootstrap/adaptation layer
- core skill dispatcher
- workflow control skills
- stateful brainstorm companion

### Workflow Surface

- brainstorm to spec
- worktree isolation
- plan writing
- subagent execution
- review and verification
- TDD and debugging

### State / Memory

- session bootstrap memory from hooks and transform-based context injection
- file-backed brainstorm state
- compounding through plans, reviews, and transcript verification

## Appendix B: Code Hotspot Notes

### Bootstrap Hotspots

- `hooks/session-start`
- `hooks/run-hook.cmd`
- `.opencode/plugins/superpowers.js`
- `hooks/hooks.json`
- `.claude-plugin/plugin.json`
- `.cursor-plugin/plugin.json`

### Workflow Gate Hotspots

- `skills/using-superpowers/SKILL.md`
- `skills/using-git-worktrees/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `skills/finishing-a-development-branch/SKILL.md`

### State / Verification Hotspots

- `skills/brainstorming/scripts/start-server.sh`
- `skills/brainstorming/scripts/server.cjs`
- `skills/brainstorming/scripts/stop-server.sh`
- `docs/testing.md`

## Appendix C: Detailed Bootstrap Notes

### Claude / Codex Path

This path is primarily filesystem-based:

- clone repo
- expose skills path
- restart discovery

The simplicity is deceptive. The actual behavior still depends on:

- where the host looks for skills
- whether bootstrap instructions run at session start

### OpenCode Path

This path is materially different:

- plugin code runs
- skills path is registered
- bootstrap text is injected into the first user message

That makes OpenCode a stronger adapter example than the symlink path.

### Hook Path

The legacy or compatibility hook path matters because it preserves:

- Claude/Cursor SessionStart injection
- Windows bridge compatibility
- a host-agnostic bootstrap fallback

Even if `harness-kit` chooses not to support all of these, this is a useful example of layered reachability.

## Appendix D: Detailed File Role Notes

- `hooks/session-start`
  Most important hook entrypoint. If this fails, the system may silently degrade.
- `hooks/run-hook.cmd`
  Required for Windows/CMD compatibility.
- `.opencode/plugins/superpowers.js`
  Best file for understanding adapter-driven bootstrap.
- `.claude-plugin/plugin.json`
  Best file for Claude registration.
- `.cursor-plugin/plugin.json`
  Best file for Cursor registration.
- `hooks/hooks.json`
  Best file for SessionStart routing in Claude-like flows.
- `hooks/hooks-cursor.json`
  Best file for Cursor hook mapping.
- `skills/using-superpowers/SKILL.md`
  Root dispatcher and policy entrypoint.
- `skills/brainstorming/SKILL.md`
  Design gate and first lifecycle barrier.
- `skills/using-git-worktrees/SKILL.md`
  Isolation primitive.
- `skills/writing-plans/SKILL.md`
  Plan artifact generator.
- `skills/subagent-driven-development/SKILL.md`
  Same-session delegation loop.
- `skills/test-driven-development/SKILL.md`
  Test-first implementation policy.
- `skills/requesting-code-review/SKILL.md`
  Review request contract.
- `skills/receiving-code-review/SKILL.md`
  Review handling contract.
- `skills/verification-before-completion/SKILL.md`
  Anti-self-report completion gate.
- `skills/finishing-a-development-branch/SKILL.md`
  Exit discipline.
- `skills/brainstorming/scripts/start-server.sh`
  Creates persistent and temp brainstorm state.
- `skills/brainstorming/scripts/server.cjs`
  Appends events and serves content/state.
- `skills/brainstorming/scripts/stop-server.sh`
  Encodes retention semantics.
- `docs/testing.md`
  Strongest verification document in the repo.

## Appendix E: High-Yield Follow-Up Questions

- What exact transcript assertions do `tests/opencode/*` make about bootstrap reachability?
- What exact Claude Code session transcripts are used to confirm skill triggering?
- Are `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json` generated from a common source or manually mirrored?
- Is the brainstorm companion the only true runtime state, or do some tests create other durable state files?
- Which skills are truly mandatory versus just commonly co-triggered in practice?

## Appendix F: Why This Repo Matters Even Without A Memory Service

`superpowers` is a useful reminder that compounding does not require a central database.

It compounds through:

- session bootstrap reinjection
- self-contained plans
- isolated worktrees
- explicit review loops
- transcript-backed verification
- versioned methodology files

That is relevant to `harness-kit` because a strong v1 may not need more than:

- good bootstrap
- durable files
- verification gates
- clean workflow boundaries

## Evidence Map

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `.codex/INSTALL.md`
- `docs/README.codex.md`
- `docs/README.opencode.md`
- `docs/testing.md`
- `docs/windows/polyglot-hooks.md`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.cursor-plugin/plugin.json`
- `.opencode/plugins/superpowers.js`
- `hooks/hooks.json`
- `hooks/hooks-cursor.json`
- `hooks/session-start`
- `hooks/run-hook.cmd`
- `skills/using-superpowers/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/test-driven-development/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `skills/using-git-worktrees/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/finishing-a-development-branch/SKILL.md`
- `skills/dispatching-parallel-agents/SKILL.md`
- `skills/brainstorming/scripts/start-server.sh`
- `skills/brainstorming/scripts/server.cjs`
- `skills/brainstorming/scripts/stop-server.sh`
- `tests/brainstorm-server/*`
- `tests/claude-code/*`
- `tests/explicit-skill-requests/*`
- `tests/opencode/*`
- `tests/skill-triggering/*`
- `tests/subagent-driven-dev/*`

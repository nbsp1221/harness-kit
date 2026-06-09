---
last_reviewed: 2026-04-21
source_pass: 2026-04-21-first-pass
---

# Research Overview

## Decision Frame

`wayrail` is not trying to become the biggest open harness platform.

The current target is narrower:

- standardize new project startup
- define a project-local agent contract
- define common verification gates
- preserve enough structure that future agent work is legible

That means the relevant benchmark question is not "which project is most impressive?" It is "which project best informs a lean internal harness starter with a strong local contract?"

## Candidate Summary

- `compound-engineering-plugin`: best benchmark for staged methodology and artifact handoff
- `gstack`: best benchmark for durable state, rich routing, QA, and learned history
- `superpowers`: best benchmark for hard-gated process skills and host adapters
- `oh-my-codex`: best benchmark for Codex-native state authority and operational control
- `Archon`: best benchmark for deterministic workflow modeling and overlay precedence
- `OpenHarness`: best benchmark for runtime substrate, profiles, permissions, and markdown-first memory

## Current Ranking For Wayrail

This ranking is provisional and judgment-based. It is informed by the first evidence pass, but it is not a numeric result.

Rubric used for ordering:

- highest weight: fit for a lean internal starter
- high weight: usefulness for project bootstrap and agent contract design
- medium weight: usefulness for verification and compounding design
- penalty: runtime heaviness that would likely push `wayrail` past v1 scope
- penalty: host-specific baggage that would leak into the core contract

1. `compound-engineering-plugin`
2. `oh-my-codex`
3. `Archon`
4. `gstack`
5. `superpowers`
6. `OpenHarness`

## Why This Ranking Exists

### 1. Compound Engineering Plugin

It is closest to the actual problem shape: staged work, artifact handoffs, setup as a first-class action, and compounding as a discipline. It is weaker as a runtime benchmark than it first appears, which is actually useful because `wayrail` v1 also should not start as a full runtime.

### 2. Oh My Codex

It is the best Codex-specific benchmark in the current set and offers the clearest operational lessons here for local-first state, setup boundaries, hook ownership, and compounding through state plus wiki files.

### 3. Archon

It is broader than `wayrail` v1, but it is the best reference in this pass for deterministic workflows, validation, lifecycle operations, and bundled < global < project config precedence.

### 4. gstack

It offers very strong ideas around staged routing, QA, browser-backed control, and append-only learnings. It ranks lower because the surface is larger and more opinionated than a minimal starter needs.

### 5. Superpowers

It is highly influential and very useful, but mostly as a source of process patterns and adapter ideas. It is less directly useful as a template for a small internal starter because of its breadth and strong contributor culture.

### 6. OpenHarness

It is the broadest runtime substrate in the target set. That makes it valuable architecturally, but it is less directly aligned with `wayrail`'s immediate goal than the others.

## Cross-Cutting Patterns Worth Carrying Forward

- explicit stage boundaries with artifact handoffs
- separation between setup-time bootstrap and runtime behavior
- bundled defaults plus optional higher-level overlays
- tool-gated control instead of trust-based completion
- local-first durable state and markdown-backed compounding

## Patterns To Reject Early

- full runtime platform ambitions in v1
- very large role catalogs as the default user experience
- implicit completion claims without transcript or verification evidence
- broad compatibility layers without a removal plan
- copying host-specific baggage into the core contract

## Working Synthesis

Current best synthesis for `wayrail`:

- take staged lifecycle language from `compound-engineering-plugin`
- take Codex-native setup, state authority, and local wiki ideas from `oh-my-codex`
- take transition and precedence discipline from `Archon`
- take selected persistent learning and QA patterns from `gstack`
- take hard-gated process stages and adapter discipline from `superpowers`
- take profile, permission, and markdown-memory ideas from `OpenHarness`

## Next Step

Run a bounded review pass on the drafted research docs, then freeze the first-pass benchmark conclusions and convert them into a concrete `wayrail` v1 architecture direction.

## Source Notes

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- Quick judgment lives in `docs/research/summaries/`
- Deep evidence lives in `docs/research/dossiers/`

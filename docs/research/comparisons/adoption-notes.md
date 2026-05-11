---
last_reviewed: 2026-04-21
source_pass: 2026-04-21-first-pass
---

# Adoption Notes

This document captures what `harness-kit` is likely to adopt, defer, or reject after the first full research pass.

## Likely V1 Inclusions

- `core v1`: a project bootstrap entry point
- `core v1`: a project-local agent contract
- `core v1`: staged lifecycle documents with named handoff artifacts
- `core v1`: standard verification commands and completion gates
- `core v1`: lightweight durable learnings or checkpoints
- `core v1`: a narrow config precedence model

## Strongest Direct Inspirations

### From Compound Engineering Plugin

- `core v1`: staged lifecycle with explicit artifact boundaries
- `core v1`: setup as a first-class action
- `core v1`: compounding as a durable habit, not an afterthought
- `core v1`: manifest-backed install and cleanup discipline

### From Oh My Codex

- `core v1`: explicit state authority
- `core v1`: project-local versus global boundary clarity
- `core v1`: setup plus doctor semantics, with clear distinction between install sanity and execution readiness
- `conceptual inspiration`: local wiki or local state compounding

### From Archon

- `conceptual inspiration`: explicit workflow nodes and transitions
- `core v1`: bundled < global < project precedence
- `core v1`: validate-before-run or validate-before-save discipline
- `defer`: lifecycle operations such as resume, abandon, and rerun

## Likely Partial Inclusions

### From gstack

- `conceptual inspiration`: selected QA and ship stage language
- `core v1`: append-only learnings and checkpoints
- `conceptual inspiration`: deterministic host-aware bootstrap ideas

### From Superpowers

- `core v1`: hard-gated lifecycle stages
- `core v1`: transcript-backed verification discipline
- `conceptual inspiration`: thin host adapters over a shared method

### From OpenHarness

- `defer`: profile and auth separation
- `conceptual inspiration`: tool-gated permissions
- `conceptual inspiration`: markdown-first memory patterns

## Likely Exclusions For V1

- full agent-team runtime
- TUI, dashboard, or broad control-plane UI
- database-backed execution history
- large default role catalogs
- browser daemon and security surface
- broad multi-host compatibility before the core local contract is stable

## Current Working Product Boundary

`harness-kit` v1 should behave like a project starter and contract layer, not like a complete agent runtime platform.

That means it should:

- create or standardize files
- encode rules
- define workflow checkpoints
- make verification explicit
- capture lightweight durable learnings

It should not yet try to own:

- full background task orchestration
- long-running agent teams
- generalized multi-model runtime management
- remote dashboards or web control planes
- persistent database-backed workflow history

## Concrete Design Pressure From The Research

- `compound-engineering-plugin` pressures `harness-kit` to keep lifecycle stages distinct
- `oh-my-codex` pressures `harness-kit` to make state authority explicit
- `Archon` pressures `harness-kit` to define config precedence early
- `gstack` pressures `harness-kit` to avoid ephemeral-only session memory
- `superpowers` pressures `harness-kit` to distrust agent self-report
- `OpenHarness` pressures `harness-kit` to gate tools before trusting outer UX layers

## Questions To Resolve Before V1 Scope Freezes

- Should `harness-kit` ship any hooks in v1, or only describe hook points?
- Should bootstrap create only docs and contracts, or also runnable scripts and checks?
- Should the initial workflow be Codex-first or host-agnostic with a Codex adapter first?
- What is the smallest compounding mechanism worth shipping: learnings log, wiki, checkpoint file, or all three?
- How much global config should exist before a repo-local starter becomes too runtime-like?

## Source Notes

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- Adoption judgments are synthesized from the target reports and remain provisional until the `harness-kit` v1 architecture is written.

---
title: oh-my-codex
repo: https://github.com/Yeachan-Heo/oh-my-codex
source_repo: https://github.com/Yeachan-Heo/oh-my-codex
source_ref: d56148c
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
category: orchestration-layer
status: reviewed
last_reviewed: 2026-04-21
priority: high
fit_for_harness_kit: high
host_focus:
  - codex
---

# Oh My Codex

## Summary

In this first research pass, `oh-my-codex` looks like the most directly relevant Codex-oriented orchestration layer for `wayrail`. It is not a standalone agent platform. It is a workflow and control layer around Codex CLI with strong ideas about state authority, setup boundaries, hook ownership, and local compounding.

## Why It Matters

- `wayrail` will likely live in a Codex-heavy workflow.
- It provides concrete examples of Codex-native hooks, runtime fallbacks, and project-local versus global state.
- It offers a clear local-first state and compounding model.

## Snapshot

- Repository: `Yeachan-Heo/oh-my-codex`
- Source ref: `d56148c`
- Primary positioning: workflow and orchestration layer for Codex
- Host focus: Codex
- Approximate scale: large public Codex ecosystem project
- Maintenance signal: high
- Install surface: CLI, setup, doctor, teams, prompts, skills, hooks, and generated config

## Core Thesis

Codex should not run as a bare chat loop. It should run inside an operational layer with explicit mode transitions, setup and diagnostics, hook ownership, durable local state, and repeatable workflows.

## Architecture

Important architectural areas:

- `README.md` and `docs/readme/README.md` establish the product framing
- `docs/codex-native-hooks.md` describes native hook mapping and control ownership
- `docs/STATE_MODEL.md` defines state authority and lifecycle semantics
- `src/state/**` implements transitions, reconciliation, and operational state
- `src/config/generator.ts` shows generated setup and config scaffolding
- `docs/reference/project-wiki.md` shows the local compounding and wiki model

## Workflow Model

Workflow control is explicit and mode-driven, with allowlisted handoffs and hard denials across incompatible states.

Observed strengths:

- clear transition model
- explicit reset or clear behavior
- state reconciliation instead of silent rollback
- operational concepts for stuck or stale sessions

This is the cleanest target in the set for studying deterministic mode transitions in a Codex environment.

## Bootstrap Model

Bootstrap is split between global or user install-time config and project-local runtime state.

Observed patterns:

- install-time scaffolding under the Codex environment
- project-local state under `.omx`
- generated hooks and config that still preserve user-managed entries
- a `doctor` concept for install sanity checks

Important caveat: the repo itself warns, implicitly and explicitly, that `doctor` is not the same thing as authenticated execution readiness.

## Verification And Control

The strongest control patterns are:

- native-hook plus runtime-fallback split
- explicit state authority and clears
- safer launch and resume behavior
- operational diagnostics that distinguish setup correctness from runtime correctness

This is useful because `wayrail` will likely need its own version of “what is installed” versus “what is actually ready to run.”

## Memory And Compounding

Memory and compounding are file-backed, local-first, and session-scoped.

Observed patterns:

- authority in `.omx/state`
- local project wiki in `.omx/wiki`
- compatibility layers kept visible rather than hidden

This is a strong fit for a local harness because it avoids pretending that compounding requires a heavyweight remote memory service.

## Strengths

- Strong Codex relevance
- Clear operational focus
- One of the best examples of explicit state authority in the target set
- Good reference for project-local versus user-global boundary decisions

## Weaknesses

- Runtime-heavy relative to a lean starter
- Team features may exceed immediate v1 needs
- Can pull in tmux and Codex-specific operational baggage too early
- Compatibility layers can become permanent debt if copied without pruning

## What To Steal

- session-scoped authoritative state with explicit clear and tombstone behavior
- native-hook plus runtime-fallback split
- setup that owns generated hooks and config while preserving user-managed entries
- markdown-first local wiki compounding

## What Not To Steal

- tight coupling to tmux or Codex launch paths
- treating `doctor` as a readiness guarantee
- long-lived compatibility scaffolding without a removal plan
- OMX-specific role vocabulary as a generic harness abstraction

## Open Questions

- Should `wayrail` depend on the `.codex` bootstrap layer at all, or keep its own install surface isolated?
- Does `wayrail` need a wiki-like compounding layer, or only lifecycle semantics and state?
- Which compatibility layers in OMX are migration-only versus worth preserving?

## Evidence

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `docs/readme/README.md`
- `docs/codex-native-hooks.md`
- `docs/prompt-guidance-contract.md`
- `docs/STATE_MODEL.md`
- `docs/migration-mainline-post-v0.4.4.md`
- `docs/reference/project-wiki.md`
- `docs/reference/ralph-parity-matrix.md`
- `src/config/generator.ts`
- `src/state/workflow-transition.ts`
- `src/state/workflow-transition-reconcile.ts`
- `src/state/operations.ts`
- `src/mcp/state-server.ts`

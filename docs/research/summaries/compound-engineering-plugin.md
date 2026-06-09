---
title: compound-engineering-plugin
repo: https://github.com/EveryInc/compound-engineering-plugin
source_repo: https://github.com/EveryInc/compound-engineering-plugin
source_ref: 4c57508
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
category: methodology-plugin
status: reviewed
last_reviewed: 2026-04-21
priority: high
fit_for_harness_kit: high
host_focus:
  - claude-code
  - codex
  - cursor
---

# Compound Engineering Plugin

## Summary

In this first research pass, `compound-engineering-plugin` looks like the best methodology benchmark for `wayrail`, but it is not a full runtime. The repo is best understood as a cross-harness plugin and conversion layer that packages a staged development method for multiple hosts. The most valuable parts for `wayrail` are its explicit stage separation, artifact handoffs, manifest-backed installation, and cleanup discipline.

## Why It Matters

- It maps closely to the problem `wayrail` is trying to solve: standardize project startup and ongoing agent work.
- It emphasizes durable learning capture instead of one-off session output.
- It is a strong example of a cross-host methodology plugin rather than a single-host runtime.

## Snapshot

- Repository: `EveryInc/compound-engineering-plugin`
- Source ref: `4c57508`
- Primary positioning: official compound engineering plugin plus host conversion layer
- Host focus: Claude Code, Codex, Cursor, Copilot CLI, and other adapters
- Approximate scale: large public project with active recent releases
- Maintenance signal: high
- Install surface: plugin install, host-specific manifests, target-specific cleanup and conversion

## Core Thesis

The harness should make each engineering task improve the next one through explicit stage boundaries and durable artifacts. The repo does not try to own the whole execution runtime. Instead, it packages a workflow model and distributes it safely across multiple host environments.

## Architecture

Important architectural areas:

- `README.md` establishes the staged method and cross-host framing.
- `src/index.ts` and `src/commands/install.ts` position the repo as an install and conversion surface.
- `src/targets/codex.ts` shows host-specific adaptation logic.
- `src/commands/cleanup.ts` and `tests/manifest-path-safety.test.ts` show that install hygiene and path containment are first-class concerns.
- `docs/solutions/**` contains much of the real operating knowledge, including workflow and compounding rationale.

## Workflow Model

The workflow model is intentionally split by artifact type and information type:

- brainstorm
- plan
- work
- review
- resolve or cleanup
- compound or refresh learnings

The key takeaway is not only the names of the stages, but the insistence that each stage produces a different kind of artifact. Brainstorming is for product or problem context. Planning is for implementation context. Work is execution. Review and resolve are defensive stages.

## Bootstrap Model

Bootstrap is target-specific and manifest-driven rather than runtime-centric.

Observed patterns:

- native install paths per host
- cleanup for stale artifacts
- special handling for Codex and other targets
- path-safety checks to avoid unsafe writes during install

This matters because `wayrail` will likely need a similar distinction between reusable method assets, host adapter surfaces, repo-local generated files, and cleanup or migration behavior.

## Verification And Control

The repo's control model is strongest at packaging and workflow boundaries:

- install logic is explicit and target-aware
- manifest paths are tested
- cleanup is a first-class command
- the pipeline model keeps stage transitions deliberate rather than vague

The main verification insight for `wayrail` is that host conversion and file installation should be treated as real engineering surfaces with tests, not as side scripts around the “real” product.

## Memory And Compounding

The compounding story is partly real and partly aspirational.

What is clearly present:

- structured learnings captured in docs
- workflow notes about todo and pipeline lifecycle
- explicit discussion of compounding refresh

What is not clearly present in this pass:

- a visible standalone runtime memory service

That means `wayrail` should copy the habit of durable learnings and structured artifacts, but should not assume this repo already proves a full memory substrate design.

## Strengths

- Strong alignment with `wayrail` on staged lifecycle design
- Cross-host packaging discipline is useful for long-term portability
- Manifest-backed install and cleanup behavior are more mature than most prompt-pack projects
- Good separation between product context, implementation context, execution, and cleanup

## Weaknesses

- Easy to mistake for a full runtime when it is better used as a methodology and packaging benchmark
- Compounding appears more document- and practice-based than substrate-based
- Shared-root ownership patterns for installed artifacts can create shadowing risk if copied blindly

## What To Steal

- explicit stage separation with artifact handoffs
- manifest-backed install and cleanup
- path-containment and path-safety checks
- cross-host adapter mindset without forcing one runtime
- structured compounding documents and refresh habits

## What Not To Steal

- broad shared-root artifact ownership patterns
- assuming documented compounding equals a native memory substrate
- converting to many hosts before the core local contract is stable

## Open Questions

- Is the auto-memory direction still proposal-level or shipping somewhere deeper in the repo?
- What is the smallest subset that preserves the value for `wayrail` v1?
- Which parts should become repo-local generated files versus global host adapter assets?

## Evidence

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `src/index.ts`
- `src/commands/install.ts`
- `src/commands/cleanup.ts`
- `src/targets/codex.ts`
- `tests/manifest-path-safety.test.ts`
- `docs/solutions/integrations/native-plugin-install-strategy-2026-04-19.md`
- `docs/solutions/skill-design/research-agent-pipeline-separation-2026-04-05.md`
- `docs/solutions/best-practices/ce-pipeline-end-to-end-learnings-2026-04-17.md`
- `docs/brainstorms/2026-03-18-auto-memory-integration-requirements.md`
- `docs/solutions/skill-design/compound-refresh-skill-improvements.md`

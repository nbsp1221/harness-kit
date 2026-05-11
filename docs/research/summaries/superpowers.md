---
title: superpowers
repo: https://github.com/obra/superpowers
source_repo: https://github.com/obra/superpowers
source_ref: b557648
capture_date: 2026-04-21
source_pass: 2026-04-21-first-pass
category: skills-framework
status: reviewed
last_reviewed: 2026-04-21
priority: high
fit_for_harness_kit: medium
host_focus:
  - claude-code
  - codex
---

# Superpowers

## Summary

In this first research pass, `superpowers` looks like a development methodology and skills framework, not a loose prompt pack. It matters because it encodes a hard-gated lifecycle for coding agents and uses harness-specific adapters, hooks, transcript checks, and versioned files to shape behavior.

## Why It Matters

- It is a large public system in this area.
- It provides a mature example of process skill composition and workflow enforcement.
- It reveals both what `harness-kit` should adopt and what it should leave to adapters or future extensions.

## Snapshot

- Repository: `obra/superpowers`
- Source ref: `b557648`
- Primary positioning: end-to-end coding-agent methodology and skill system
- Host focus: Claude Code first, expanding parity elsewhere
- Approximate scale: large public project
- Maintenance signal: high
- Install surface: host-specific plugin manifests, install docs, hooks, and adapter scripts

## Core Thesis

A coding agent should follow a disciplined lifecycle with hard gates and named artifacts. The harness is valuable when it changes behavior early, before the first response, and when completion claims are checked against transcripts and verification evidence.

## Architecture

Important architectural areas:

- `README.md` and `CLAUDE.md` define the overall methodology and contributor contract
- process-critical skills live in `skills/brainstorming`, `skills/writing-plans`, `skills/subagent-driven-development`, `skills/test-driven-development`, and `skills/verification-before-completion`
- host-specific installation lives in plugin manifests and docs such as `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `docs/README.codex.md`
- hooks and runtime injection surfaces live in `hooks/hooks.json` and adapter files such as `.opencode/plugins/superpowers.js`

## Workflow Model

The workflow is a fixed pipeline with hard gates:

- brainstorm
- isolate workspace
- write a plan
- execute with subagents or checkpoints
- use TDD
- review
- verify before completion
- finish the development branch

The key lesson for `harness-kit` is to encode a small number of hard stage boundaries with named artifacts and to refuse to skip them casually.

## Bootstrap Model

Bootstrap is harness-specific and adapter-driven, not only README-driven.

Observed patterns:

- plugin manifests per host
- codex-specific and opencode-specific install docs
- hooks that inject context or enforce checks
- adapter code that translates the core method into host semantics

This suggests `harness-kit` should have a thin adapter layer per host rather than pretending one install story fits every runtime.

## Verification And Control

Verification and control are stronger than the repo first appears.

Observed mechanisms:

- transcript and runtime checks
- hard-gated skills
- verification-before-completion discipline
- hooks that enforce behavior around lifecycle events
- tests around skill triggering

The strong pattern here is “do not trust the agent’s self-report.” That is directly relevant to `harness-kit`.

## Memory And Compounding

Compounding is mostly file- and git-backed.

Observed patterns:

- versioned methodology files
- release notes and update flow
- context reinjection patterns in host docs

This is valuable, but it is not the same as a native semantic memory layer. `harness-kit` should not pretend otherwise.

## Strengths

- Strong example of codifying software-engineering discipline for agents
- Good source for small numbers of hard-gated lifecycle stages
- Strong evidence culture around behavior-shaping changes
- Good example of thin host adapters over a shared method

## Weaknesses

- Very broad surface area
- Easy to over-import and create a bloated local system
- Some docs and runtime surfaces can drift if not derived or tested together
- Contributor tone is sharper than `harness-kit` likely needs

## What To Steal

- a small number of hard-gated lifecycle stages
- harness-specific bootstrap adapters
- transcript-backed or log-backed verification before declaring success
- git-backed compounding and drift-aware updates
- eval expectations for behavior-shaping documentation changes

## What Not To Steal

- the aggressive contributor voice unless intentionally chosen
- built-in support for every project-specific customization in core
- assuming a semantic memory layer exists when the design is really file-backed compounding

## Open Questions

- Does `harness-kit` need a real memory API or is file-backed compounding enough for v1?
- How many adapters should exist at launch?
- Should adapter docs be generated or tested against manifests to avoid drift?

## Evidence

- Source pass: [2026-04-21 First Pass](../passes/2026-04-21-first-pass.md)
- `README.md`
- `CLAUDE.md`
- `skills/brainstorming/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/test-driven-development/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `docs/README.codex.md`
- `docs/README.opencode.md`
- `.claude-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `hooks/hooks.json`
- `.opencode/plugins/superpowers.js`
- `tests/skill-triggering/run-test.sh`
- `RELEASE-NOTES.md`

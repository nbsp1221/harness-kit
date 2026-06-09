---
name: wr-verify
description: "Use when converting an implemented wayrail spec item into verification.md evidence. Reads a selected spec item, checks Implementation Handoff readiness, runs planned verification checks fresh, records concise evidence, and writes only verification.md. Do not use for code implementation, fixing tests, review conclusions, waiver approval, creating tasks.md, or editing spec.md/plan.md."
---

# wr-verify

Create verification evidence for an implemented wayrail spec item.

## Use When

- The user asks to run `wr-verify`, verify completed implementation, or move an implemented wayrail spec item from implementation to verification.
- The input includes an explicit spec item path or an unambiguous current spec item from the conversation.
- The target spec item has `spec.md`, `plan.md`, and `verification.md`.

## Do Not Use When

- The user asks to start a new spec item; use `wr-spec`.
- The user asks to create an implementation plan; use `wr-plan`.
- The user asks for code implementation, code fixes, or fixing tests.
- The user asks for review conclusions or review approval.
- The plan is not ready for implementation.
- Implementation has not been reported or observed.
- The request would approve waivers, accept risk, or create `tasks.md`.

## Inputs

Prefer an explicit spec item path such as `specs/<id>/spec.md`.
If the conversation has exactly one unambiguous current spec item, use that path and state it.
If neither is available, ask for the spec path.

## Readiness Gate

Read `spec.md` and read `plan.md` before writing anything.
Check `Implementation Handoff` in `plan.md`.
Stop without writing successful verification when the handoff is not `Ready for implementation`, when implementation has not been reported or observed, or when required planned checks are too ambiguous to run or classify.

## Workflow

1. Identify the target spec item.
2. Read `spec.md`.
3. Read `plan.md`.
4. Confirm the readiness gate.
5. Extract planned verification checks, expected outcomes, requirement links, implementation-unit links, and manual validation expectations from `plan.md`.
6. Assign check IDs such as `V1`, `V2`, and `V3` when the plan does not already provide them.
7. Read existing `verification.md` before writing.
8. If existing `verification.md` has meaningful non-stub content, do not overwrite it unless the user explicitly asks to replace or revise the evidence.
9. Derive commands in this order:
   - planned verification checks from `plan.md`
   - repository guidance such as `AGENTS.md`
   - standard project scripts only when they verify the same claim
10. Apply the command safety gate before execution.
11. Run each planned verification check fresh from the current workspace unless unsafe, unavailable, or blocked.
12. Do not silently replace a planned check with a different command.
13. If an equivalent repo-native check is substituted, record the substitution and rationale.
14. If no safe equivalent exists, mark the check as `blocked` or `skipped`.
15. Keep running independent checks after a failure when doing so is safe and useful.
16. Write only `verification.md`.

## Command Safety Gate

Run only local verification commands by default.
Block or skip commands that are destructive, mutate source files, install dependencies, deploy, touch production resources, use credentials, run migrations, delete files, or perform broad writes unless the human gives explicit human authorization.
Record blocked or skipped unsafe commands in `verification.md` with reason and residual risk.

## Result Labels

Per-check labels:

- `pass`
- `fail`
- `skipped`
- `blocked`

Overall verdicts:

- `pass`: all required checks passed and evidence matches expectations
- `fail`: one or more required checks ran and contradicted expectations
- `partial`: some evidence is valid, but required evidence is missing, skipped, blocked, or manual-only
- `blocked`: verification could not run enough required checks to support a completion claim

## Verification Authoring Rules

Write `verification.md` with these sections:

- Summary
- Planned Checks
- Results
- Manual Validation
- Skipped Checks
- Remaining Risk
- Review Handoff

For command-backed checks, record:

- check ID
- command
- working directory
- result label
- exit status when available
- concise evidence
- artifact paths when relevant

Avoid full raw terminal transcripts by default.
Use concise excerpts, counts, exit status, command names, and artifact paths.

For skipped or blocked checks, record:

- reason
- whether the check was required for pass
- residual risk
- owner or next step when knowable

For manual validation, record:

- scenario or method
- expected result
- observed result
- observer when known
- evidence

Treat missing or incomplete planned checks as planning or verification risk.
Do not invent a broad unrelated test suite by default.

## Boundaries

Write only `verification.md`.
Do not edit source code.
Do not edit tests.
Do not edit `spec.md`.
Do not edit `plan.md`.
Do not edit `review.md`.
Do not run implementation.
Do not approve waivers.
Do not accept risk on behalf of the human.
Do not declare review complete.
Do not create `tasks.md`.
Phase 1 does not require a script; verification is evidence judgment plus fresh command execution.

## Completion

Report the written `verification.md` path.
If checks failed or evidence is missing, recommend returning to implementation.
If evidence is legible enough for a fresh reviewer, recommend continuing to `wr-review`.
Do not claim review has happened.

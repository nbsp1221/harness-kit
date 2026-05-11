# Deep Research Contract

This contract governs the deep dossier pass for the six benchmark targets.

## Goal

Upgrade the current research archive from summary reports into source-grounded dossiers that remain useful months later even when the original exploration context is gone.

## Scope

Create deep dossiers for:

- `compound-engineering-plugin`
- `gstack`
- `superpowers`
- `oh-my-codex`
- `Archon`
- `OpenHarness`

The target outcome is not prose inflation. The target outcome is deeper source reconstruction:

- install and bootstrap trace
- artifact inventory
- architecture map
- workflow surface
- state and memory model
- verification and control model
- code hotspot map

## Owners

- Parent agent: all edits under `docs/research/dossiers/**`, synthesis, final judgment
- Subagents: read-only research only
- Review agents: read-only critique only

## Acceptance Criteria

- Each target has a deep dossier at `docs/research/dossiers/<target>.md`
- Each dossier is source-grounded and substantially deeper than the summary report
- Each dossier documents the install path, major owned artifacts, workflow surface, state model, and key code paths
- The evidence map uses repo-relative source paths plus the pinned `source_ref`

## Evidence Required

Every subagent return must include:

- concrete repo-relative file paths
- what the file proves
- why that proof matters for `harness-kit`
- unresolved gaps

Subagents should prefer:

- README and architecture docs
- install and setup scripts
- config loaders and generators
- state or memory modules
- hook, permission, workflow, or agent code
- tests that reveal contract boundaries

## Output Contract For Structure Pass

```text
Scope:
Owner:

Install / Bootstrap:
- Claim:
  Evidence:
  Why it matters:

Artifact Inventory:
- Artifact:
  Scope:
  Evidence:
  Why it matters:

Architecture Map:
- Area:
  Key paths:
  Why it matters:

Workflow Surface:
- Component:
  Evidence:
  Why it matters:

State / Memory:
- Component:
  Evidence:
  Why it matters:

Next-step note:
```

## Output Contract For Code Hotspot Pass

```text
Scope:
Owner:

Code Hotspots:
- File:
  Role:
  Why it matters:
  Evidence:

Verification / Control Paths:
- File:
  Mechanism:
  Why it matters:
  Evidence:

Open Questions:
- ...

Next-step note:
```

## Non-Negotiable Rules

- Subagents stay read-only.
- The parent stays the only writer.
- Evidence must use repo-relative paths, not `/tmp` links.
- Summary-only returns are not acceptable.

---
spec_id: 20260502-0026-npm-packaging-cli
title: npm packaging CLI setup
status: active
stage: spec
created_at: 2026-05-02 00:26
timezone: Asia/Seoul
---

# npm packaging CLI setup

## Problem

`harness-kit` currently has repository scripts under `scripts/harness-kit/` and a starter template under `template/`, but it is not yet shaped as an npm-installable CLI package.
Users cannot install it with a normal package manager, cannot inspect package metadata, cannot rely on semantic package versioning, and cannot run a stable global command without knowing this repository's internal script paths.

This blocks the next product step: making `harness-kit` easy to install and use as a personal, opinionated repo-local agent workflow starter.

The CLI implementation should also align with the chosen distribution channel.
Because the product target is npm, the package should not depend on a second Python runtime for its core install, bootstrap, adopt, or doctor behavior.
The existing Python scripts are small enough that this packaging step should complete the migration rather than preserve Python as a long-term reference implementation.

## Why Now

The Phase 1 lifecycle starter is mostly in place:

- `template/` contains the starter source of truth.
- `bootstrap`, `adopt`, and `doctor` already exist as runnable repository scripts.
- `hk-spec`, `hk-plan`, `hk-verify`, and `hk-review` are installed through the starter template.
- The project has enough contract tests to support packaging without changing core behavior.

Before publishing, the repository needs package metadata, command entrypoints, version scripts, and packaging checks so npm publication is possible later without doing release design under time pressure.

Name availability research also changed the naming decision.
The unscoped `harness-kit` package is currently unclaimed, but the `@harness-kit/cli` package already exists and exposes a `harness-kit` binary for a similar problem space.
Because this project is primarily `retn0`'s opinionated starter that others may use if they want, the package should use the scoped name `@retn0/harness-kit`.

## Requirements

- `R1`: The npm package name MUST be `@retn0/harness-kit`.
- `R2`: The package MUST be configured for public scoped npm publishing.
- `R3`: The package MUST expose a global `harness-kit` binary.
- `R4`: The package SHOULD expose a shorter fallback binary alias, `hks`, to avoid global command conflicts.
- `R5`: The CLI entrypoint MUST support the existing commands: `bootstrap`, `adopt`, and `doctor`.
- `R6`: The CLI entrypoint MUST preserve the current command behavior and JSON output shape for `bootstrap`, `adopt`, and `doctor`.
- `R7`: The npm package MUST include the files needed to run the CLI and install the starter template.
- `R8`: The npm package MUST NOT include generated test caches, git internals, local temporary files, or unrelated research clones.
- `R9`: The package metadata MUST include a clear description that this is `retn0`'s opinionated harness-kit starter for repo-local agent workflows.
- `R10`: The package metadata MUST include repository, license, bin, files, engines, and scripts fields appropriate for npm publication.
- `R11`: The implementation MUST add package scripts for testing the package setup locally.
- `R12`: The implementation MUST provide a way to inspect the exact npm tarball contents before publishing.
- `R13`: The packaging setup MUST NOT publish automatically as part of this work.
- `R14`: The packaging setup MUST implement the npm-facing CLI behavior natively in Node.js.
- `R15`: The npm-facing CLI MUST NOT delegate core `bootstrap`, `adopt`, or `doctor` behavior to Python.
- `R16`: The implementation MUST document the intended install and usage commands.
- `R17`: The implementation MUST make version ownership explicit in `package.json`.
- `R18`: The implementation MUST remove the existing Python CLI implementation once the Node implementation covers the same starter behavior.
- `R19`: Tests MUST verify that package metadata exists and exposes the expected package name and binaries.
- `R20`: Tests MUST verify that packaged file selection includes required starter files and excludes obvious non-package artifacts.
- `R21`: Tests MUST verify that the npm CLI can invoke at least `--help` or equivalent command discovery without publishing.
- `R22`: The work MUST leave actual npm login, npm publish, provenance setup, and release automation for a later release spec unless explicitly requested.

## Success Criteria

- `SC1`: A maintainer can run local package checks and see that `@retn0/harness-kit` would package the expected files.
- `SC2`: A maintainer can install or execute the local package entrypoint and run `harness-kit bootstrap`, `harness-kit adopt`, and `harness-kit doctor` behavior through the npm-facing command path.
- `SC3`: `package.json` clearly communicates the package name, command names, version, description, repository, license, supported runtime, files, and scripts.
- `SC4`: The package can be prepared for `npm publish --access public` later without renaming or reorganizing the project again.
- `SC5`: The repository no longer contains the existing Python CLI implementation under `scripts/harness-kit/`.
- `SC6`: No actual publish occurs during this spec item.
- `SC7`: The Node implementation passes behavior tests for `bootstrap`, `adopt`, and `doctor`, including JSON output and conflict handling.

## Scope

In scope:

- root `package.json`
- npm-facing CLI files
- package file inclusion/exclusion configuration
- packaging-related tests
- README or package usage documentation updates needed to explain npm installation
- verification commands for local packaging
- removing the replaced Python CLI implementation and updating tests accordingly

Out of scope:

- actual `npm publish`
- npm token/login setup
- GitHub Actions release workflow
- npm provenance/trusted publishing setup
- package signing
- changelog automation
- adding new lifecycle commands beyond `bootstrap`, `adopt`, and `doctor`
- changing the starter template contract except where required for packaging docs

## Constraints

- The package is scoped to `@retn0`, matching the owner's existing npm publishing pattern.
- The project should remain usable directly from the repository without global npm installation.
- The Node CLI should be dependency-light and should not introduce a large runtime dependency graph.
- Published package contents should be intentionally small and auditable.
- The work must account for possible global binary conflict with the existing `@harness-kit/cli` package's `harness-kit` binary.
- The package should be public even though it is opinionated for personal use.

## Assumptions

- `A1`: The npm account or organization has permission to publish `@retn0/harness-kit`.
- `A2`: `@retn0/harness-kit` is currently unclaimed on npm based on `npm view @retn0/harness-kit` returning 404 on 2026-05-02.
- `A3`: Users who install this package are expected to have Node available.
- `A4`: Users who install this package should not need Python for core `harness-kit` commands.
- `A5`: The existing Python implementation is small enough to migrate in this spec item without keeping it as a reference implementation.
- `A6`: The fallback `hks` binary is useful because another package already exposes a global `harness-kit` binary.

## Open Questions

### Resolve Before Planning

- None.

### Deferred to hk-plan

- Decide the exact Node implementation shape: dependency-free JavaScript or TypeScript with a build step.
- Decide whether package content should be controlled with `files` in `package.json`, `.npmignore`, or both.
- Decide the exact local package verification commands, including whether to use `npm pack --dry-run --json`.
- Decide whether README changes belong in root README, template README, or both.

## Planning Handoff

Status: Ready for hk-plan
Spec path: specs/20260502-0026-npm-packaging-cli/spec.md
Open questions: none blocking planning
Key assumptions: A1, A2, A3, A4, A5, A6
Requirement index: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22
Recommended next action: hk-plan

## Sources

- Local: `scripts/harness-kit/bootstrap`
- Local: `scripts/harness-kit/adopt`
- Local: `scripts/harness-kit/doctor`
- Local: `scripts/harness-kit/_lib/starter.py`
- Local: `template/`
- npm registry: `npm view @retn0/harness-kit` returned 404 on 2026-05-02
- npm registry: `npm view @harness-kit/cli` shows an existing package with `bin.harness-kit`
- npm registry: `npm view harnesskit` shows an existing similar unscoped package

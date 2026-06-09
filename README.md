# wayrail

`@retn0/wayrail` is retn0's opinionated starter for repo-local agent workflows.

It installs a small project contract: lifecycle specs, repo-local agent skills, starter docs, and health checks.

## Install

This package is prepared for npm publication, but this repository does not publish during the current setup work.

Future global install:

```sh
npm install -g @retn0/wayrail
```

Local development:

```sh
node bin/wayrail.js --help
node bin/wayrail.js bootstrap ./my-project
```

## Commands

```sh
wayrail bootstrap [--dry-run] [--json] [target]
wayrail adopt [--dry-run] [--json] [target]
wayrail doctor [--json] [target]
```

`wyr` is provided as a shorter alias for `wayrail`.

- `bootstrap` installs the starter into a new repository path.
- `adopt` adds missing starter files to an existing repository and preserves an existing `README.md`.
- `doctor` validates that a repository satisfies the starter contract.

## Package Checks

```sh
npm run test
npm run package:dry-run
npm run package:check
```

Release automation, npm login, trusted publishing, provenance, and actual `npm publish` are intentionally outside this pass.

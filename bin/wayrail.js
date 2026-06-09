#!/usr/bin/env node
import { constants as fsConstants } from "node:fs";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { TextDecoder } from "node:util";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const TEMPLATE_DIR = path.join(REPO_ROOT, "template");

const REQUIRED_TEMPLATE_FILES = [
  "README.md",
  "AGENTS.md",
  "wayrail.yaml",
  "docs/roadmap/README.md",
  "specs/.gitkeep",
  "specs/_templates/spec.md",
  "specs/_templates/plan.md",
  "specs/_templates/verification.md",
  "specs/_templates/review.md",
  ".agents/skills/wr-spec/SKILL.md",
  ".agents/skills/wr-spec/scripts/new-spec-item",
  ".agents/skills/wr-spec/agents/openai.yaml",
  ".agents/skills/wr-plan/SKILL.md",
  ".agents/skills/wr-plan/agents/openai.yaml",
  ".agents/skills/wr-verify/SKILL.md",
  ".agents/skills/wr-verify/agents/openai.yaml",
  ".agents/skills/wr-review/SKILL.md",
  ".agents/skills/wr-review/agents/openai.yaml",
  "memory/learnings.md",
];

const CONFIG_REQUIRED_SNIPPETS = [
  "schema_version: 1",
  "artifact_root: specs",
  "spec_id_format: YYYYMMDD-HHMM-short-slug",
  "learnings: memory/learnings.md",
];

const COMMANDS = new Set(["bootstrap", "adopt", "doctor"]);

function printTopHelp() {
  console.log(`usage: wayrail <command> [options] [target]

Commands:
  bootstrap    Install the wayrail starter into a new repository.
  adopt        Inspect and add missing wayrail starter files to an existing repository.
  doctor       Validate wayrail starter contract health.

Aliases:
  wyr          Short alias for wayrail.

Run "wayrail <command> --help" for command options.`);
}

function printCommandHelp(command) {
  const descriptions = {
    bootstrap: "Install the wayrail starter into a new repository.",
    adopt: "Inspect and add missing wayrail starter files to an existing repository.",
    doctor: "Validate wayrail starter contract health.",
  };
  const dryRun = command === "doctor" ? "" : "\n  --dry-run   Report actions without writing files";
  console.log(`usage: wayrail ${command} [--json]${command === "doctor" ? "" : " [--dry-run]"} [target]

${descriptions[command]}

Options:
  --json      Print machine-readable JSON${dryRun}
  --help      Show this help message`);
}

function parseCommandArgs(command, rawArgs) {
  const options = { json: false, dryRun: false, target: "." };
  const positionals = [];

  for (const arg of rawArgs) {
    if (arg === "--help" || arg === "-h") {
      printCommandHelp(command);
      process.exit(0);
    }
    if (arg === "--json") {
      options.json = true;
      continue;
    }
    if (arg === "--dry-run" && command !== "doctor") {
      options.dryRun = true;
      continue;
    }
    if (arg.startsWith("-")) {
      throw new Error(`unknown option for ${command}: ${arg}`);
    }
    positionals.push(arg);
  }

  if (positionals.length > 1) {
    throw new Error(`too many arguments for ${command}`);
  }
  if (positionals.length === 1) {
    options.target = positionals[0];
  }

  return options;
}

function expandHome(input) {
  if (input === "~") {
    return os.homedir();
  }
  if (input.startsWith(`~${path.sep}`)) {
    return path.join(os.homedir(), input.slice(2));
  }
  return input;
}

function targetPath(rawTarget) {
  return path.resolve(expandHome(rawTarget));
}

async function exists(filePath) {
  try {
    await fs.lstat(filePath);
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") {
      return false;
    }
    throw error;
  }
}

async function lstatOrNull(filePath) {
  try {
    return await fs.lstat(filePath);
  } catch (error) {
    if (error?.code === "ENOENT") {
      return null;
    }
    throw error;
  }
}

async function pathConflict(target, relativePath) {
  const targetStats = await lstatOrNull(target);
  if (targetStats && !targetStats.isDirectory()) {
    return "target path exists and is not a directory";
  }

  let current = target;
  const parentParts = relativePath.split("/").slice(0, -1);
  for (const part of parentParts) {
    current = path.join(current, part);
    const stats = await lstatOrNull(current);
    if (!stats) {
      continue;
    }
    if (stats.isSymbolicLink()) {
      return "parent path is a symlink";
    }
    if (!stats.isDirectory()) {
      return "parent path exists and is not a directory";
    }
  }

  const destination = path.join(target, relativePath);
  const destinationStats = await lstatOrNull(destination);
  if (destinationStats?.isSymbolicLink()) {
    return "path is a symlink";
  }

  return "";
}

async function filesEqual(left, right) {
  try {
    const [leftBuffer, rightBuffer] = await Promise.all([fs.readFile(left), fs.readFile(right)]);
    return Buffer.compare(leftBuffer, rightBuffer) === 0;
  } catch (error) {
    if (error?.code === "ENOENT" || error?.code === "EISDIR") {
      return false;
    }
    throw error;
  }
}

async function plannedActions(command, target) {
  const actions = [];
  for (const relativePath of REQUIRED_TEMPLATE_FILES) {
    const source = path.join(TEMPLATE_DIR, relativePath);
    const destination = path.join(target, relativePath);

    if (command === "adopt" && relativePath === "README.md" && await exists(destination)) {
      actions.push({ path: relativePath, action: "preserve", reason: "existing README.md preserved" });
      continue;
    }

    const conflict = await pathConflict(target, relativePath);
    if (conflict) {
      actions.push({ path: relativePath, action: "conflict", reason: conflict });
      continue;
    }

    const destinationStats = await lstatOrNull(destination);
    if (!destinationStats) {
      actions.push({ path: relativePath, action: "create" });
    } else if (destinationStats.isFile() && await filesEqual(source, destination)) {
      actions.push({ path: relativePath, action: "skip-identical" });
    } else {
      actions.push({ path: relativePath, action: "conflict", reason: "path exists and differs" });
    }
  }
  return actions;
}

function hasConflicts(actions) {
  return actions.some((action) => action.action === "conflict");
}

async function copyTemplateFile(relativePath, target) {
  const source = path.join(TEMPLATE_DIR, relativePath);
  const destination = path.join(target, relativePath);
  const sourceStats = await fs.stat(source);
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.copyFile(source, destination, fsConstants.COPYFILE_EXCL);
  await fs.chmod(destination, sourceStats.mode & 0o777);
}

async function applyActions(target, actions) {
  for (const action of actions) {
    if (action.action !== "create") {
      continue;
    }
    await copyTemplateFile(action.path, target);
  }
}

function printInstallResult(payload, jsonMode) {
  if (jsonMode) {
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  console.log(`${payload.command}: ${payload.target}`);
  console.log(`safe_to_apply: ${String(payload.safe_to_apply)}`);
  for (const action of payload.actions) {
    const suffix = action.reason ? ` (${action.reason})` : "";
    console.log(`- ${action.action}: ${action.path}${suffix}`);
  }
}

async function runInstall(command, options) {
  if (!await exists(TEMPLATE_DIR)) {
    console.error(`template directory not found: ${TEMPLATE_DIR}`);
    return 2;
  }

  const target = targetPath(options.target);
  const actions = await plannedActions(command, target);
  const payload = {
    command,
    target,
    dry_run: options.dryRun,
    safe_to_apply: !hasConflicts(actions),
    actions,
  };

  if (hasConflicts(actions)) {
    printInstallResult(payload, options.json);
    return 1;
  }

  if (!options.dryRun) {
    await applyActions(target, actions);
  }

  printInstallResult(payload, options.json);
  return 0;
}

async function readUtf8Text(filePath) {
  try {
    const buffer = await fs.readFile(filePath);
    return { text: new TextDecoder("utf-8", { fatal: true }).decode(buffer), error: null };
  } catch (error) {
    return { text: null, error: String(error.message || error) };
  }
}

function addCheck(checks, id, category, status, checkPath, message) {
  checks.push({ id, category, status, path: checkPath, message });
}

async function validateConfig(target, checks) {
  const configPath = path.join(target, "wayrail.yaml");
  if (!await exists(configPath)) {
    addCheck(checks, "config.exists", "config", "fail", "wayrail.yaml", "wayrail.yaml is missing");
    return;
  }

  const { text, error } = await readUtf8Text(configPath);
  if (text === null) {
    addCheck(
      checks,
      "config.readable",
      "config",
      "fail",
      "wayrail.yaml",
      `wayrail.yaml could not be read as text: ${error}`,
    );
    return;
  }

  const missing = CONFIG_REQUIRED_SNIPPETS.filter((snippet) => !text.includes(snippet));
  if (missing.length > 0) {
    addCheck(
      checks,
      "config.minimum_shape",
      "config",
      "fail",
      "wayrail.yaml",
      "wayrail.yaml is missing required Phase 1 keys",
    );
  } else {
    addCheck(
      checks,
      "config.minimum_shape",
      "config",
      "pass",
      "wayrail.yaml",
      "wayrail.yaml has the minimum Phase 1 shape",
    );
  }
}

async function doctorChecks(target) {
  const checks = [];
  const targetExists = await exists(target);
  addCheck(
    checks,
    "environment.repo_root",
    "environment",
    targetExists ? "pass" : "fail",
    ".",
    targetExists ? "target path exists" : "target path does not exist",
  );

  for (const relativePath of REQUIRED_TEMPLATE_FILES) {
    const artifactExists = await exists(path.join(target, relativePath));
    addCheck(
      checks,
      `artifact.${relativePath}`,
      "starter_integrity",
      artifactExists ? "pass" : "fail",
      relativePath,
      artifactExists ? "required starter artifact exists" : "required starter artifact is missing",
    );
  }

  await validateConfig(target, checks);

  for (const relativePath of [
    "specs/_templates/spec.md",
    "specs/_templates/plan.md",
    "specs/_templates/verification.md",
    "specs/_templates/review.md",
  ]) {
    const { text } = await readUtf8Text(path.join(target, relativePath));
    const status = text !== null && text.trim() ? "pass" : "fail";
    addCheck(
      checks,
      `artifact_shape.${relativePath}`,
      "artifact_shape",
      status,
      relativePath,
      status === "pass" ? "lifecycle template is recognizable" : "lifecycle template is missing or empty",
    );
  }

  return checks;
}

function statusFromChecks(checks) {
  if (checks.some((check) => check.status === "error")) return "error";
  if (checks.some((check) => check.status === "fail")) return "fail";
  if (checks.some((check) => check.status === "warn")) return "warn";
  return "pass";
}

function summaryFromChecks(checks) {
  const summary = { pass: 0, warn: 0, fail: 0, skip: 0, error: 0 };
  for (const check of checks) {
    summary[check.status] += 1;
  }
  return summary;
}

function printDoctorResult(payload, jsonMode) {
  if (jsonMode) {
    console.log(JSON.stringify(payload, null, 2));
    return;
  }

  console.log(`doctor: ${payload.repo_root}`);
  console.log(`status: ${payload.status}`);
  for (const check of payload.checks) {
    console.log(`- ${check.status}: ${check.id} (${check.path}) - ${check.message}`);
  }
}

async function runDoctor(options) {
  const target = targetPath(options.target);
  const checks = await doctorChecks(target);
  const payload = {
    schema_version: 1,
    status: statusFromChecks(checks),
    repo_root: target,
    generated_at: new Date().toISOString().slice(0, 19),
    checks,
    summary: summaryFromChecks(checks),
  };

  printDoctorResult(payload, options.json);
  return payload.status === "fail" || payload.status === "error" ? 1 : 0;
}

async function main() {
  const [command, ...commandArgs] = process.argv.slice(2);

  if (!command || command === "--help" || command === "-h") {
    printTopHelp();
    return 0;
  }
  if (!COMMANDS.has(command)) {
    console.error(`unknown command: ${command}`);
    printTopHelp();
    return 2;
  }

  const options = parseCommandArgs(command, commandArgs);
  if (command === "doctor") {
    return await runDoctor(options);
  }
  return await runInstall(command, options);
}

try {
  process.exitCode = await main();
} catch (error) {
  console.error(error?.message || String(error));
  process.exitCode = 2;
}

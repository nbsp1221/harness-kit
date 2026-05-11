import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = REPO_ROOT / "bin" / "harness-kit.js"
TEMPLATE_DIR = REPO_ROOT / "template"


REQUIRED_TEMPLATE_FILES = [
    "README.md",
    "AGENTS.md",
    "harness-kit.yaml",
    "docs/roadmap/README.md",
    "specs/.gitkeep",
    "specs/_templates/spec.md",
    "specs/_templates/plan.md",
    "specs/_templates/verification.md",
    "specs/_templates/review.md",
    ".agents/skills/hk-spec/SKILL.md",
    ".agents/skills/hk-spec/scripts/new-spec-item",
    ".agents/skills/hk-spec/agents/openai.yaml",
    ".agents/skills/hk-plan/SKILL.md",
    ".agents/skills/hk-plan/agents/openai.yaml",
    ".agents/skills/hk-verify/SKILL.md",
    ".agents/skills/hk-verify/agents/openai.yaml",
    ".agents/skills/hk-review/SKILL.md",
    ".agents/skills/hk-review/agents/openai.yaml",
    "memory/learnings.md",
]


class StarterTemplateTest(unittest.TestCase):
    def test_template_contains_required_starter_files(self):
        for relative_path in REQUIRED_TEMPLATE_FILES:
            path = TEMPLATE_DIR / relative_path
            self.assertTrue(path.exists(), f"missing template file: {relative_path}")

    def test_harness_config_is_minimal_phase_one_contract(self):
        config = (TEMPLATE_DIR / "harness-kit.yaml").read_text()

        self.assertIn("schema_version: 1", config)
        self.assertIn("artifact_root: specs", config)
        self.assertIn("spec_id_format: YYYYMMDD-HHMM-short-slug", config)
        self.assertIn("learnings: memory/learnings.md", config)
        self.assertNotIn("host", config.lower())
        self.assertNotIn("hook", config.lower())
        self.assertNotIn("runtime", config.lower())


class StarterScriptTest(unittest.TestCase):
    def run_cli(self, *args, cwd=None):
        command = ["node", str(CLI_PATH), *args]
        return subprocess.run(
            command,
            cwd=cwd or REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_scripts_expose_help(self):
        for name in ["bootstrap", "adopt", "doctor"]:
            with self.subTest(name=name):
                result = self.run_cli(name, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout)

    def test_bootstrap_dry_run_json_reports_creates_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "blank"
            target.mkdir()

            result = self.run_cli("bootstrap", "--dry-run", "--json", str(target))

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["safe_to_apply"])
            actions = {item["path"]: item["action"] for item in payload["actions"]}
            self.assertEqual(actions["AGENTS.md"], "create")
            self.assertEqual(actions["specs/_templates/spec.md"], "create")
            self.assertFalse((target / "AGENTS.md").exists())

    def test_bootstrap_creates_full_starter_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "blank"
            target.mkdir()

            result = self.run_cli("bootstrap", "--json", str(target))

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["safe_to_apply"])
            for relative_path in REQUIRED_TEMPLATE_FILES:
                self.assertTrue((target / relative_path).exists(), relative_path)
            self.assertTrue((target / ".agents/skills/hk-spec/scripts/new-spec-item").stat().st_mode & 0o111)

    def test_adopt_reports_conflict_without_partial_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing"
            target.mkdir()
            (target / "AGENTS.md").write_text("# Existing Agent Rules\n")

            result = self.run_cli("adopt", "--json", str(target))

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["safe_to_apply"])
            conflicts = [
                item for item in payload["actions"]
                if item["path"] == "AGENTS.md" and item["action"] == "conflict"
            ]
            self.assertEqual(len(conflicts), 1)
            self.assertEqual((target / "AGENTS.md").read_text(), "# Existing Agent Rules\n")
            self.assertFalse((target / "harness-kit.yaml").exists())

    def test_adopt_preserves_existing_readme_without_blocking_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing"
            target.mkdir()
            (target / "README.md").write_text("# Existing Project\n")

            result = self.run_cli("adopt", "--json", str(target))

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["safe_to_apply"])
            actions = {item["path"]: item["action"] for item in payload["actions"]}
            self.assertEqual(actions["README.md"], "preserve")
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "harness-kit.yaml").exists())
            self.assertEqual((target / "README.md").read_text(), "# Existing Project\n")

    def test_bootstrap_reports_ancestor_file_conflict_without_partial_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "blank"
            target.mkdir()
            (target / "docs").write_text("not a directory\n")

            result = self.run_cli("bootstrap", "--json", str(target))

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["safe_to_apply"])
            conflicts = [
                item for item in payload["actions"]
                if item["path"] == "docs/roadmap/README.md" and item["action"] == "conflict"
            ]
            self.assertEqual(len(conflicts), 1)
            self.assertFalse((target / "README.md").exists())
            self.assertEqual((target / "docs").read_text(), "not a directory\n")

    def test_bootstrap_reports_file_target_as_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "not-a-directory"
            target.write_text("existing file\n")

            result = self.run_cli("bootstrap", "--json", str(target))

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["safe_to_apply"])
            self.assertTrue(
                any(item["action"] == "conflict" and "target path" in item["reason"] for item in payload["actions"])
            )
            self.assertEqual(target.read_text(), "existing file\n")

    def test_bootstrap_reports_symlink_parent_conflict_without_external_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "blank"
            target.mkdir()
            outside = Path(tmp) / "outside"
            outside.mkdir()
            docs = target / "docs"
            docs.mkdir()
            (docs / "roadmap").symlink_to(outside, target_is_directory=True)

            result = self.run_cli("bootstrap", "--json", str(target))

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["safe_to_apply"])
            conflicts = [
                item for item in payload["actions"]
                if item["path"] == "docs/roadmap/README.md" and item["action"] == "conflict"
            ]
            self.assertEqual(len(conflicts), 1)
            self.assertFalse((outside / "README.md").exists())
            self.assertFalse((target / "README.md").exists())

    def test_adopt_treats_identical_files_as_satisfied(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing"
            shutil.copytree(TEMPLATE_DIR, target)

            result = self.run_cli("adopt", "--dry-run", "--json", str(target))

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            actions = {item["path"]: item["action"] for item in payload["actions"]}
            self.assertEqual(actions["AGENTS.md"], "skip-identical")
            self.assertEqual(actions["harness-kit.yaml"], "skip-identical")

    def test_doctor_reports_valid_bootstrapped_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "blank"
            target.mkdir()
            bootstrap = self.run_cli("bootstrap", "--json", str(target))
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)

            result = self.run_cli("doctor", "--json", str(target))

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["summary"]["fail"], 0)
            self.assertGreater(payload["summary"]["pass"], 0)

    def test_doctor_fails_when_required_starter_file_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "blank"
            target.mkdir()
            bootstrap = self.run_cli("bootstrap", "--json", str(target))
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)
            (target / "harness-kit.yaml").unlink()

            result = self.run_cli("doctor", "--json", str(target))

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "fail")
            failed = [check for check in payload["checks"] if check["status"] == "fail"]
            self.assertTrue(any(check["path"] == "harness-kit.yaml" for check in failed))

    def test_doctor_reports_invalid_utf8_config_as_json_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "blank"
            target.mkdir()
            bootstrap = self.run_cli("bootstrap", "--json", str(target))
            self.assertEqual(bootstrap.returncode, 0, bootstrap.stderr)
            (target / "harness-kit.yaml").write_bytes(b"\xff\xfe\x00")

            result = self.run_cli("doctor", "--json", str(target))

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "fail")
            failed = [check for check in payload["checks"] if check["status"] == "fail"]
            self.assertTrue(any(check["id"] == "config.readable" for check in failed))


if __name__ == "__main__":
    unittest.main()

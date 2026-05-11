import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO_ROOT / "template"
SKILL_DIR = TEMPLATE_DIR / ".agents" / "skills" / "hk-spec"
SCRIPT = SKILL_DIR / "scripts" / "new-spec-item"


class HkSpecSkillTest(unittest.TestCase):
    def run_new_spec_item(self, *args, cwd=None):
        command = [str(SCRIPT), *args]
        return subprocess.run(
            command,
            cwd=cwd or REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def copy_template(self, target: Path) -> None:
        shutil.copytree(TEMPLATE_DIR, target)

    def assert_json_envelope(self, payload):
        self.assertEqual(
            set(payload),
            {
                "schema_version",
                "command",
                "status",
                "dry_run",
                "safe_to_apply",
                "repo_root",
                "spec",
                "created_paths",
                "planned_paths",
                "actions",
                "conflicts",
                "error",
                "next_action",
            },
        )

    def test_hk_spec_template_files_exist(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue(SCRIPT.exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertTrue(SCRIPT.stat().st_mode & 0o111)

    def test_hk_spec_frontmatter_matches_skill_contract(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: hk-spec", frontmatter)
        self.assertIn("starting or creating a new harness-kit spec item", frontmatter)
        self.assertIn("Do not use for implementation planning", frontmatter)

    def test_hk_spec_instructions_reference_script_and_templates(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("scripts/new-spec-item", text)
        self.assertIn("before writing prose", text)
        self.assertIn("specs/_templates/", text)
        self.assertIn("Fill only `spec.md`", text)

    def test_new_spec_item_exposes_help(self):
        result = self.run_new_spec_item("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage:", result.stdout)

    def test_new_spec_item_dry_run_json_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            self.copy_template(target)

            result = self.run_new_spec_item(
                "--root",
                str(target),
                "--slug",
                "sample-feature",
                "--timezone",
                "Asia/Seoul",
                "--dry-run",
                "--json",
                "--",
                "Sample Feature",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assert_json_envelope(payload)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["command"], "new-spec-item")
            self.assertEqual(payload["status"], "planned")
            self.assertTrue(payload["dry_run"])
            self.assertTrue(payload["safe_to_apply"])
            self.assertEqual(payload["repo_root"], str(target))
            self.assertEqual(payload["conflicts"], [])
            self.assertIsNone(payload["error"])
            self.assertEqual(payload["next_action"], "write_spec")
            self.assertEqual(len(payload["actions"]), 4)
            self.assertEqual(payload["created_paths"], [])
            self.assertEqual(len(payload["planned_paths"]), 4)
            self.assertFalse(Path(payload["spec"]["spec_dir"]).exists())

    def test_new_spec_item_creates_full_lifecycle_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            self.copy_template(target)

            result = self.run_new_spec_item(
                "--root",
                str(target),
                "--slug",
                "sample-feature",
                "--timezone",
                "Asia/Seoul",
                "--json",
                "--",
                "Sample Feature",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assert_json_envelope(payload)
            self.assertEqual(payload["status"], "created")
            self.assertTrue(payload["safe_to_apply"])
            self.assertEqual(payload["planned_paths"], [])
            self.assertEqual(len(payload["created_paths"]), 4)
            self.assertEqual(len(payload["actions"]), 4)
            self.assertTrue(all(action["applied"] for action in payload["actions"]))
            spec_dir = Path(payload["spec"]["spec_dir"])
            self.assertTrue(spec_dir.exists())
            for filename in ["spec.md", "plan.md", "verification.md", "review.md"]:
                self.assertTrue((spec_dir / filename).exists(), filename)

            spec_text = (spec_dir / "spec.md").read_text()
            self.assertIn(f"spec_id: {payload['spec']['spec_id']}", spec_text)
            self.assertIn("title: Sample Feature", spec_text)
            self.assertIn("status: active", spec_text)
            self.assertIn("stage: spec", spec_text)
            self.assertIn("created_at:", spec_text)
            self.assertIn("timezone: Asia/Seoul", spec_text)

    def test_new_spec_item_uses_repo_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            self.copy_template(target)
            sentinel = "PLAN TEMPLATE SENTINEL\n"
            (target / "specs" / "_templates" / "plan.md").write_text(sentinel)

            result = self.run_new_spec_item(
                "--root",
                str(target),
                "--slug",
                "repo-template",
                "--timezone",
                "Asia/Seoul",
                "--json",
                "--",
                "Repo Template",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            plan_path = Path(payload["spec"]["files"]["plan"])
            self.assertEqual(plan_path.read_text(), sentinel)

    def test_new_spec_item_conflict_is_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            self.copy_template(target)

            first = self.run_new_spec_item(
                "--root",
                str(target),
                "--slug",
                "same-slug",
                "--timezone",
                "Asia/Seoul",
                "--json",
                "--",
                "Same Slug",
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            first_payload = json.loads(first.stdout)
            spec_path = Path(first_payload["spec"]["files"]["spec"])
            spec_path.write_text("do not overwrite\n")

            second = self.run_new_spec_item(
                "--root",
                str(target),
                "--slug",
                "same-slug",
                "--timezone",
                "Asia/Seoul",
                "--json",
                "--",
                "Same Slug",
            )

            self.assertEqual(second.returncode, 1)
            payload = json.loads(second.stdout)
            self.assert_json_envelope(payload)
            self.assertEqual(payload["status"], "conflict")
            self.assertFalse(payload["safe_to_apply"])
            self.assertIsNotNone(payload["error"])
            self.assertTrue(payload["conflicts"])
            self.assertEqual(spec_path.read_text(), "do not overwrite\n")

    def test_new_spec_item_missing_templates_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            self.copy_template(target)
            shutil.rmtree(target / "specs" / "_templates")

            result = self.run_new_spec_item(
                "--root",
                str(target),
                "--slug",
                "missing-templates",
                "--timezone",
                "Asia/Seoul",
                "--json",
                "--",
                "Missing Templates",
            )

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assert_json_envelope(payload)
            self.assertEqual(payload["status"], "conflict")
            self.assertFalse(payload["safe_to_apply"])
            self.assertTrue(
                any("required template is missing" == conflict["reason"] for conflict in payload["conflicts"])
            )

    def test_new_spec_item_invalid_invocation_json_uses_error_envelope(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            self.copy_template(target)

            result = self.run_new_spec_item(
                "--root",
                str(target),
                "--json",
            )

            self.assertEqual(result.returncode, 2)
            payload = json.loads(result.stdout)
            self.assert_json_envelope(payload)
            self.assertEqual(payload["status"], "error")
            self.assertFalse(payload["safe_to_apply"])
            self.assertEqual(payload["error"]["code"], "invalid_invocation")

    def test_new_spec_item_invalid_timezone_json_uses_error_envelope(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            self.copy_template(target)

            result = self.run_new_spec_item(
                "--root",
                str(target),
                "--slug",
                "bad-timezone",
                "--timezone",
                "Not/AZone",
                "--json",
                "--",
                "Bad Timezone",
            )

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assert_json_envelope(payload)
            self.assertEqual(payload["status"], "conflict")
            self.assertFalse(payload["safe_to_apply"])
            self.assertEqual(payload["error"]["code"], "invalid_timezone")

    def test_new_spec_item_dry_run_validates_rendered_spec_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "repo"
            self.copy_template(target)
            spec_template = target / "specs" / "_templates" / "spec.md"
            spec_template.write_text(spec_template.read_text().replace("timezone: <Timezone>\n", ""))

            result = self.run_new_spec_item(
                "--root",
                str(target),
                "--slug",
                "bad-template",
                "--timezone",
                "Asia/Seoul",
                "--dry-run",
                "--json",
                "--",
                "Bad Template",
            )

            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assert_json_envelope(payload)
            self.assertFalse(payload["safe_to_apply"])
            self.assertEqual(payload["error"]["code"], "generated_spec_invalid")
            self.assertFalse(Path(payload["spec"]["spec_dir"]).exists())

    def test_new_spec_item_allows_minimal_repo_with_only_templates(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "minimal"
            templates = target / "specs" / "_templates"
            templates.mkdir(parents=True)
            for name in ["spec.md", "plan.md", "verification.md", "review.md"]:
                shutil.copyfile(TEMPLATE_DIR / "specs" / "_templates" / name, templates / name)

            result = self.run_new_spec_item(
                "--root",
                str(target),
                "--slug",
                "minimal-repo",
                "--timezone",
                "Asia/Seoul",
                "--json",
                "--",
                "Minimal Repo",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assert_json_envelope(payload)
            self.assertEqual(payload["status"], "created")
            self.assertTrue(Path(payload["spec"]["files"]["spec"]).exists())


if __name__ == "__main__":
    unittest.main()

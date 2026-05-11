import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_JSON = REPO_ROOT / "package.json"
CLI_PATH = REPO_ROOT / "bin" / "harness-kit.js"


class NpmPackageTest(unittest.TestCase):
    def run_command(self, *args):
        return subprocess.run(
            args,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def package_json(self):
        return json.loads(PACKAGE_JSON.read_text())

    def test_package_metadata_defines_public_scoped_cli(self):
        package = self.package_json()

        self.assertEqual(package["name"], "@retn0/harness-kit")
        self.assertEqual(package["version"], "0.1.0")
        self.assertEqual(package["type"], "module")
        self.assertEqual(package["license"], "MIT")
        self.assertEqual(package["publishConfig"]["access"], "public")
        self.assertEqual(package["bin"]["harness-kit"], "./bin/harness-kit.js")
        self.assertEqual(package["bin"]["hks"], "./bin/harness-kit.js")
        self.assertIn("bin/", package["files"])
        self.assertIn("template/", package["files"])
        self.assertIn("README.md", package["files"])
        self.assertNotIn("scripts/harness-kit/", package["files"])
        self.assertIn("package:dry-run", package["scripts"])
        self.assertIn("package:check", package["scripts"])
        self.assertNotIn("publish", package["scripts"])
        self.assertNotIn("release", package["scripts"])

    def test_cli_help_and_unknown_command(self):
        help_result = self.run_command("node", str(CLI_PATH), "--help")
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("usage:", help_result.stdout)
        self.assertIn("bootstrap", help_result.stdout)
        self.assertIn("adopt", help_result.stdout)
        self.assertIn("doctor", help_result.stdout)

        unknown_result = self.run_command("node", str(CLI_PATH), "unknown")
        self.assertNotEqual(unknown_result.returncode, 0)
        self.assertIn("unknown command", unknown_result.stderr.lower())

    def test_replaced_python_cli_implementation_is_absent(self):
        removed_paths = [
            REPO_ROOT / "scripts" / "harness-kit" / "bootstrap",
            REPO_ROOT / "scripts" / "harness-kit" / "adopt",
            REPO_ROOT / "scripts" / "harness-kit" / "doctor",
            REPO_ROOT / "scripts" / "harness-kit" / "_lib" / "starter.py",
        ]

        for path in removed_paths:
            self.assertFalse(path.exists(), f"removed Python CLI path still exists: {path}")

    def test_npm_pack_contains_only_package_runtime_files(self):
        result = self.run_command("npm", "pack", "--dry-run", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        pack = json.loads(result.stdout)[0]
        paths = {entry["path"] for entry in pack["files"]}

        expected = {
            "package.json",
            "README.md",
            "bin/harness-kit.js",
            "template/README.md",
            "template/AGENTS.md",
            "template/harness-kit.yaml",
            "template/specs/_templates/spec.md",
            "template/specs/_templates/plan.md",
            "template/specs/_templates/verification.md",
            "template/specs/_templates/review.md",
            "template/.agents/skills/hk-spec/SKILL.md",
            "template/.agents/skills/hk-spec/scripts/new-spec-item",
            "template/.agents/skills/hk-plan/SKILL.md",
            "template/.agents/skills/hk-verify/SKILL.md",
            "template/.agents/skills/hk-review/SKILL.md",
        }
        for path in expected:
            self.assertIn(path, paths)

        excluded_prefixes = (
            ".git/",
            ".pytest_cache/",
            "docs/research/",
            "scripts/harness-kit/",
            "specs/",
            "tests/",
        )
        for path in paths:
            self.assertNotIn("__pycache__/", path)
            self.assertFalse(
                path.startswith(excluded_prefixes),
                f"unexpected non-package artifact in tarball: {path}",
            )


if __name__ == "__main__":
    unittest.main()

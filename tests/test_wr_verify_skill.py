import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO_ROOT / "template"
SKILL_DIR = TEMPLATE_DIR / ".agents" / "skills" / "wr-verify"


class WrVerifySkillTest(unittest.TestCase):
    def test_wr_verify_template_files_exist(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertFalse((SKILL_DIR / "scripts").exists())

    def test_wr_verify_frontmatter_matches_skill_contract(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: wr-verify", frontmatter)
        self.assertIn("implemented wayrail spec item", frontmatter)
        self.assertIn("verification.md evidence", frontmatter)
        self.assertIn("Do not use for code implementation", frontmatter)

    def test_wr_verify_requires_explicit_or_unambiguous_spec_item(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("explicit spec item path", text)
        self.assertIn("unambiguous current spec item", text)

    def test_wr_verify_reads_spec_and_plan_before_writing(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Read `spec.md`", text)
        self.assertIn("Read `plan.md`", text)
        self.assertIn("before writing", text)

    def test_wr_verify_enforces_implementation_handoff(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Implementation Handoff", text)
        self.assertIn("Ready for implementation", text)
        self.assertIn("Stop without writing successful verification", text)

    def test_wr_verify_requires_fresh_planned_check_evidence(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("planned verification checks", text)
        self.assertIn("fresh", text)
        self.assertIn("command", text)
        self.assertIn("working directory", text)
        self.assertIn("exit status", text)
        self.assertIn("concise evidence", text)
        self.assertIn("artifact paths", text)

    def test_wr_verify_defines_command_derivation_and_substitution_rules(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Derive commands in this order", text)
        self.assertIn("planned verification checks from `plan.md`", text)
        self.assertIn("repository guidance such as `AGENTS.md`", text)
        self.assertIn("standard project scripts only when they verify the same claim", text)
        self.assertIn("Do not silently replace a planned check", text)
        self.assertIn("record the substitution and rationale", text)
        self.assertIn("mark the check as `blocked` or `skipped`", text)

    def test_wr_verify_defines_command_safety_gate(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Run only local verification commands by default", text)
        self.assertIn("destructive", text)
        self.assertIn("production", text)
        self.assertIn("credentials", text)
        self.assertIn("install dependencies", text)
        self.assertIn("deploy", text)
        self.assertIn("explicit human authorization", text)

    def test_wr_verify_defines_result_labels(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        for label in ["pass", "fail", "skipped", "blocked", "partial"]:
            self.assertIn(label, text)
        self.assertIn("Per-check labels", text)
        self.assertIn("Overall verdicts", text)

    def test_wr_verify_defines_verification_md_sections(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        for section in [
            "Summary",
            "Planned Checks",
            "Results",
            "Manual Validation",
            "Skipped Checks",
            "Remaining Risk",
            "Review Handoff",
        ]:
            self.assertIn(section, text)

    def test_wr_verify_records_skipped_blocked_and_manual_validation_details(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("reason", text)
        self.assertIn("required for pass", text)
        self.assertIn("residual risk", text)
        self.assertIn("owner or next step", text)
        self.assertIn("expected result", text)
        self.assertIn("observed result", text)
        self.assertIn("observer", text)

    def test_wr_verify_preserves_existing_verification_evidence(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Read existing `verification.md`", text)
        self.assertIn("non-stub content", text)
        self.assertIn("do not overwrite", text)
        self.assertIn("explicitly asks to replace or revise", text)

    def test_wr_verify_limits_write_scope_and_lifecycle_boundary(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Write only `verification.md`", text)
        self.assertIn("Do not edit source code", text)
        self.assertIn("Do not edit tests", text)
        self.assertIn("Do not edit `spec.md`", text)
        self.assertIn("Do not edit `plan.md`", text)
        self.assertIn("Do not edit `review.md`", text)
        self.assertIn("Do not approve waivers", text)
        self.assertIn("Do not declare review complete", text)
        self.assertIn("Do not create `tasks.md`", text)

    def test_wr_verify_does_not_require_phase_one_script(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Phase 1 does not require a script", text)
        self.assertIn("verification is evidence judgment", text)
        self.assertIn("missing or incomplete planned checks", text)


if __name__ == "__main__":
    unittest.main()

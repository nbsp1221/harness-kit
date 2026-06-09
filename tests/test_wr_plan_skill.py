import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO_ROOT / "template"
SKILL_DIR = TEMPLATE_DIR / ".agents" / "skills" / "wr-plan"


class WrPlanSkillTest(unittest.TestCase):
    def test_wr_plan_template_files_exist(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertFalse((SKILL_DIR / "scripts").exists())

    def test_wr_plan_frontmatter_matches_skill_contract(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: wr-plan", frontmatter)
        self.assertIn("ready wayrail spec.md", frontmatter)
        self.assertIn("writes only plan.md", frontmatter)
        self.assertIn("Do not use for code implementation", frontmatter)

    def test_wr_plan_requires_explicit_or_unambiguous_spec_item(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("explicit spec item path", text)
        self.assertIn("unambiguous current spec item", text)

    def test_wr_plan_enforces_readiness_gate(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Planning Handoff", text)
        self.assertIn("Blocked before wr-plan", text)
        self.assertIn("Resolve Before Planning", text)
        self.assertIn("Stop without writing", text)

    def test_wr_plan_requires_bounded_repository_research(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("bounded repository research", text)
        self.assertIn("relevant docs", text)
        self.assertIn("likely target files", text)
        self.assertIn("test conventions", text)
        self.assertIn("verification commands", text)

    def test_wr_plan_limits_write_scope_and_lifecycle_boundary(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Write only `plan.md`", text)
        self.assertIn("Do not edit source code", text)
        self.assertIn("Do not run implementation", text)
        self.assertIn("Do not collect verification evidence", text)
        self.assertIn("Do not write review conclusions", text)
        self.assertIn("Do not create `tasks.md`", text)

    def test_wr_plan_defines_plan_authoring_rules(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        for section in [
            "Overview",
            "Requirements Trace",
            "Scope",
            "Context",
            "Decisions",
            "Implementation Units",
            "Verification",
            "Risks",
            "Implementation Handoff",
        ]:
            self.assertIn(section, text)
        self.assertIn("coarse implementation units", text)
        self.assertIn("Requirements:", text)
        self.assertIn("Files:", text)
        self.assertIn("Depends on:", text)
        self.assertIn("Approach:", text)
        self.assertIn("Verification:", text)

    def test_wr_plan_classifies_unknowns_before_asking_human(self):
        text = (SKILL_DIR / "SKILL.md").read_text()

        self.assertIn("Classify unknowns", text)
        self.assertIn("Human judgment", text)
        self.assertIn("Technical convention", text)
        self.assertIn("Risks", text)


if __name__ == "__main__":
    unittest.main()

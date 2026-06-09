import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO_ROOT / "template"
SKILL_DIR = TEMPLATE_DIR / ".agents" / "skills" / "wr-review"


class WrReviewSkillTest(unittest.TestCase):
    def skill_text(self):
        return (SKILL_DIR / "SKILL.md").read_text()

    def test_wr_review_template_files_exist(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").exists())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertFalse((SKILL_DIR / "scripts").exists())

    def test_wr_review_frontmatter_matches_skill_contract(self):
        text = self.skill_text()

        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: wr-review", frontmatter)
        self.assertIn("implemented and verified wayrail spec item", frontmatter)
        self.assertIn("review.md", frontmatter)
        self.assertIn("Do not use for implementation", frontmatter)

    def test_wr_review_requires_explicit_or_unambiguous_spec_item(self):
        text = self.skill_text()

        self.assertIn("explicit spec item path", text)
        self.assertIn("unambiguous current spec item", text)

    def test_wr_review_reads_required_artifacts_before_writing(self):
        text = self.skill_text()

        self.assertIn("Read `spec.md`", text)
        self.assertIn("Read `plan.md`", text)
        self.assertIn("Read `verification.md`", text)
        self.assertIn("Read existing `review.md` when present", text)
        self.assertIn("missing `review.md` is allowed", text)
        self.assertIn("before writing", text)

    def test_wr_review_enforces_review_handoff_completeness(self):
        text = self.skill_text()

        self.assertIn("Review Handoff", text)
        for field in [
            "verification status",
            "commands or checks run",
            "pass/fail/blocked/skipped results",
            "manual evidence",
            "known gaps",
            "residual risks",
            "recommended next action",
        ]:
            self.assertIn(field, text)
        self.assertIn("blocks a `ready` verdict", text)
        self.assertIn("record a finding", text)

    def test_wr_review_requires_fresh_artifact_context(self):
        text = self.skill_text()

        self.assertIn("fresh-context", text)
        self.assertIn("lifecycle artifacts", text)
        self.assertIn("not hidden implementation-session memory", text)

    def test_wr_review_defines_safe_read_only_diff_inspection(self):
        text = self.skill_text()

        self.assertIn("git status --short", text)
        self.assertIn("git diff --no-ext-diff --no-textconv", text)
        self.assertIn("git diff --cached --no-ext-diff --no-textconv", text)
        for forbidden in [
            "git add",
            "git stash",
            "git checkout",
            "git clean",
            "git reset",
            "commit",
            "merge",
            "push",
        ]:
            self.assertIn(forbidden, text)
        self.assertIn("list untracked files first", text)
        self.assertIn("read only relevant untracked files", text)

    def test_wr_review_compares_against_artifacts_and_evidence(self):
        text = self.skill_text()

        self.assertIn("requirements", text)
        self.assertIn("success criteria", text)
        self.assertIn("implementation units", text)
        self.assertIn("planned verification", text)
        self.assertIn("treat `verification.md` as evidence, not truth", text)
        self.assertIn("failed, skipped, blocked, missing, weak, or manual-only", text)

    def test_wr_review_defines_delegated_reviewer_boundaries(self):
        text = self.skill_text()

        for role in ["correctness", "testing/evidence", "maintainability/scope", "security"]:
            self.assertIn(role, text)
        self.assertIn("large", text)
        self.assertIn("shared lifecycle behavior", text)
        self.assertIn("findings only", text)
        self.assertIn("same read-only/no-fix/no-approval boundaries", text)
        self.assertIn("MUST NOT edit files", text)
        self.assertIn("MUST NOT run mutating commands", text)
        self.assertIn("MUST NOT grant waivers", text)
        self.assertIn("parent `wr-review`", text)
        self.assertIn("final verdict", text)

    def test_wr_review_defines_finding_schema(self):
        text = self.skill_text()

        for field in [
            "stable ID",
            "severity",
            "resolution state",
            "reviewer/source",
            "location",
            "artifact reference",
            "evidence",
            "behavioral risk",
            "recommendation",
            "decision authority",
            "human-required",
            "parent-decidable",
        ]:
            self.assertIn(field, text)

    def test_wr_review_defines_severity_resolution_and_verdict_labels(self):
        text = self.skill_text()

        for label in ["P0", "P1", "P2", "P3"]:
            self.assertIn(label, text)
        for label in ["fixed", "human-accepted-risk", "deferred", "rejected", "open"]:
            self.assertIn(label, text)
        for verdict in ["ready", "ready-with-residual-risk", "not-ready"]:
            self.assertIn(verdict, text)
        self.assertIn("New findings default to `open`", text)
        self.assertIn("explicit human decision", text)
        self.assertIn("MUST NOT invent acceptance", text)
        self.assertIn("open `P0` or `P1`", text)
        self.assertIn("no blocking findings", text)
        self.assertIn("human-accepted-risk", text)
        self.assertIn("deferred", text)
        self.assertIn("skipped, blocked, weak, manual-only", text)
        self.assertIn("`P2` residual risk", text)

    def test_wr_review_defines_review_md_sections_and_no_findings_rule(self):
        text = self.skill_text()

        for section in [
            "Summary",
            "Scope",
            "Reviewers",
            "Findings",
            "Resolutions",
            "Residual Risk",
            "Verdict",
        ]:
            self.assertIn(section, text)
        self.assertIn("If there are no findings", text)
        self.assertIn("still record scope, reviewers, residual risk, and verdict", text)

    def test_wr_review_preserves_existing_review_content(self):
        text = self.skill_text()

        self.assertIn("non-stub content", text)
        self.assertIn("preserve it", text)
        self.assertIn("append a new dated review section", text)
        self.assertIn("explicit user instruction to replace or revise", text)
        self.assertIn("MUST NOT silently overwrite", text)

    def test_wr_review_limits_write_scope_and_lifecycle_boundary(self):
        text = self.skill_text()

        self.assertIn("Write only `review.md`", text)
        self.assertIn("Do not edit source code", text)
        self.assertIn("Do not edit tests", text)
        self.assertIn("Do not edit `spec.md`", text)
        self.assertIn("Do not edit `plan.md`", text)
        self.assertIn("Do not edit `verification.md`", text)
        self.assertIn("Do not fix findings", text)
        self.assertIn("Do not approve waivers", text)
        self.assertIn("Do not claim human approval", text)
        self.assertIn("Do not merge", text)
        self.assertIn("Do not commit", text)
        self.assertIn("Do not approve release", text)
        self.assertIn("Do not change scope", text)

    def test_wr_review_does_not_require_phase_one_script(self):
        text = self.skill_text()

        self.assertIn("Phase 1 does not require a script", text)
        self.assertIn("review requires judgment and synthesis", text)
        self.assertIn("future helper script", text)
        self.assertIn("must not replace review judgment", text)


if __name__ == "__main__":
    unittest.main()

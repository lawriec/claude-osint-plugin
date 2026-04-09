# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8.0"]
# ///
"""Challenge validation tests — verify challenge files are well-formed."""

import re
from pathlib import Path

import pytest

CHALLENGES_DIR = Path(__file__).parent.parent / "challenges"


def get_challenge_files() -> list[Path]:
    """Get all challenge markdown files (excluding README)."""
    return sorted(f for f in CHALLENGES_DIR.glob("**/*.md") if f.name != "README.md")


class TestChallengeFormat:
    @pytest.fixture(params=get_challenge_files(), ids=lambda p: str(p.relative_to(CHALLENGES_DIR)))
    def challenge(self, request):
        return request.param

    def test_has_title(self, challenge):
        text = challenge.read_text(encoding="utf-8")
        assert text.startswith("# "), "Challenge should start with '# Title'"

    def test_has_domain_section(self, challenge):
        text = challenge.read_text(encoding="utf-8")
        assert "## Domain" in text

    def test_has_difficulty_with_valid_level(self, challenge):
        text = challenge.read_text(encoding="utf-8")
        assert "## Difficulty" in text
        difficulty_match = re.search(r"## Difficulty\s*\n\s*(\w+)", text)
        assert difficulty_match, "No difficulty level found"
        level = difficulty_match.group(1)
        assert level in ("Easy", "Medium", "Hard"), f"Invalid difficulty: {level}"

    def test_has_scenario(self, challenge):
        text = challenge.read_text(encoding="utf-8")
        assert "## Scenario" in text
        # Scenario should have substantive content
        scenario_match = re.search(r"## Scenario\s*\n(.*?)(?=\n## )", text, re.DOTALL)
        assert scenario_match, "Scenario section empty"
        assert len(scenario_match.group(1).strip()) > 50, "Scenario too short"

    def test_has_expected_approach(self, challenge):
        text = challenge.read_text(encoding="utf-8")
        assert "## Expected Approach" in text

    def test_has_verification(self, challenge):
        text = challenge.read_text(encoding="utf-8")
        assert "## Verification" in text

    def test_has_ground_truth_with_content(self, challenge):
        text = challenge.read_text(encoding="utf-8")
        assert "## Ground Truth" in text
        # Should have actual content (not just the header)
        gt_match = re.search(r"## Ground Truth\s*\n(.*)", text, re.DOTALL)
        assert gt_match and len(gt_match.group(1).strip()) > 50


class TestChallengeCategories:
    def test_has_readme(self):
        assert (CHALLENGES_DIR / "README.md").exists()

    def test_each_category_has_challenges(self):
        categories = [
            "geolocation", "people", "infrastructure", "image-forensics",
            "multi-domain", "transportation", "crypto", "verification",
        ]
        for cat in categories:
            cat_dir = CHALLENGES_DIR / cat
            challenges = list(cat_dir.glob("*.md"))
            assert len(challenges) >= 1, f"Category '{cat}' has no challenges"

    def test_minimum_challenge_count(self):
        all_challenges = get_challenge_files()
        assert len(all_challenges) >= 20, f"Expected 20+ challenges, found {len(all_challenges)}"

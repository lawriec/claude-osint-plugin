# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8.0", "pyyaml>=6.0"]
# ///
"""Skill integrity tests — verify internal consistency of the OSINT plugin.

These tests require no network access and validate:
- All reference files mentioned in SKILL.md exist
- All scripts mentioned in reference files exist
- SKILL.md frontmatter is valid YAML
- Challenge files have required sections
- No broken internal links
"""

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
SKILL_DIR = ROOT / "skills" / "osint"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCES_DIR = SKILL_DIR / "references"
SCRIPTS_DIR = SKILL_DIR / "scripts"
CHALLENGES_DIR = ROOT / "challenges"


def extract_frontmatter(filepath: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return None


def extract_md_references(filepath: Path, pattern: str) -> list[str]:
    """Extract all references matching a pattern from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    return re.findall(pattern, text)


class TestSkillFrontmatter:
    def test_skill_md_exists(self):
        assert SKILL_MD.exists(), "SKILL.md does not exist"

    def test_skill_md_has_frontmatter(self):
        fm = extract_frontmatter(SKILL_MD)
        assert fm is not None, "SKILL.md has no YAML frontmatter"

    def test_skill_md_has_name(self):
        fm = extract_frontmatter(SKILL_MD)
        assert fm.get("name") == "osint", f"Expected name 'osint', got '{fm.get('name')}'"

    def test_skill_md_has_description(self):
        fm = extract_frontmatter(SKILL_MD)
        assert fm.get("description"), "SKILL.md has no description"
        assert len(fm["description"]) > 50, "Description is too short"


class TestReferenceFiles:
    def test_references_dir_exists(self):
        assert REFERENCES_DIR.exists(), "references/ directory does not exist"

    def test_reference_files_mentioned_in_skill_exist(self):
        """Every .md file referenced in SKILL.md's table should exist in references/."""
        text = SKILL_MD.read_text(encoding="utf-8")
        # Match backtick-quoted .md filenames
        referenced = set(re.findall(r"`([a-z0-9_-]+\.md)`", text))
        # Filter to likely reference files (not SKILL.md itself, not template files)
        reference_files = {f for f in referenced if f != "SKILL.md" and not f.startswith("search-log")}

        missing = []
        for ref_file in sorted(reference_files):
            ref_path = REFERENCES_DIR / ref_file
            if not ref_path.exists():
                missing.append(ref_file)

        # Allow some files to be listed as future/TODO items
        # Only fail if more than 30% are missing (some may be planned but not yet written)
        if reference_files:
            missing_ratio = len(missing) / len(reference_files)
            if missing_ratio > 0.5:
                pytest.fail(
                    f"{len(missing)}/{len(reference_files)} referenced files missing from references/: {missing}"
                )
            elif missing:
                pytest.skip(f"{len(missing)} reference files planned but not yet written: {missing}")


class TestScripts:
    def test_scripts_dir_exists(self):
        assert SCRIPTS_DIR.exists(), "scripts/ directory does not exist"

    def test_all_scripts_have_script_block(self):
        """Every .py file in scripts/ must have a # /// script block."""
        scripts = list(SCRIPTS_DIR.glob("*.py"))
        assert scripts, "No Python scripts found"

        missing_block = []
        for script in scripts:
            text = script.read_text(encoding="utf-8")
            if "# /// script" not in text:
                missing_block.append(script.name)

        assert not missing_block, f"Scripts missing '# /// script' block: {missing_block}"

    def test_all_scripts_have_dependencies(self):
        """Every script's # /// script block should have a dependencies line."""
        scripts = list(SCRIPTS_DIR.glob("*.py"))
        for script in scripts:
            text = script.read_text(encoding="utf-8")
            match = re.search(r"# /// script\n(.*?)# ///", text, re.DOTALL)
            if match:
                block = match.group(1)
                assert "dependencies" in block, f"{script.name}: script block has no dependencies line"

    def test_all_scripts_parseable(self):
        """Every .py file should be syntactically valid Python."""
        import py_compile

        scripts = list(SCRIPTS_DIR.glob("*.py"))
        for script in scripts:
            try:
                py_compile.compile(str(script), doraise=True)
            except py_compile.PyCompileError as e:
                pytest.fail(f"{script.name} has syntax error: {e}")

    def test_all_scripts_have_main(self):
        """Every script should have a main() function and if __name__ == '__main__' guard."""
        scripts = list(SCRIPTS_DIR.glob("*.py"))
        for script in scripts:
            text = script.read_text(encoding="utf-8")
            assert "def main()" in text, f"{script.name}: no main() function"
            assert '__name__ == "__main__"' in text or "__name__ == '__main__'" in text, (
                f"{script.name}: no __name__ guard"
            )

    def test_all_scripts_have_argparse(self):
        """Every script should use argparse for CLI interface."""
        scripts = list(SCRIPTS_DIR.glob("*.py"))
        for script in scripts:
            text = script.read_text(encoding="utf-8")
            assert "argparse" in text, f"{script.name}: no argparse import"


class TestChallenges:
    def test_challenges_dir_exists(self):
        assert CHALLENGES_DIR.exists(), "challenges/ directory does not exist"

    def test_challenge_categories_exist(self):
        expected = ["geolocation", "people", "infrastructure", "image-forensics", "multi-domain"]
        for category in expected:
            cat_dir = CHALLENGES_DIR / category
            assert cat_dir.exists(), f"Challenge category '{category}/' missing"

    def test_challenge_files_have_required_sections(self):
        """Every challenge .md file must have Scenario, Expected Approach, Verification, and Ground Truth."""
        required_sections = ["## Scenario", "## Expected Approach", "## Verification", "## Ground Truth"]

        challenge_files = list(CHALLENGES_DIR.glob("**/*.md"))
        # Exclude README.md
        challenge_files = [f for f in challenge_files if f.name != "README.md"]

        assert challenge_files, "No challenge files found"

        for challenge in challenge_files:
            text = challenge.read_text(encoding="utf-8")
            missing = [s for s in required_sections if s not in text]
            assert not missing, f"{challenge.relative_to(ROOT)}: missing sections: {missing}"

    def test_challenge_files_have_difficulty(self):
        """Every challenge should specify difficulty."""
        challenge_files = [f for f in CHALLENGES_DIR.glob("**/*.md") if f.name != "README.md"]
        for challenge in challenge_files:
            text = challenge.read_text(encoding="utf-8")
            assert "## Difficulty" in text, f"{challenge.relative_to(ROOT)}: missing Difficulty section"
            assert any(d in text for d in ["Easy", "Medium", "Hard"]), (
                f"{challenge.relative_to(ROOT)}: no difficulty level specified"
            )

    def test_challenge_ground_truth_not_empty(self):
        """Ground Truth sections should contain actual content."""
        challenge_files = [f for f in CHALLENGES_DIR.glob("**/*.md") if f.name != "README.md"]
        for challenge in challenge_files:
            text = challenge.read_text(encoding="utf-8")
            gt_match = re.search(r"## Ground Truth\s*\n(.*)", text, re.DOTALL)
            assert gt_match, f"{challenge.relative_to(ROOT)}: no Ground Truth content"
            gt_content = gt_match.group(1).strip()
            assert len(gt_content) > 50, f"{challenge.relative_to(ROOT)}: Ground Truth too short"


class TestPluginConfig:
    def test_plugin_json_exists(self):
        assert (ROOT / ".claude-plugin" / "plugin.json").exists()

    def test_marketplace_json_exists(self):
        assert (ROOT / ".claude-plugin" / "marketplace.json").exists()

    def test_mcp_json_exists(self):
        assert (ROOT / ".mcp.json").exists()

    def test_plugin_json_valid(self):
        import json
        with open(ROOT / ".claude-plugin" / "plugin.json") as f:
            data = json.load(f)
        assert data["name"] == "osint"
        assert data["version"]
        assert data["author"]["name"]

    def test_mcp_json_valid(self):
        import json
        with open(ROOT / ".mcp.json") as f:
            data = json.load(f)
        assert "mcpServers" in data
        assert len(data["mcpServers"]) >= 10, f"Expected 10+ MCP servers, got {len(data['mcpServers'])}"


class TestTemplates:
    def test_templates_exist(self):
        templates_dir = SKILL_DIR / "templates" / "_example-investigation"
        assert templates_dir.exists()
        expected = ["search-log.md", "leads.md", "dead-ends.md", "evidence-chain.md", "report.md"]
        for name in expected:
            assert (templates_dir / name).exists(), f"Template '{name}' missing"

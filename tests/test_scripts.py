# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8.0"]
# ///
"""Script validation tests — verify all OSINT scripts are well-formed and runnable.

Non-integration tests verify structure and syntax.
Integration tests (marked with @pytest.mark.integration) hit real APIs.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).parent.parent / "skills" / "osint" / "scripts"
UV_BIN = shutil.which("uv") or "uv"


def get_all_scripts() -> list[Path]:
    """Get all Python scripts in the scripts directory."""
    return sorted(SCRIPTS_DIR.glob("*.py"))


class TestScriptHelp:
    """Verify every script responds to --help without errors."""

    @pytest.fixture(params=get_all_scripts(), ids=lambda p: p.name)
    def script(self, request):
        return request.param

    def test_help_flag(self, script):
        """Every script should accept --help and exit 0 (via uv run for dependency resolution)."""
        result = subprocess.run(
            [UV_BIN, "run", str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0, f"{script.name} --help failed:\n{result.stderr}"
        assert "usage:" in result.stdout.lower() or "optional arguments" in result.stdout.lower(), (
            f"{script.name} --help output doesn't look like argparse output"
        )


class TestScriptStructure:
    """Verify script code quality without running them."""

    @pytest.fixture(params=get_all_scripts(), ids=lambda p: p.name)
    def script(self, request):
        return request.param

    def test_has_docstring(self, script):
        """Every script should have a module docstring."""
        text = script.read_text(encoding="utf-8")
        # Look for triple-quote docstring after the script block
        assert '"""' in text or "'''" in text, f"{script.name}: no docstring found"

    def test_has_logging(self, script):
        """Every script should use logging (not print for diagnostics)."""
        text = script.read_text(encoding="utf-8")
        assert "import logging" in text or "from logging" in text, (
            f"{script.name}: should use logging module"
        )

    def test_json_output(self, script):
        """Every script should import json for structured output."""
        text = script.read_text(encoding="utf-8")
        assert "import json" in text, f"{script.name}: should import json for output"


# --- Integration tests (require network) ---


@pytest.mark.integration
class TestDNSScript:
    def test_dns_all(self):
        result = subprocess.run(
            [UV_BIN, "run", str(SCRIPTS_DIR / "query_dns.py"), "all", "example.com"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        import json
        data = json.loads(result.stdout)
        assert data["domain"] == "example.com"
        assert "records" in data
        assert "A" in data["records"]


@pytest.mark.integration
class TestCrtshScript:
    def test_crtsh_subdomains(self):
        result = subprocess.run(
            [UV_BIN, "run", str(SCRIPTS_DIR / "query_crtsh.py"), "subdomains", "example.com"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0
        import json
        data = json.loads(result.stdout)
        assert data["domain"] == "example.com"
        assert "subdomains" in data


@pytest.mark.integration
class TestShodanScript:
    def test_shodan_lookup(self):
        result = subprocess.run(
            [UV_BIN, "run", str(SCRIPTS_DIR / "query_shodan_internetdb.py"), "8.8.8.8"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        import json
        data = json.loads(result.stdout)
        assert data["ip"] == "8.8.8.8"


@pytest.mark.integration
class TestBlockchainScript:
    def test_btc_lookup(self):
        # Satoshi's address — always exists
        result = subprocess.run(
            [UV_BIN, "run", str(SCRIPTS_DIR / "query_blockchain.py"), "btc",
             "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0
        import json
        data = json.loads(result.stdout)
        assert data["chain"] == "bitcoin"
        assert data["balance_sat"] >= 0

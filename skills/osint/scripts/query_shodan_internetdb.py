# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Shodan InternetDB lookup for OSINT investigations.

Free API — no API key required. Returns open ports, hostnames, CPEs, and vulns for an IP.

Usage:
    uv run query_shodan_internetdb.py 8.8.8.8
    uv run query_shodan_internetdb.py 1.1.1.1
"""

import argparse
import json
import logging
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

INTERNETDB_URL = "https://internetdb.shodan.io"


def lookup(ip: str) -> dict:
    """Look up an IP address in Shodan's InternetDB."""
    try:
        resp = httpx.get(f"{INTERNETDB_URL}/{ip}", timeout=15)
        if resp.status_code == 404:
            log.info("No data found for %s in InternetDB", ip)
            return {"ip": ip, "found": False}
        resp.raise_for_status()
        data = resp.json()
        data["found"] = True
        log.info(
            "Found data for %s: %d ports, %d hostnames, %d vulns",
            ip,
            len(data.get("ports", [])),
            len(data.get("hostnames", [])),
            len(data.get("vulns", [])),
        )
        return data
    except httpx.HTTPStatusError as e:
        log.error("Shodan InternetDB returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"ip": ip, "error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        log.error("Shodan InternetDB lookup failed: %s", e)
        return {"ip": ip, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Shodan InternetDB lookup (free, no API key)")
    parser.add_argument("ip", help="IP address to look up")
    args = parser.parse_args()

    result = lookup(args.ip)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

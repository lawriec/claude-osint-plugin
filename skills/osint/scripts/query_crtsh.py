# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Certificate transparency search via crt.sh for OSINT investigations.

Usage:
    uv run query_crtsh.py search example.com
    uv run query_crtsh.py subdomains example.com
"""

import argparse
import json
import logging
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

CRTSH_URL = "https://crt.sh/"


def search_certificates(domain: str, wildcard: bool = True) -> list[dict]:
    """Search for certificates issued for a domain."""
    query = f"%.{domain}" if wildcard else domain
    try:
        resp = httpx.get(CRTSH_URL, params={"q": query, "output": "json"}, timeout=30)
        resp.raise_for_status()
        certs = resp.json()
        results = []
        seen = set()
        for cert in certs:
            cert_id = cert.get("id")
            if cert_id in seen:
                continue
            seen.add(cert_id)
            results.append(
                {
                    "id": cert_id,
                    "logged_at": cert.get("entry_timestamp"),
                    "not_before": cert.get("not_before"),
                    "not_after": cert.get("not_after"),
                    "common_name": cert.get("common_name"),
                    "name_value": cert.get("name_value"),
                    "issuer_name": cert.get("issuer_name"),
                }
            )
        log.info("Found %d unique certificates for %s", len(results), domain)
        return results
    except httpx.HTTPStatusError as e:
        log.error("crt.sh returned %d: %s", e.response.status_code, e.response.text[:200])
        return []
    except Exception as e:
        log.error("crt.sh search failed: %s", e)
        return []


def extract_subdomains(domain: str) -> list[str]:
    """Extract unique subdomains from certificate transparency logs."""
    certs = search_certificates(domain)
    subdomains = set()
    for cert in certs:
        name_value = cert.get("name_value", "")
        for name in name_value.split("\n"):
            name = name.strip().lower()
            if (name and (name.endswith(f".{domain}") or name == domain)) and not name.startswith("*"):
                subdomains.add(name)
    sorted_subs = sorted(subdomains)
    log.info("Found %d unique subdomains for %s", len(sorted_subs), domain)
    return sorted_subs


def main():
    parser = argparse.ArgumentParser(description="Certificate transparency search via crt.sh")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search for certificates")
    search_parser.add_argument("domain", help="Domain to search")
    search_parser.add_argument("--exact", action="store_true", help="Exact match (no wildcard)")

    sub_parser = subparsers.add_parser("subdomains", help="Extract subdomains from certs")
    sub_parser.add_argument("domain", help="Domain to search")

    args = parser.parse_args()

    if args.command == "search":
        result = {
            "domain": args.domain,
            "certificates": search_certificates(args.domain, wildcard=not getattr(args, "exact", False)),
        }
    elif args.command == "subdomains":
        result = {
            "domain": args.domain,
            "subdomains": extract_subdomains(args.domain),
        }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

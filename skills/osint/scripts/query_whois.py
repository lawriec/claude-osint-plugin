# /// script
# requires-python = ">=3.11"
# dependencies = ["python-whois>=0.9"]
# ///
"""WHOIS lookup tool for OSINT investigations.

Usage:
    uv run query_whois.py lookup example.com
    uv run query_whois.py registrar example.com
    uv run query_whois.py dates example.com
"""

import argparse
import json
import logging
import sys
from datetime import datetime

import whois

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)


def serialize(obj):
    """JSON serializer for objects not serializable by default."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    return str(obj)


def lookup(domain: str) -> dict:
    """Full WHOIS lookup for a domain."""
    try:
        w = whois.whois(domain)
        data = {}
        for key in [
            "domain_name",
            "registrar",
            "whois_server",
            "creation_date",
            "expiration_date",
            "updated_date",
            "name_servers",
            "status",
            "emails",
            "name",
            "org",
            "address",
            "city",
            "state",
            "registrant_postal_code",
            "country",
            "dnssec",
        ]:
            val = getattr(w, key, None)
            if val is not None:
                if isinstance(val, list) and len(val) == 1:
                    val = val[0]
                data[key] = val
        return {"domain": domain, "whois": data}
    except Exception as e:
        log.error("WHOIS lookup failed for %s: %s", domain, e)
        return {"domain": domain, "error": str(e)}


def registrar_info(domain: str) -> dict:
    """Extract registrar information only."""
    try:
        w = whois.whois(domain)
        return {
            "domain": domain,
            "registrar": w.registrar,
            "whois_server": w.whois_server,
            "name_servers": w.name_servers,
        }
    except Exception as e:
        log.error("WHOIS lookup failed for %s: %s", domain, e)
        return {"domain": domain, "error": str(e)}


def date_info(domain: str) -> dict:
    """Extract date information only."""
    try:
        w = whois.whois(domain)
        return {
            "domain": domain,
            "creation_date": w.creation_date,
            "expiration_date": w.expiration_date,
            "updated_date": w.updated_date,
        }
    except Exception as e:
        log.error("WHOIS lookup failed for %s: %s", domain, e)
        return {"domain": domain, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="WHOIS lookup for OSINT")
    subparsers = parser.add_subparsers(dest="command", required=True)

    lookup_parser = subparsers.add_parser("lookup", help="Full WHOIS lookup")
    lookup_parser.add_argument("domain", help="Domain to query")

    reg_parser = subparsers.add_parser("registrar", help="Registrar info only")
    reg_parser.add_argument("domain", help="Domain to query")

    date_parser = subparsers.add_parser("dates", help="Date info only")
    date_parser.add_argument("domain", help="Domain to query")

    args = parser.parse_args()

    if args.command == "lookup":
        result = lookup(args.domain)
    elif args.command == "registrar":
        result = registrar_info(args.domain)
    elif args.command == "dates":
        result = date_info(args.domain)

    print(json.dumps(result, indent=2, default=serialize))


if __name__ == "__main__":
    main()

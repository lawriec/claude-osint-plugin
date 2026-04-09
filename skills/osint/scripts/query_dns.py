# /// script
# requires-python = ">=3.11"
# dependencies = ["dnspython>=2.6"]
# ///
"""DNS enumeration tool for OSINT investigations.

Usage:
    uv run query_dns.py all example.com
    uv run query_dns.py mx example.com
    uv run query_dns.py txt example.com
    uv run query_dns.py ns example.com
    uv run query_dns.py reverse 8.8.8.8
"""

import argparse
import json
import logging
import sys

import dns.resolver
import dns.reversename

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

RECORD_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "SOA", "CNAME", "CAA", "SRV"]


def query_records(domain: str, rdtype: str) -> list[dict]:
    """Query DNS records of a specific type."""
    results = []
    try:
        answers = dns.resolver.resolve(domain, rdtype)
        for rdata in answers:
            record = {"type": rdtype, "value": str(rdata), "ttl": answers.rrset.ttl}
            if rdtype == "MX":
                record["priority"] = rdata.preference
                record["exchange"] = str(rdata.exchange)
            elif rdtype == "SOA":
                record["mname"] = str(rdata.mname)
                record["rname"] = str(rdata.rname)
                record["serial"] = rdata.serial
                record["refresh"] = rdata.refresh
                record["retry"] = rdata.retry
                record["expire"] = rdata.expire
                record["minimum"] = rdata.minimum
            elif rdtype == "SRV":
                record["priority"] = rdata.priority
                record["weight"] = rdata.weight
                record["port"] = rdata.port
                record["target"] = str(rdata.target)
            results.append(record)
    except dns.resolver.NoAnswer:
        log.debug("No %s records for %s", rdtype, domain)
    except dns.resolver.NXDOMAIN:
        log.error("Domain %s does not exist", domain)
    except dns.resolver.NoNameservers:
        log.error("No nameservers available for %s", domain)
    except Exception as e:
        log.warning("Error querying %s for %s: %s", rdtype, domain, e)
    return results


def query_all(domain: str) -> dict:
    """Query all common record types for a domain."""
    result = {"domain": domain, "records": {}}
    for rdtype in RECORD_TYPES:
        records = query_records(domain, rdtype)
        if records:
            result["records"][rdtype] = records
    return result


def reverse_lookup(ip: str) -> dict:
    """Perform reverse DNS lookup on an IP address."""
    try:
        rev_name = dns.reversename.from_address(ip)
        answers = dns.resolver.resolve(rev_name, "PTR")
        hostnames = [str(rdata) for rdata in answers]
        return {"ip": ip, "hostnames": hostnames}
    except Exception as e:
        log.error("Reverse lookup failed for %s: %s", ip, e)
        return {"ip": ip, "hostnames": [], "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="DNS enumeration for OSINT")
    subparsers = parser.add_subparsers(dest="command", required=True)

    all_parser = subparsers.add_parser("all", help="Query all record types")
    all_parser.add_argument("domain", help="Domain to query")

    for rdtype in ["a", "aaaa", "mx", "txt", "ns", "soa", "cname", "caa", "srv"]:
        p = subparsers.add_parser(rdtype, help=f"Query {rdtype.upper()} records")
        p.add_argument("domain", help="Domain to query")

    rev_parser = subparsers.add_parser("reverse", help="Reverse DNS lookup")
    rev_parser.add_argument("ip", help="IP address to look up")

    args = parser.parse_args()

    if args.command == "all":
        result = query_all(args.domain)
    elif args.command == "reverse":
        result = reverse_lookup(args.ip)
    else:
        rdtype = args.command.upper()
        records = query_records(args.domain, rdtype)
        result = {"domain": args.domain, "type": rdtype, "records": records}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

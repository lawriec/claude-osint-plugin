# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""VirusTotal API lookup for OSINT investigations.

Query domains, IPs, URLs, and file hashes via the VirusTotal v3 API.
Requires a free API key (4 requests/minute) set as VT_API_KEY env var.

Usage:
    uv run query_virustotal.py domain example.com
    uv run query_virustotal.py ip 8.8.8.8
    uv run query_virustotal.py url "https://example.com/page"
    uv run query_virustotal.py hash 44d88612fea8a8f36de82e1278abb02f
"""

import argparse
import base64
import json
import logging
import os
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

BASE_URL = "https://www.virustotal.com/api/v3"


def _get_api_key() -> str | None:
    """Read VT_API_KEY from environment."""
    key = os.environ.get("VT_API_KEY", "").strip()
    if not key:
        log.error("VT_API_KEY environment variable not set. Get a free key at https://www.virustotal.com/gui/join")
        return None
    return key


def _make_request(endpoint: str, api_key: str) -> dict | None:
    """Make an authenticated GET request to the VirusTotal API."""
    log.info("Note: Free VT tier allows 4 requests/minute and 500/day")
    try:
        resp = httpx.get(
            f"{BASE_URL}/{endpoint}",
            headers={"x-apikey": api_key},
            timeout=30,
        )
        if resp.status_code == 401:
            log.error("Invalid API key. Check your VT_API_KEY.")
            return None
        if resp.status_code == 429:
            log.error("Rate limited. Free tier: 4 requests/min. Wait and retry.")
            return None
        if resp.status_code == 404:
            log.info("Resource not found in VirusTotal database.")
            return None
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        log.error("VirusTotal API returned %d: %s", e.response.status_code, e.response.text[:200])
        return None
    except Exception as e:
        log.error("VirusTotal request failed: %s", e)
        return None


def _extract_analysis_stats(attrs: dict) -> dict:
    """Extract last_analysis_stats into a flat summary."""
    stats = attrs.get("last_analysis_stats", {})
    return {
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "undetected": stats.get("undetected", 0),
        "harmless": stats.get("harmless", 0),
        "timeout": stats.get("timeout", 0),
    }


def lookup_domain(domain: str) -> dict:
    """Get domain report from VirusTotal."""
    api_key = _get_api_key()
    if not api_key:
        return {"domain": domain, "error": "VT_API_KEY not set"}

    data = _make_request(f"domains/{domain}", api_key)
    if data is None:
        return {"domain": domain, "error": "Lookup failed or domain not found"}

    attrs = data.get("data", {}).get("attributes", {})
    result = {
        "domain": domain,
        "reputation": attrs.get("reputation", 0),
        "registrar": attrs.get("registrar"),
        "creation_date": attrs.get("creation_date"),
        "last_modification_date": attrs.get("last_modification_date"),
        "last_analysis_date": attrs.get("last_analysis_date"),
        "analysis_stats": _extract_analysis_stats(attrs),
        "categories": attrs.get("categories", {}),
        "popularity_ranks": attrs.get("popularity_ranks", {}),
        "whois": attrs.get("whois", "")[:500] if attrs.get("whois") else None,
        "last_dns_records": [],
        "tags": attrs.get("tags", []),
    }

    for rec in attrs.get("last_dns_records", [])[:20]:
        result["last_dns_records"].append({
            "type": rec.get("type"),
            "value": rec.get("value"),
            "ttl": rec.get("ttl"),
        })

    log.info(
        "Domain %s: reputation=%s, malicious=%d, harmless=%d",
        domain,
        result["reputation"],
        result["analysis_stats"]["malicious"],
        result["analysis_stats"]["harmless"],
    )
    return result


def lookup_ip(ip: str) -> dict:
    """Get IP address report from VirusTotal."""
    api_key = _get_api_key()
    if not api_key:
        return {"ip": ip, "error": "VT_API_KEY not set"}

    data = _make_request(f"ip_addresses/{ip}", api_key)
    if data is None:
        return {"ip": ip, "error": "Lookup failed or IP not found"}

    attrs = data.get("data", {}).get("attributes", {})
    result = {
        "ip": ip,
        "reputation": attrs.get("reputation", 0),
        "asn": attrs.get("asn"),
        "as_owner": attrs.get("as_owner"),
        "country": attrs.get("country"),
        "continent": attrs.get("continent"),
        "network": attrs.get("network"),
        "regional_internet_registry": attrs.get("regional_internet_registry"),
        "last_analysis_date": attrs.get("last_analysis_date"),
        "analysis_stats": _extract_analysis_stats(attrs),
        "whois": attrs.get("whois", "")[:500] if attrs.get("whois") else None,
        "tags": attrs.get("tags", []),
    }

    log.info(
        "IP %s: AS%s (%s), country=%s, malicious=%d",
        ip,
        result["asn"],
        result["as_owner"],
        result["country"],
        result["analysis_stats"]["malicious"],
    )
    return result


def lookup_url(url: str) -> dict:
    """Get URL analysis from VirusTotal."""
    api_key = _get_api_key()
    if not api_key:
        return {"url": url, "error": "VT_API_KEY not set"}

    # VT uses base64-encoded URL (without padding) as the identifier
    url_id = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
    data = _make_request(f"urls/{url_id}", api_key)
    if data is None:
        return {"url": url, "error": "Lookup failed or URL not found"}

    attrs = data.get("data", {}).get("attributes", {})
    result = {
        "url": attrs.get("url", url),
        "final_url": attrs.get("last_final_url"),
        "reputation": attrs.get("reputation", 0),
        "title": attrs.get("title"),
        "last_http_response_code": attrs.get("last_http_response_code"),
        "last_http_response_content_length": attrs.get("last_http_response_content_length"),
        "last_analysis_date": attrs.get("last_analysis_date"),
        "analysis_stats": _extract_analysis_stats(attrs),
        "categories": attrs.get("categories", {}),
        "outgoing_links": attrs.get("outgoing_links", [])[:10],
        "tags": attrs.get("tags", []),
        "trackers": [t.get("name") for t in attrs.get("trackers", {}).values()] if attrs.get("trackers") else [],
    }

    log.info(
        "URL %s: status=%s, malicious=%d",
        url[:60],
        result["last_http_response_code"],
        result["analysis_stats"]["malicious"],
    )
    return result


def lookup_hash(file_hash: str) -> dict:
    """Get file hash report from VirusTotal."""
    api_key = _get_api_key()
    if not api_key:
        return {"hash": file_hash, "error": "VT_API_KEY not set"}

    data = _make_request(f"files/{file_hash}", api_key)
    if data is None:
        return {"hash": file_hash, "error": "Lookup failed or hash not found"}

    attrs = data.get("data", {}).get("attributes", {})
    result = {
        "hash_queried": file_hash,
        "md5": attrs.get("md5"),
        "sha1": attrs.get("sha1"),
        "sha256": attrs.get("sha256"),
        "meaningful_name": attrs.get("meaningful_name"),
        "type_description": attrs.get("type_description"),
        "type_tag": attrs.get("type_tag"),
        "size": attrs.get("size"),
        "first_submission_date": attrs.get("first_submission_date"),
        "last_submission_date": attrs.get("last_submission_date"),
        "last_analysis_date": attrs.get("last_analysis_date"),
        "times_submitted": attrs.get("times_submitted"),
        "reputation": attrs.get("reputation", 0),
        "analysis_stats": _extract_analysis_stats(attrs),
        "popular_threat_classification": attrs.get("popular_threat_classification"),
        "names": attrs.get("names", [])[:10],
        "tags": attrs.get("tags", []),
    }

    log.info(
        "Hash %s: %s, malicious=%d/%d engines",
        file_hash[:16],
        result["type_description"],
        result["analysis_stats"]["malicious"],
        sum(result["analysis_stats"].values()),
    )
    return result


def main():
    parser = argparse.ArgumentParser(
        description="VirusTotal API lookup for OSINT (free tier: 4 req/min). "
        "Requires VT_API_KEY environment variable.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    domain_parser = subparsers.add_parser("domain", help="Get domain report")
    domain_parser.add_argument("domain", help="Domain name to look up")

    ip_parser = subparsers.add_parser("ip", help="Get IP address report")
    ip_parser.add_argument("ip", help="IP address to look up")

    url_parser = subparsers.add_parser("url", help="Get URL analysis")
    url_parser.add_argument("url", help="URL to look up")

    hash_parser = subparsers.add_parser("hash", help="Get file hash report")
    hash_parser.add_argument("hash", help="MD5, SHA-1, or SHA-256 hash")

    args = parser.parse_args()

    if args.command == "domain":
        result = lookup_domain(args.domain)
    elif args.command == "ip":
        result = lookup_ip(args.ip)
    elif args.command == "url":
        result = lookup_url(args.url)
    elif args.command == "hash":
        result = lookup_hash(args.hash)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

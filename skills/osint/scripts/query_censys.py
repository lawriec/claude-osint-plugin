# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Censys Search API for OSINT investigations.

Requires free API credentials (250 queries/month). Register at https://censys.io
and set CENSYS_API_ID and CENSYS_API_SECRET environment variables.

Usage:
    uv run query_censys.py host 8.8.8.8
    uv run query_censys.py host 1.1.1.1
    uv run query_censys.py search "services.service_name: HTTP"
    uv run query_censys.py search "services.service_name: SSH AND location.country: Germany" --per-page 50
    uv run query_censys.py search "services.port: 443 AND services.tls.certificates.leaf.subject.common_name: *.com"
"""

import argparse
import json
import logging
import os
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

BASE_URL = "https://search.censys.io/api/v2"


def _get_auth() -> tuple[str, str] | None:
    """Read Censys API credentials from environment variables."""
    api_id = os.environ.get("CENSYS_API_ID", "").strip()
    api_secret = os.environ.get("CENSYS_API_SECRET", "").strip()
    if not api_id or not api_secret:
        return None
    return (api_id, api_secret)


def _auth_error() -> dict:
    """Return an error dict when API credentials are missing."""
    log.error(
        "CENSYS_API_ID and CENSYS_API_SECRET environment variables are required. "
        "Register for free API keys at https://censys.io (250 queries/month on free tier)."
    )
    return {
        "error": "Missing API credentials",
        "detail": "Set CENSYS_API_ID and CENSYS_API_SECRET environment variables. "
        "Register at https://censys.io for free API keys (250 queries/month).",
    }


def lookup_host(ip: str) -> dict:
    """Get details for a specific IP address from Censys."""
    auth = _get_auth()
    if auth is None:
        return _auth_error()

    try:
        resp = httpx.get(f"{BASE_URL}/hosts/{ip}", auth=auth, timeout=30)
        if resp.status_code == 404:
            log.info("No data found for %s in Censys", ip)
            return {"ip": ip, "found": False}
        resp.raise_for_status()
        data = resp.json()

        result_data = data.get("result", {})

        services = []
        for svc in result_data.get("services", []):
            services.append({
                "port": svc.get("port"),
                "service_name": svc.get("service_name"),
                "transport_protocol": svc.get("transport_protocol"),
                "extended_service_name": svc.get("extended_service_name"),
                "certificate": svc.get("certificate"),
            })

        location = result_data.get("location", {})
        autonomous_system = result_data.get("autonomous_system", {})

        result = {
            "ip": result_data.get("ip", ip),
            "found": True,
            "services": services,
            "services_count": len(services),
            "location": {
                "country": location.get("country"),
                "country_code": location.get("country_code"),
                "city": location.get("city"),
                "province": location.get("province"),
                "postal_code": location.get("postal_code"),
                "timezone": location.get("timezone"),
                "continent": location.get("continent"),
                "coordinates": location.get("coordinates"),
            },
            "autonomous_system": {
                "asn": autonomous_system.get("asn"),
                "name": autonomous_system.get("name"),
                "description": autonomous_system.get("description"),
                "bgp_prefix": autonomous_system.get("bgp_prefix"),
                "country_code": autonomous_system.get("country_code"),
            },
            "operating_system": result_data.get("operating_system"),
            "last_updated_at": result_data.get("last_updated_at"),
            "dns": result_data.get("dns"),
            "whois": result_data.get("whois"),
        }

        log.info(
            "Censys host %s: %d services, %s, AS%s (%s)",
            ip,
            len(services),
            location.get("country", "unknown location"),
            autonomous_system.get("asn", "?"),
            autonomous_system.get("name", "unknown"),
        )
        return result
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            log.error("Censys authentication failed. Check your CENSYS_API_ID and CENSYS_API_SECRET.")
            return {"ip": ip, "error": "HTTP 401 Unauthorized", "detail": "Check API credentials."}
        if e.response.status_code == 403:
            log.error("Censys access denied. Your API key may lack permissions or quota is exhausted.")
            return {"ip": ip, "error": "HTTP 403 Forbidden", "detail": "Check API key permissions or quota."}
        if e.response.status_code == 429:
            log.error("Censys rate limit exceeded. Free tier allows 250 queries/month.")
            return {"ip": ip, "error": "HTTP 429 Rate Limited", "detail": "Free tier: 250 queries/month."}
        log.error("Censys returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"ip": ip, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("Censys host lookup failed: %s", e)
        return {"ip": ip, "error": str(e)}


def search_hosts(query: str, per_page: int = 25) -> dict:
    """Search Censys hosts by query string."""
    auth = _get_auth()
    if auth is None:
        return _auth_error()

    try:
        resp = httpx.get(
            f"{BASE_URL}/hosts/search",
            params={"q": query, "per_page": min(per_page, 100)},
            auth=auth,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        result_data = data.get("result", {})
        hits = result_data.get("hits", [])

        results = []
        for hit in hits:
            location = hit.get("location", {})
            autonomous_system = hit.get("autonomous_system", {})

            services_summary = []
            for svc in hit.get("services", []):
                services_summary.append({
                    "port": svc.get("port"),
                    "service_name": svc.get("service_name"),
                    "transport_protocol": svc.get("transport_protocol"),
                    "extended_service_name": svc.get("extended_service_name"),
                })

            results.append({
                "ip": hit.get("ip"),
                "services": services_summary,
                "services_count": len(services_summary),
                "location": {
                    "country": location.get("country"),
                    "country_code": location.get("country_code"),
                    "city": location.get("city"),
                    "continent": location.get("continent"),
                    "coordinates": location.get("coordinates"),
                },
                "autonomous_system": {
                    "asn": autonomous_system.get("asn"),
                    "name": autonomous_system.get("name"),
                    "description": autonomous_system.get("description"),
                    "bgp_prefix": autonomous_system.get("bgp_prefix"),
                },
                "operating_system": hit.get("operating_system"),
                "last_updated_at": hit.get("last_updated_at"),
                "dns": hit.get("dns"),
            })

        total = result_data.get("total", len(results))
        links = result_data.get("links", {})
        has_next = links.get("next", "") != ""

        log.info("Censys search '%s': %d results (total: %s)", query, len(results), total)
        if has_next:
            log.info("More results available; increase --per-page or refine query")

        return {
            "query": query,
            "total": total,
            "showing": len(results),
            "has_more": has_next,
            "results": results,
        }
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            log.error("Censys authentication failed. Check your CENSYS_API_ID and CENSYS_API_SECRET.")
            return {"query": query, "error": "HTTP 401 Unauthorized", "detail": "Check API credentials."}
        if e.response.status_code == 403:
            log.error("Censys access denied. Your API key may lack permissions or quota is exhausted.")
            return {"query": query, "error": "HTTP 403 Forbidden", "detail": "Check API key permissions or quota."}
        if e.response.status_code == 429:
            log.error("Censys rate limit exceeded. Free tier allows 250 queries/month.")
            return {"query": query, "error": "HTTP 429 Rate Limited", "detail": "Free tier: 250 queries/month."}
        log.error("Censys returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"query": query, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("Censys search failed: %s", e)
        return {"query": query, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Censys Search API (free tier: 250 queries/month). "
        "Requires CENSYS_API_ID and CENSYS_API_SECRET environment variables.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    host_parser = subparsers.add_parser("host", help="Get details for a specific IP address")
    host_parser.add_argument("ip", help="IP address to look up")

    search_parser = subparsers.add_parser("search", help="Search hosts by query string")
    search_parser.add_argument(
        "query", help="Censys search query (e.g. 'services.service_name: HTTP AND location.country: Germany')"
    )
    search_parser.add_argument("--per-page", type=int, default=25, help="Results per page (default: 25, max: 100)")

    args = parser.parse_args()

    if args.command == "host":
        result = lookup_host(args.ip)
    elif args.command == "search":
        result = search_hosts(args.query, per_page=args.per_page)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

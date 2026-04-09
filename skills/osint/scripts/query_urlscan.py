# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""URLScan.io search for OSINT investigations.

Free API (no auth needed for search; auth needed for submissions).
Supports Elasticsearch query syntax for powerful filtering.

Usage:
    uv run query_urlscan.py search "domain:example.com"
    uv run query_urlscan.py search "ip:1.2.3.4" --size 20
    uv run query_urlscan.py search "server:nginx AND country:US"
    uv run query_urlscan.py search "filename:malware.exe"
    uv run query_urlscan.py search "asn:AS13335"
    uv run query_urlscan.py result 01234567-89ab-cdef-0123-456789abcdef
    uv run query_urlscan.py dom 01234567-89ab-cdef-0123-456789abcdef
"""

import argparse
import json
import logging
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

BASE_URL = "https://urlscan.io/api/v1"


def search_scans(query: str, size: int = 10) -> dict:
    """Search URLScan.io scans using Elasticsearch query syntax.

    Supported query fields: domain, ip, filename, server, asn, country,
    page.url, page.domain, page.ip, page.server, page.asn, etc.
    """
    try:
        resp = httpx.get(
            f"{BASE_URL}/search/",
            params={"q": query, "size": min(size, 100)},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        results = []
        for r in data.get("results", []):
            task = r.get("task", {})
            page = r.get("page", {})
            stats = r.get("stats", {})

            results.append(
                {
                    "uuid": r.get("_id"),
                    "url": task.get("url"),
                    "domain": page.get("domain"),
                    "ip": page.get("ip"),
                    "country": page.get("country"),
                    "server": page.get("server"),
                    "asn": page.get("asn"),
                    "asnname": page.get("asnname"),
                    "status": page.get("status"),
                    "mime_type": page.get("mimeType"),
                    "title": page.get("title"),
                    "time": task.get("time"),
                    "visibility": task.get("visibility"),
                    "requests_count": stats.get("requests"),
                    "unique_ips": stats.get("uniqIPs"),
                    "report_url": f"https://urlscan.io/result/{r.get('_id')}/",
                    "screenshot_url": r.get("screenshot"),
                }
            )

        total = data.get("total", len(results))
        has_more = data.get("has_more", total > len(results))

        log.info("URLScan search '%s': %d results (total: %s)", query, len(results), total)
        if has_more:
            log.info("More results available; increase --size or refine query")

        return {
            "query": query,
            "total": total,
            "showing": len(results),
            "has_more": has_more,
            "results": results,
        }
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            log.error("Rate limited by URLScan.io. Wait a moment and try again.")
        else:
            log.error("URLScan.io returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"query": query, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("URLScan search failed: %s", e)
        return {"query": query, "error": str(e)}


def get_result(uuid: str) -> dict:
    """Get full scan result by UUID."""
    try:
        resp = httpx.get(f"{BASE_URL}/result/{uuid}/", timeout=30)
        if resp.status_code == 404:
            log.info("Scan %s not found (may still be processing)", uuid)
            return {"uuid": uuid, "found": False, "note": "Scan not found or still processing"}
        resp.raise_for_status()
        data = resp.json()

        task = data.get("task", {})
        page = data.get("page", {})
        lists = data.get("lists", {})
        meta = data.get("meta", {})
        stats = data.get("stats", {})
        verdicts = data.get("verdicts", {})

        result = {
            "uuid": uuid,
            "found": True,
            "task": {
                "url": task.get("url"),
                "domain": task.get("domain"),
                "time": task.get("time"),
                "visibility": task.get("visibility"),
                "method": task.get("method"),
                "source": task.get("source"),
            },
            "page": {
                "url": page.get("url"),
                "domain": page.get("domain"),
                "ip": page.get("ip"),
                "country": page.get("country"),
                "city": page.get("city"),
                "server": page.get("server"),
                "asn": page.get("asn"),
                "asnname": page.get("asnname"),
                "status": page.get("status"),
                "mime_type": page.get("mimeType"),
                "title": page.get("title"),
                "tls_issuer": page.get("tlsIssuer"),
                "tls_valid_from": page.get("tlsValidFrom"),
                "tls_valid_days": page.get("tlsValidDays"),
            },
            "lists": {
                "ips": lists.get("ips", []),
                "countries": lists.get("countries", []),
                "asns": lists.get("asns", []),
                "domains": lists.get("domains", []),
                "servers": lists.get("servers", []),
                "urls": lists.get("urls", [])[:20],
                "hashes": lists.get("hashes", [])[:10],
                "certificates": lists.get("certificates", [])[:10],
            },
            "stats": {
                "requests": stats.get("requests"),
                "unique_countries": stats.get("uniqCountries"),
                "unique_ips": stats.get("uniqIPs"),
                "data_length": stats.get("dataLength"),
                "encoded_data_length": stats.get("encodedDataLength"),
            },
            "verdicts": {
                "overall": verdicts.get("overall", {}),
                "urlscan": verdicts.get("urlscan", {}),
                "engines": verdicts.get("engines", {}),
                "community": verdicts.get("community", {}),
            },
            "meta_processors": list(meta.get("processors", {}).keys()) if meta.get("processors") else [],
            "report_url": f"https://urlscan.io/result/{uuid}/",
            "screenshot_url": f"https://urlscan.io/screenshots/{uuid}.png",
        }

        log.info("Scan result %s: %s (%s)", uuid, page.get("domain"), page.get("status"))
        return result
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            log.error("Rate limited by URLScan.io. Wait a moment and try again.")
        else:
            log.error("URLScan.io returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"uuid": uuid, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("URLScan result lookup failed: %s", e)
        return {"uuid": uuid, "error": str(e)}


def get_dom(uuid: str) -> dict:
    """Get DOM content for a scan by UUID."""
    try:
        resp = httpx.get(f"{BASE_URL}/dom/{uuid}/", timeout=30)
        if resp.status_code == 404:
            log.info("DOM for scan %s not found", uuid)
            return {"uuid": uuid, "found": False}
        resp.raise_for_status()

        dom_text = resp.text
        log.info("DOM for %s: %d characters", uuid, len(dom_text))

        return {
            "uuid": uuid,
            "found": True,
            "dom_length": len(dom_text),
            "dom": dom_text[:50000] if len(dom_text) > 50000 else dom_text,
            "truncated": len(dom_text) > 50000,
            "report_url": f"https://urlscan.io/result/{uuid}/",
        }
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            log.error("Rate limited by URLScan.io. Wait a moment and try again.")
        else:
            log.error("URLScan.io returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"uuid": uuid, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("URLScan DOM lookup failed: %s", e)
        return {"uuid": uuid, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="URLScan.io search (free, no API key for search). "
        "Supports Elasticsearch query syntax: domain:, ip:, server:, asn:, filename:, etc.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search URLScan.io scans")
    search_parser.add_argument("query", help="Search query (Elasticsearch syntax, e.g. 'domain:example.com')")
    search_parser.add_argument("--size", type=int, default=10, help="Number of results (default: 10, max: 100)")

    result_parser = subparsers.add_parser("result", help="Get full scan result by UUID")
    result_parser.add_argument("uuid", help="Scan UUID")

    dom_parser = subparsers.add_parser("dom", help="Get DOM content for a scan")
    dom_parser.add_argument("uuid", help="Scan UUID")

    args = parser.parse_args()

    if args.command == "search":
        result = search_scans(args.query, size=args.size)
    elif args.command == "result":
        result = get_result(args.uuid)
    elif args.command == "dom":
        result = get_dom(args.uuid)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

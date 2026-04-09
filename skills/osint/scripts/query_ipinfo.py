# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""IP geolocation and ASN lookup via ip-api.com for OSINT investigations.

Free API (no key needed, 45 requests/minute).

Usage:
    uv run query_ipinfo.py geo 8.8.8.8
    uv run query_ipinfo.py asn 1.1.1.1
    uv run query_ipinfo.py batch ips.txt
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

BASE_URL = "http://ip-api.com"

# Field bitmask 66846719 requests all available fields
ALL_FIELDS = 66846719


def log_rate_limit(resp: httpx.Response) -> None:
    """Log rate limit info from response headers if present."""
    remaining = resp.headers.get("X-Rl")
    ttl = resp.headers.get("X-Ttl")
    if remaining is not None:
        log.info("Rate limit: %s requests remaining, resets in %s seconds", remaining, ttl)
        if int(remaining) < 5:
            log.warning("Approaching rate limit! Only %s requests remaining (resets in %ss)", remaining, ttl)


def geo_lookup(ip: str) -> dict:
    """Geolocation lookup for a single IP address."""
    try:
        resp = httpx.get(
            f"{BASE_URL}/json/{ip}",
            params={"fields": ALL_FIELDS},
            timeout=15,
        )
        resp.raise_for_status()
        log_rate_limit(resp)
        data = resp.json()

        if data.get("status") == "fail":
            log.error("Lookup failed for %s: %s", ip, data.get("message"))
            return {"ip": ip, "error": data.get("message", "Unknown error")}

        result = {
            "ip": data.get("query", ip),
            "status": data.get("status"),
            "country": data.get("country"),
            "country_code": data.get("countryCode"),
            "region": data.get("regionName"),
            "region_code": data.get("region"),
            "city": data.get("city"),
            "zip": data.get("zip"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "timezone": data.get("timezone"),
            "isp": data.get("isp"),
            "org": data.get("org"),
            "as": data.get("as"),
            "asname": data.get("asname"),
            "reverse": data.get("reverse"),
            "mobile": data.get("mobile"),
            "proxy": data.get("proxy"),
            "hosting": data.get("hosting"),
            "continent": data.get("continent"),
            "continent_code": data.get("continentCode"),
            "district": data.get("district"),
            "offset": data.get("offset"),
            "currency": data.get("currency"),
        }

        if data.get("lat") is not None and data.get("lon") is not None:
            result["maps_url"] = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"

        log.info(
            "IP %s: %s, %s, %s (%s)",
            ip, data.get("city"), data.get("regionName"), data.get("country"), data.get("org"),
        )
        return result
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            log.error("Rate limited by ip-api.com (45 req/min). Wait and retry.")
        else:
            log.error("ip-api.com returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"ip": ip, "error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        log.error("IP geo lookup failed: %s", e)
        return {"ip": ip, "error": str(e)}


def asn_lookup(ip: str) -> dict:
    """ASN and network info for an IP, focused on AS/org/ISP fields."""
    try:
        resp = httpx.get(
            f"{BASE_URL}/json/{ip}",
            params={"fields": ALL_FIELDS},
            timeout=15,
        )
        resp.raise_for_status()
        log_rate_limit(resp)
        data = resp.json()

        if data.get("status") == "fail":
            log.error("Lookup failed for %s: %s", ip, data.get("message"))
            return {"ip": ip, "error": data.get("message", "Unknown error")}

        result = {
            "ip": data.get("query", ip),
            "as": data.get("as"),
            "asname": data.get("asname"),
            "org": data.get("org"),
            "isp": data.get("isp"),
            "reverse": data.get("reverse"),
            "hosting": data.get("hosting"),
            "proxy": data.get("proxy"),
            "mobile": data.get("mobile"),
            "country": data.get("country"),
            "country_code": data.get("countryCode"),
        }

        log.info("IP %s: %s (%s / %s)", ip, data.get("as"), data.get("org"), data.get("isp"))
        return result
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            log.error("Rate limited by ip-api.com (45 req/min). Wait and retry.")
        else:
            log.error("ip-api.com returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"ip": ip, "error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        log.error("ASN lookup failed: %s", e)
        return {"ip": ip, "error": str(e)}


def batch_lookup(filepath: str) -> dict:
    """Batch geolocation lookup from a file of IPs (one per line).

    Uses the ip-api.com batch endpoint (max 100 IPs per request).
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return {"error": f"File not found: {filepath}"}

        ips = [line.strip() for line in path.read_text().splitlines() if line.strip()]
        if not ips:
            return {"error": "No IPs found in file"}

        log.info("Processing %d IPs from %s", len(ips), filepath)

        all_results = []
        # Process in chunks of 100
        for i in range(0, len(ips), 100):
            chunk = ips[i:i + 100]
            log.info("Batch %d: processing IPs %d-%d of %d", i // 100 + 1, i + 1, i + len(chunk), len(ips))

            try:
                fields = (
                    "status,message,country,countryCode,regionName,city,"
                    "zip,lat,lon,timezone,isp,org,as,asname,reverse,"
                    "mobile,proxy,hosting,query"
                )
                payload = [{"query": ip, "fields": fields} for ip in chunk]
                resp = httpx.post(
                    f"{BASE_URL}/batch",
                    json=payload,
                    timeout=30,
                )
                resp.raise_for_status()
                log_rate_limit(resp)
                batch_data = resp.json()

                for item in batch_data:
                    entry = {
                        "ip": item.get("query"),
                        "status": item.get("status"),
                    }
                    if item.get("status") == "success":
                        entry.update({
                            "country": item.get("country"),
                            "country_code": item.get("countryCode"),
                            "region": item.get("regionName"),
                            "city": item.get("city"),
                            "zip": item.get("zip"),
                            "latitude": item.get("lat"),
                            "longitude": item.get("lon"),
                            "timezone": item.get("timezone"),
                            "isp": item.get("isp"),
                            "org": item.get("org"),
                            "as": item.get("as"),
                            "asname": item.get("asname"),
                            "reverse": item.get("reverse"),
                            "mobile": item.get("mobile"),
                            "proxy": item.get("proxy"),
                            "hosting": item.get("hosting"),
                        })
                        if item.get("lat") is not None and item.get("lon") is not None:
                            entry["maps_url"] = f"https://www.google.com/maps?q={item['lat']},{item['lon']}"
                    else:
                        entry["error"] = item.get("message", "Unknown error")

                    all_results.append(entry)

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    log.error("Rate limited on batch %d. Partial results returned.", i // 100 + 1)
                    break
                else:
                    log.error("Batch request failed: HTTP %d", e.response.status_code)
                    for ip in chunk:
                        all_results.append({"ip": ip, "error": f"HTTP {e.response.status_code}"})

        successful = sum(1 for r in all_results if r.get("status") == "success")
        log.info("Batch complete: %d/%d successful lookups", successful, len(all_results))

        return {
            "file": filepath,
            "total_ips": len(ips),
            "successful": successful,
            "failed": len(all_results) - successful,
            "results": all_results,
        }
    except Exception as e:
        log.error("Batch lookup failed: %s", e)
        return {"file": filepath, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="IP geolocation and ASN lookup via ip-api.com (free, 45 req/min)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    geo_parser = subparsers.add_parser("geo", help="Full geolocation lookup for an IP")
    geo_parser.add_argument("ip", help="IP address to look up")

    asn_parser = subparsers.add_parser("asn", help="ASN and network info for an IP")
    asn_parser.add_argument("ip", help="IP address to look up")

    batch_parser = subparsers.add_parser("batch", help="Batch lookup from file (one IP per line)")
    batch_parser.add_argument("file", help="Path to file with one IP per line (max 100 per request)")

    args = parser.parse_args()

    if args.command == "geo":
        result = geo_lookup(args.ip)
    elif args.command == "asn":
        result = asn_lookup(args.ip)
    elif args.command == "batch":
        result = batch_lookup(args.file)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

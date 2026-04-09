# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Vessel/ship tracking via Fintraffic AIS API for OSINT investigations.

Uses Finland's Fintraffic open AIS data (free, no auth needed).
Coverage: Baltic Sea and nearby waters. For global coverage, consider
MarineTraffic or VesselFinder (paid APIs).

Usage:
    uv run query_ais.py search "Viking Grace"
    uv run query_ais.py mmsi 230629000
    uv run query_ais.py location 230629000
"""

import argparse
import json
import logging
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

BASE_URL = "https://meri.digitraffic.fi/api/ais/v1"


def search_vessel(name: str) -> dict:
    """Search for vessels by name using Fintraffic AIS API.

    Fetches all vessel metadata and filters client-side by name substring match.
    """
    try:
        log.info("Fetching vessel list from Fintraffic (this may take a moment)...")
        resp = httpx.get(f"{BASE_URL}/vessels", timeout=60)
        resp.raise_for_status()
        vessels = resp.json()

        query = name.lower()
        matches = []
        for v in vessels:
            vessel_name = v.get("name") or ""
            if query in vessel_name.lower():
                matches.append(
                    {
                        "mmsi": v.get("mmsi"),
                        "name": v.get("name"),
                        "ship_type": v.get("shipType"),
                        "callsign": v.get("callSign"),
                        "imo": v.get("imo"),
                        "destination": v.get("destination"),
                        "draught": v.get("draught"),
                        "eta": v.get("eta"),
                        "pos_type": v.get("posType"),
                        "reference_point_a": v.get("referencePointA"),
                        "reference_point_b": v.get("referencePointB"),
                        "reference_point_c": v.get("referencePointC"),
                        "reference_point_d": v.get("referencePointD"),
                    }
                )

        log.info("Found %d vessel(s) matching '%s' (searched %d total)", len(matches), name, len(vessels))
        return {
            "query": name,
            "match_count": len(matches),
            "vessels": matches,
            "note": "Data from Fintraffic AIS (Baltic Sea coverage).",
        }
    except httpx.HTTPStatusError as e:
        log.error("Fintraffic API returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"query": name, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("Vessel search failed: %s", e)
        return {"query": name, "error": str(e)}


def lookup_mmsi(mmsi: int) -> dict:
    """Look up vessel metadata by MMSI."""
    try:
        resp = httpx.get(f"{BASE_URL}/vessels/{mmsi}", timeout=15)
        if resp.status_code == 404:
            log.info("No vessel found for MMSI %d", mmsi)
            return {"mmsi": mmsi, "found": False}
        resp.raise_for_status()
        data = resp.json()

        result = {
            "mmsi": data.get("mmsi"),
            "found": True,
            "name": data.get("name"),
            "ship_type": data.get("shipType"),
            "callsign": data.get("callSign"),
            "imo": data.get("imo"),
            "destination": data.get("destination"),
            "draught": data.get("draught"),
            "eta": data.get("eta"),
            "pos_type": data.get("posType"),
            "reference_point_a": data.get("referencePointA"),
            "reference_point_b": data.get("referencePointB"),
            "reference_point_c": data.get("referencePointC"),
            "reference_point_d": data.get("referencePointD"),
        }

        log.info("Vessel MMSI %d: %s (type %s)", mmsi, result["name"], result["ship_type"])
        return result
    except httpx.HTTPStatusError as e:
        log.error("Fintraffic API returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"mmsi": mmsi, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("MMSI lookup failed: %s", e)
        return {"mmsi": mmsi, "error": str(e)}


def get_location(mmsi: int) -> dict:
    """Get current vessel location by MMSI."""
    try:
        resp = httpx.get(f"{BASE_URL}/locations/{mmsi}", timeout=15)
        if resp.status_code == 404:
            log.info("No location data for MMSI %d", mmsi)
            return {"mmsi": mmsi, "found": False}
        resp.raise_for_status()
        data = resp.json()

        # The location endpoint returns a Feature or FeatureCollection
        if data.get("type") == "Feature":
            props = data.get("properties", {})
            coords = data.get("geometry", {}).get("coordinates", [])
            longitude = coords[0] if len(coords) > 0 else None
            latitude = coords[1] if len(coords) > 1 else None

            result = {
                "mmsi": props.get("mmsi", mmsi),
                "found": True,
                "longitude": longitude,
                "latitude": latitude,
                "sog": props.get("sog"),
                "cog": props.get("cog"),
                "nav_stat": props.get("navStat"),
                "rot": props.get("rot"),
                "heading": props.get("heading"),
                "timestamp": props.get("timestampExternal"),
            }

            if longitude is not None and latitude is not None:
                result["maps_url"] = f"https://www.google.com/maps?q={latitude},{longitude}"

            log.info("Vessel MMSI %d at %.4f, %.4f (SOG: %s)", mmsi, latitude or 0, longitude or 0, result["sog"])
            return result
        else:
            # Might be a FeatureCollection or other format
            log.info("Location data for MMSI %d returned in unexpected format", mmsi)
            return {"mmsi": mmsi, "found": True, "raw": data}

    except httpx.HTTPStatusError as e:
        log.error("Fintraffic API returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"mmsi": mmsi, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("Vessel location lookup failed: %s", e)
        return {"mmsi": mmsi, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Vessel/ship tracking via Fintraffic AIS (free, no API key). "
        "Covers Baltic Sea region. For global coverage, use MarineTraffic or VesselFinder.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search vessels by name")
    search_parser.add_argument("name", help="Vessel name (or partial name) to search for")

    mmsi_parser = subparsers.add_parser("mmsi", help="Look up vessel by MMSI")
    mmsi_parser.add_argument("number", type=int, help="MMSI number (e.g. 230629000)")

    loc_parser = subparsers.add_parser("location", help="Get current vessel location")
    loc_parser.add_argument("mmsi", type=int, help="MMSI number (e.g. 230629000)")

    args = parser.parse_args()

    if args.command == "search":
        result = search_vessel(args.name)
    elif args.command == "mmsi":
        result = lookup_mmsi(args.number)
    elif args.command == "location":
        result = get_location(args.mmsi)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

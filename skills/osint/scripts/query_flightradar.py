# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Aircraft tracking via OpenSky Network REST API for OSINT investigations.

Free API (no auth needed, ~100 requests/day for anonymous users).

Usage:
    uv run query_flightradar.py states
    uv run query_flightradar.py states --icao24 abc123
    uv run query_flightradar.py states --bbox 45.0,5.0,48.0,10.0
    uv run query_flightradar.py track abc123
    uv run query_flightradar.py arrivals EGLL
    uv run query_flightradar.py departures KJFK
    uv run query_flightradar.py arrivals EDDF --hours 12
"""

import argparse
import json
import logging
import sys
import time

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

BASE_URL = "https://opensky-network.org/api"

STATES_FIELDS = [
    "icao24", "callsign", "origin_country", "time_position", "last_contact",
    "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
    "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
    "spi", "position_source",
]


def parse_state_vector(sv: list) -> dict:
    """Map a raw state vector array to a named-field dict."""
    result = {}
    for i, field in enumerate(STATES_FIELDS):
        if i < len(sv):
            value = sv[i]
            if field == "callsign" and isinstance(value, str):
                value = value.strip()
            result[field] = value
    return result


def get_states(icao24: str | None = None, bbox: str | None = None) -> dict:
    """Get current aircraft states, optionally filtered by ICAO24 or bounding box."""
    params = {}
    if icao24:
        params["icao24"] = icao24.lower()
    if bbox:
        parts = [p.strip() for p in bbox.split(",")]
        if len(parts) != 4:
            return {"error": "Bounding box must be 4 comma-separated values: lamin,lomin,lamax,lomax"}
        params["lamin"] = parts[0]
        params["lomin"] = parts[1]
        params["lamax"] = parts[2]
        params["lomax"] = parts[3]

    try:
        resp = httpx.get(f"{BASE_URL}/states/all", params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        states_raw = data.get("states") or []
        states = [parse_state_vector(sv) for sv in states_raw]

        log.info("Retrieved %d aircraft state vectors (time: %s)", len(states), data.get("time"))
        return {
            "time": data.get("time"),
            "aircraft_count": len(states),
            "states": states,
        }
    except httpx.HTTPStatusError as e:
        log.error("OpenSky API returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("OpenSky states lookup failed: %s", e)
        return {"error": str(e)}


def get_track(icao24: str) -> dict:
    """Get flight track (waypoints) for a specific aircraft."""
    try:
        resp = httpx.get(
            f"{BASE_URL}/tracks/all",
            params={"icao24": icao24.lower(), "time": 0},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        waypoints = []
        for wp in data.get("path", []):
            waypoints.append({
                "time": wp[0] if len(wp) > 0 else None,
                "latitude": wp[1] if len(wp) > 1 else None,
                "longitude": wp[2] if len(wp) > 2 else None,
                "baro_altitude": wp[3] if len(wp) > 3 else None,
                "true_track": wp[4] if len(wp) > 4 else None,
                "on_ground": wp[5] if len(wp) > 5 else None,
            })

        log.info("Track for %s: %d waypoints", icao24, len(waypoints))
        return {
            "icao24": data.get("icao24", icao24),
            "callsign": (data.get("callsign") or "").strip(),
            "start_time": data.get("startTime"),
            "end_time": data.get("endTime"),
            "waypoint_count": len(waypoints),
            "waypoints": waypoints,
        }
    except httpx.HTTPStatusError as e:
        log.error("OpenSky API returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"icao24": icao24, "error": f"HTTP {e.response.status_code}", "detail": e.response.text[:200]}
    except Exception as e:
        log.error("OpenSky track lookup failed: %s", e)
        return {"icao24": icao24, "error": str(e)}


def get_flights(airport: str, flight_type: str, hours: int = 24) -> dict:
    """Get arrivals or departures for an airport."""
    now = int(time.time())
    begin = now - (hours * 3600)

    endpoint = "arrival" if flight_type == "arrivals" else "departure"
    try:
        resp = httpx.get(
            f"{BASE_URL}/flights/{endpoint}",
            params={"airport": airport.upper(), "begin": begin, "end": now},
            timeout=30,
        )
        resp.raise_for_status()
        flights = resp.json()

        results = []
        for f in flights:
            results.append({
                "icao24": f.get("icao24"),
                "callsign": (f.get("callsign") or "").strip(),
                "departure_airport": f.get("estDepartureAirport"),
                "arrival_airport": f.get("estArrivalAirport"),
                "first_seen": f.get("firstSeen"),
                "last_seen": f.get("lastSeen"),
                "departure_horiz_distance": f.get("estDepartureAirportHorizDistance"),
                "arrival_horiz_distance": f.get("estArrivalAirportHorizDistance"),
            })

        log.info("%s at %s (last %dh): %d flights", flight_type.capitalize(), airport, hours, len(results))
        return {
            "airport": airport.upper(),
            "type": flight_type,
            "time_range_hours": hours,
            "begin": begin,
            "end": now,
            "flight_count": len(results),
            "flights": results,
        }
    except httpx.HTTPStatusError as e:
        log.error("OpenSky API returned %d: %s", e.response.status_code, e.response.text[:200])
        return {
            "airport": airport, "type": flight_type,
            "error": f"HTTP {e.response.status_code}",
        }
    except Exception as e:
        log.error("OpenSky %s lookup failed: %s", flight_type, e)
        return {"airport": airport, "type": flight_type, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Aircraft tracking via OpenSky Network (free, no API key)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    states_parser = subparsers.add_parser("states", help="Get current aircraft states")
    states_parser.add_argument("--icao24", help="Filter by ICAO24 hex address (e.g. abc123)")
    states_parser.add_argument("--bbox", help="Bounding box: lamin,lomin,lamax,lomax (e.g. 45.0,5.0,48.0,10.0)")

    track_parser = subparsers.add_parser("track", help="Get flight track for an aircraft")
    track_parser.add_argument("icao24", help="ICAO24 hex address of the aircraft")

    arrivals_parser = subparsers.add_parser("arrivals", help="Get arrivals at an airport")
    arrivals_parser.add_argument("airport", help="ICAO airport code (e.g. EGLL, KJFK)")
    arrivals_parser.add_argument("--hours", type=int, default=24, help="Lookback hours (default: 24, max: 168)")

    departures_parser = subparsers.add_parser("departures", help="Get departures from an airport")
    departures_parser.add_argument("airport", help="ICAO airport code (e.g. EGLL, KJFK)")
    departures_parser.add_argument("--hours", type=int, default=24, help="Lookback hours (default: 24, max: 168)")

    args = parser.parse_args()

    if args.command == "states":
        result = get_states(icao24=args.icao24, bbox=args.bbox)
    elif args.command == "track":
        result = get_track(args.icao24)
    elif args.command == "arrivals":
        result = get_flights(args.airport, "arrivals", hours=args.hours)
    elif args.command == "departures":
        result = get_flights(args.airport, "departures", hours=args.hours)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

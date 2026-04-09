# /// script
# requires-python = ">=3.11"
# dependencies = ["pysolar>=0.11"]
# ///
"""Solar position calculator for shadow-based geolocation in OSINT.

Calculate sun altitude and azimuth for a given location and time,
or estimate possible locations from shadow observations.

Usage:
    uv run sun_position.py calculate --lat 51.5 --lon -0.1 --date 2024-06-15 --time 14:30
    uv run sun_position.py shadow-length --lat 51.5 --lon -0.1 --date 2024-06-15 --time 14:30 --object-height 1.8
    uv run sun_position.py day-arc --lat 51.5 --lon -0.1 --date 2024-06-15
"""

import argparse
import json
import logging
import math
import sys
from datetime import datetime, timedelta, timezone

from pysolar.solar import get_altitude, get_azimuth

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)


def calculate_position(lat: float, lon: float, date_str: str, time_str: str, utc_offset: int = 0) -> dict:
    """Calculate sun position for a given location and time."""
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    dt = dt.replace(tzinfo=timezone(timedelta(hours=utc_offset)))

    altitude = get_altitude(lat, lon, dt)
    azimuth = get_azimuth(lat, lon, dt)

    # Normalize azimuth to 0-360
    azimuth = azimuth % 360

    # Cardinal direction from azimuth
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = round(azimuth / 22.5) % 16
    cardinal = directions[idx]

    result = {
        "latitude": lat,
        "longitude": lon,
        "datetime": dt.isoformat(),
        "utc_offset": utc_offset,
        "sun_altitude_deg": round(altitude, 2),
        "sun_azimuth_deg": round(azimuth, 2),
        "sun_direction": cardinal,
        "is_daylight": altitude > 0,
    }

    if altitude > 0:
        # Shadow direction is opposite to sun azimuth
        shadow_azimuth = (azimuth + 180) % 360
        shadow_idx = round(shadow_azimuth / 22.5) % 16
        result["shadow_direction"] = directions[shadow_idx]
        result["shadow_azimuth_deg"] = round(shadow_azimuth, 2)

    return result


def calculate_shadow_length(
    lat: float, lon: float, date_str: str, time_str: str, object_height: float, utc_offset: int = 0
) -> dict:
    """Calculate shadow length for an object of known height."""
    pos = calculate_position(lat, lon, date_str, time_str, utc_offset)

    altitude_rad = math.radians(pos["sun_altitude_deg"])
    if pos["sun_altitude_deg"] <= 0:
        return {**pos, "object_height_m": object_height, "shadow_length_m": None, "note": "Sun below horizon"}

    shadow_length = object_height / math.tan(altitude_rad)
    shadow_ratio = shadow_length / object_height

    return {
        **pos,
        "object_height_m": object_height,
        "shadow_length_m": round(shadow_length, 2),
        "shadow_to_height_ratio": round(shadow_ratio, 2),
        "note": f"Shadow is {shadow_ratio:.1f}x the object height",
    }


def calculate_day_arc(lat: float, lon: float, date_str: str, utc_offset: int = 0) -> dict:
    """Calculate sun positions throughout the day (hourly)."""
    positions = []
    sunrise = None
    sunset = None
    solar_noon = None
    max_altitude = -90

    for hour in range(24):
        for minute in [0, 30]:
            time_str = f"{hour:02d}:{minute:02d}"
            pos = calculate_position(lat, lon, date_str, time_str, utc_offset)
            entry = {
                "time": time_str,
                "altitude": pos["sun_altitude_deg"],
                "azimuth": pos["sun_azimuth_deg"],
            }
            positions.append(entry)

            if pos["sun_altitude_deg"] > max_altitude:
                max_altitude = pos["sun_altitude_deg"]
                solar_noon = time_str

            if pos["sun_altitude_deg"] > 0 and sunrise is None:
                sunrise = time_str
            if sunrise and pos["sun_altitude_deg"] <= 0 and sunset is None and hour > 12:
                sunset = time_str

    return {
        "latitude": lat,
        "longitude": lon,
        "date": date_str,
        "utc_offset": utc_offset,
        "sunrise_approx": sunrise,
        "sunset_approx": sunset,
        "solar_noon_approx": solar_noon,
        "max_altitude_deg": round(max_altitude, 2),
        "positions": positions,
    }


def main():
    parser = argparse.ArgumentParser(description="Solar position calculator for OSINT geolocation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser("calculate", help="Calculate sun position")
    calc_parser.add_argument("--lat", type=float, required=True, help="Latitude")
    calc_parser.add_argument("--lon", type=float, required=True, help="Longitude")
    calc_parser.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
    calc_parser.add_argument("--time", required=True, help="Time (HH:MM)")
    calc_parser.add_argument("--utc-offset", type=int, default=0, help="UTC offset in hours")

    shadow_parser = subparsers.add_parser("shadow-length", help="Calculate shadow length")
    shadow_parser.add_argument("--lat", type=float, required=True, help="Latitude")
    shadow_parser.add_argument("--lon", type=float, required=True, help="Longitude")
    shadow_parser.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
    shadow_parser.add_argument("--time", required=True, help="Time (HH:MM)")
    shadow_parser.add_argument("--object-height", type=float, required=True, help="Object height in meters")
    shadow_parser.add_argument("--utc-offset", type=int, default=0, help="UTC offset in hours")

    arc_parser = subparsers.add_parser("day-arc", help="Sun positions throughout the day")
    arc_parser.add_argument("--lat", type=float, required=True, help="Latitude")
    arc_parser.add_argument("--lon", type=float, required=True, help="Longitude")
    arc_parser.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
    arc_parser.add_argument("--utc-offset", type=int, default=0, help="UTC offset in hours")

    args = parser.parse_args()

    if args.command == "calculate":
        result = calculate_position(args.lat, args.lon, args.date, args.time, args.utc_offset)
    elif args.command == "shadow-length":
        result = calculate_shadow_length(args.lat, args.lon, args.date, args.time, args.object_height, args.utc_offset)
    elif args.command == "day-arc":
        result = calculate_day_arc(args.lat, args.lon, args.date, args.utc_offset)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

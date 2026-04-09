# /// script
# requires-python = ">=3.11"
# dependencies = ["Pillow>=10.0", "exifread>=3.0"]
# ///
"""Image EXIF/metadata extraction for OSINT investigations.

Usage:
    uv run extract_exif.py extract photo.jpg
    uv run extract_exif.py gps photo.jpg
    uv run extract_exif.py camera photo.jpg
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import exifread

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)


def _dms_to_decimal(dms_values, ref: str) -> float:
    """Convert DMS (degrees, minutes, seconds) to decimal degrees."""
    d = float(dms_values[0])
    m = float(dms_values[1])
    s = float(dms_values[2])
    decimal = d + m / 60 + s / 3600
    if ref in ("S", "W"):
        decimal = -decimal
    return round(decimal, 6)


def extract_all(filepath: str) -> dict:
    """Extract all EXIF metadata from an image."""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    with open(path, "rb") as f:
        tags = exifread.process_file(f, details=True)

    if not tags:
        log.info("No EXIF data found in %s", filepath)
        return {"file": filepath, "has_exif": False, "tags": {}}

    result = {"file": filepath, "has_exif": True, "tags": {}}
    for key, value in sorted(tags.items()):
        if key.startswith("Thumbnail"):
            continue
        result["tags"][key] = str(value)

    log.info("Extracted %d EXIF tags from %s", len(result["tags"]), filepath)
    return result


def extract_gps(filepath: str) -> dict:
    """Extract GPS coordinates from an image."""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    with open(path, "rb") as f:
        tags = exifread.process_file(f, details=False)

    lat_tag = tags.get("GPS GPSLatitude")
    lat_ref = tags.get("GPS GPSLatitudeRef")
    lon_tag = tags.get("GPS GPSLongitude")
    lon_ref = tags.get("GPS GPSLongitudeRef")

    if not all([lat_tag, lat_ref, lon_tag, lon_ref]):
        log.info("No GPS data found in %s", filepath)
        return {"file": filepath, "has_gps": False}

    lat = _dms_to_decimal(lat_tag.values, str(lat_ref))
    lon = _dms_to_decimal(lon_tag.values, str(lon_ref))

    result = {
        "file": filepath,
        "has_gps": True,
        "latitude": lat,
        "longitude": lon,
        "google_maps_url": f"https://www.google.com/maps?q={lat},{lon}",
        "openstreetmap_url": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}",
    }

    alt_tag = tags.get("GPS GPSAltitude")
    if alt_tag:
        result["altitude_m"] = float(alt_tag.values[0])

    direction_tag = tags.get("GPS GPSImgDirection")
    if direction_tag:
        result["image_direction"] = float(direction_tag.values[0])

    timestamp_tag = tags.get("GPS GPSTimeStamp")
    datestamp_tag = tags.get("GPS GPSDateStamp")
    if timestamp_tag and datestamp_tag:
        result["gps_timestamp"] = f"{datestamp_tag} {timestamp_tag}"

    log.info("GPS: %f, %f", lat, lon)
    return result


def extract_camera(filepath: str) -> dict:
    """Extract camera information from an image."""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    with open(path, "rb") as f:
        tags = exifread.process_file(f, details=False)

    camera_fields = {
        "make": "Image Make",
        "model": "Image Model",
        "software": "Image Software",
        "datetime": "Image DateTime",
        "datetime_original": "EXIF DateTimeOriginal",
        "exposure_time": "EXIF ExposureTime",
        "f_number": "EXIF FNumber",
        "iso": "EXIF ISOSpeedRatings",
        "focal_length": "EXIF FocalLength",
        "focal_length_35mm": "EXIF FocalLengthIn35mmFilm",
        "flash": "EXIF Flash",
        "white_balance": "EXIF WhiteBalance",
        "lens_make": "EXIF LensMake",
        "lens_model": "EXIF LensModel",
        "image_width": "EXIF ExifImageWidth",
        "image_height": "EXIF ExifImageLength",
    }

    result = {"file": filepath, "camera": {}}
    for key, tag_name in camera_fields.items():
        tag = tags.get(tag_name)
        if tag:
            result["camera"][key] = str(tag)

    if not result["camera"]:
        log.info("No camera info found in %s", filepath)
        return {"file": filepath, "has_camera_info": False}

    result["has_camera_info"] = True
    log.info("Camera: %s %s", result["camera"].get("make", "?"), result["camera"].get("model", "?"))
    return result


def main():
    parser = argparse.ArgumentParser(description="Image EXIF extraction for OSINT")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ext_parser = subparsers.add_parser("extract", help="Extract all EXIF metadata")
    ext_parser.add_argument("file", help="Image file path")

    gps_parser = subparsers.add_parser("gps", help="Extract GPS coordinates")
    gps_parser.add_argument("file", help="Image file path")

    cam_parser = subparsers.add_parser("camera", help="Extract camera info")
    cam_parser.add_argument("file", help="Image file path")

    args = parser.parse_args()

    if args.command == "extract":
        result = extract_all(args.file)
    elif args.command == "gps":
        result = extract_gps(args.file)
    elif args.command == "camera":
        result = extract_camera(args.file)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

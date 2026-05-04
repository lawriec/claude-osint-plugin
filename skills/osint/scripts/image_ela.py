# /// script
# requires-python = ">=3.11"
# dependencies = ["Pillow>=10.0"]
# ///
"""Error Level Analysis (ELA) for detecting image manipulation in OSINT investigations.

ELA works by re-saving a JPEG at a known quality level and comparing the result
to the original. Manipulated areas show different error levels than the surrounding
image because edited regions have been through fewer compression cycles.

Usage:
    uv run image_ela.py analyze photo.jpg
    uv run image_ela.py analyze photo.jpg --quality 90 --scale 20
    uv run image_ela.py analyze photo.jpg --output result_ela.png
    uv run image_ela.py metadata photo.jpg
    uv run image_ela.py compare original.jpg modified.jpg
"""

import argparse
import io
import json
import logging
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)


def analyze(filepath: str, quality: int = 95, scale: int = 15, output: str | None = None) -> dict:
    """Perform Error Level Analysis on an image."""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    try:
        original = Image.open(path)
    except Exception as e:
        return {"error": f"Cannot open image: {e}"}

    # Convert to RGB if necessary (e.g. RGBA, palette, grayscale)
    if original.mode != "RGB":
        log.info("Converting %s image to RGB for ELA", original.mode)
        original = original.convert("RGB")

    # Re-save as JPEG at the specified quality into a memory buffer
    buffer = io.BytesIO()
    original.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    resaved = Image.open(buffer)

    # Compute pixel-by-pixel difference
    diff = ImageChops.difference(original, resaved)

    # Amplify the differences by the scale factor
    ela_image = diff.point(lambda px: min(px * scale, 255))

    # Determine output path
    out_path = Path(output) if output else path.parent / f"{path.stem}_ela.png"

    ela_image.save(out_path)
    log.info("ELA visualization saved to %s", out_path)

    # Compute statistics on the raw (unscaled) difference
    stat = ImageStat.Stat(diff)
    channel_names = ["R", "G", "B"]
    mean_per_channel = {ch: round(stat.mean[i], 2) for i, ch in enumerate(channel_names)}
    overall_mean = round(sum(stat.mean) / len(stat.mean), 2)
    overall_max = max(stat.extrema[i][1] for i in range(len(stat.extrema)))
    overall_stddev = round(sum(stat.stddev) / len(stat.stddev), 2)

    # Assessment based on mean error and standard deviation
    if overall_mean < 5:
        assessment = "Low error levels — image appears unmodified (or was saved at very high quality)"
    elif overall_mean <= 15:
        assessment = "Moderate error levels — typical for images saved multiple times or with minor edits"
    else:
        assessment = "High error levels — potential manipulation or heavy re-compression detected"

    # Flag uneven compression (high std_dev relative to mean suggests localized editing)
    if overall_mean > 2 and overall_stddev > overall_mean * 1.5:
        assessment += ". High variance detected — potential manipulation in some regions"

    result = {
        "input": str(path),
        "output": str(out_path),
        "quality": quality,
        "scale": scale,
        "image_size": list(original.size),
        "statistics": {
            "mean_error": overall_mean,
            "max_error": overall_max,
            "std_dev": overall_stddev,
            "mean_per_channel": mean_per_channel,
        },
        "assessment": assessment,
        "note": (
            "ELA highlights areas with different compression levels. "
            "Uniformly low error suggests unmodified; high-error patches may indicate editing."
        ),
    }

    log.info("Mean error: %.2f, Max: %d, StdDev: %.2f", overall_mean, overall_max, overall_stddev)
    return result


def metadata(filepath: str) -> dict:
    """Extract basic image properties without performing ELA."""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}

    try:
        img = Image.open(path)
    except Exception as e:
        return {"error": f"Cannot open image: {e}"}

    has_exif = bool(img.getexif()) if hasattr(img, "getexif") else False

    result = {
        "file": str(path),
        "format": img.format,
        "size": list(img.size),
        "mode": img.mode,
        "has_exif": has_exif,
    }

    # Include format-specific info
    info_keys = ["dpi", "jfif", "jfif_version", "progressive", "compression"]
    for key in info_keys:
        if key in img.info:
            value = img.info[key]
            # Convert tuples to lists for JSON serialization
            if isinstance(value, tuple):
                value = list(value)
            result[key] = value

    log.info("Image: %s %dx%d %s", img.format, img.size[0], img.size[1], img.mode)
    return result


def compare(filepath1: str, filepath2: str) -> dict:
    """Compare two images pixel-by-pixel and output difference statistics."""
    path1 = Path(filepath1)
    path2 = Path(filepath2)

    if not path1.exists():
        return {"error": f"File not found: {filepath1}"}
    if not path2.exists():
        return {"error": f"File not found: {filepath2}"}

    try:
        img1 = Image.open(path1)
        img2 = Image.open(path2)
    except Exception as e:
        return {"error": f"Cannot open image: {e}"}

    # Ensure same mode
    if img1.mode != "RGB":
        img1 = img1.convert("RGB")
    if img2.mode != "RGB":
        img2 = img2.convert("RGB")

    # Resize img2 to match img1 if dimensions differ
    if img1.size != img2.size:
        log.info("Images differ in size (%s vs %s), resizing second image to match", img1.size, img2.size)
        img2 = img2.resize(img1.size, Image.LANCZOS)

    diff = ImageChops.difference(img1, img2)
    stat = ImageStat.Stat(diff)

    overall_mean = round(sum(stat.mean) / len(stat.mean), 2)
    # Count pixels where any channel differs
    total_pixels = img1.size[0] * img1.size[1]
    diff_data = diff.getdata()
    differing_pixels = sum(1 for px in diff_data if any(ch > 0 for ch in px))
    difference_pct = round((differing_pixels / total_pixels) * 100, 2)

    identical = difference_pct == 0

    if identical:
        note = "Images are pixel-identical"
    elif difference_pct < 1:
        note = "Nearly identical — minor differences likely from re-compression or metadata changes"
    elif difference_pct < 10:
        note = "Small differences detected — possible minor edits or different compression settings"
    else:
        note = "Images differ significantly — possible manipulation or different source"

    result = {
        "image1": str(path1),
        "image2": str(path2),
        "identical": identical,
        "difference_percentage": difference_pct,
        "mean_difference": overall_mean,
        "note": note,
    }

    log.info("Difference: %.2f%% of pixels, mean diff: %.2f", difference_pct, overall_mean)
    return result


def main():
    parser = argparse.ArgumentParser(description="Error Level Analysis for OSINT image forensics")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze", help="Perform ELA on an image")
    analyze_parser.add_argument("file", help="Image file path")
    analyze_parser.add_argument("--quality", type=int, default=95, help="JPEG recompression quality (default: 95)")
    analyze_parser.add_argument("--scale", type=int, default=15, help="Error amplification factor (default: 15)")
    analyze_parser.add_argument("--output", help="Output path for ELA visualization (default: <name>_ela.png)")

    meta_parser = subparsers.add_parser("metadata", help="Extract basic image properties")
    meta_parser.add_argument("file", help="Image file path")

    compare_parser = subparsers.add_parser("compare", help="Compare two images pixel-by-pixel")
    compare_parser.add_argument("image1", help="First image path")
    compare_parser.add_argument("image2", help="Second image path")

    args = parser.parse_args()

    if args.command == "analyze":
        result = analyze(args.file, quality=args.quality, scale=args.scale, output=args.output)
    elif args.command == "metadata":
        result = metadata(args.file)
    elif args.command == "compare":
        result = compare(args.image1, args.image2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

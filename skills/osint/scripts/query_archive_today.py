# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""archive.today (archive.ph) snapshot search and retrieval for OSINT investigations.

Search for cached snapshots of web pages on archive.today. Useful for finding
historical versions of pages that may have been modified or deleted.

Usage:
    uv run query_archive_today.py search "https://example.com"
    uv run query_archive_today.py newest "https://example.com"
    uv run query_archive_today.py oldest "https://example.com"
"""

import argparse
import json
import logging
import re
import sys
from urllib.parse import quote, unquote

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

BASE_URL = "https://archive.ph"
TIMEOUT = 20
MAX_RETRIES = 1

# Common headers to avoid blocks
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _fetch_with_retry(url: str, follow_redirects: bool = True) -> httpx.Response | None:
    """Fetch a URL with one retry on transient failures."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = httpx.get(
                url,
                headers=HEADERS,
                timeout=TIMEOUT,
                follow_redirects=follow_redirects,
            )
            return resp
        except httpx.TimeoutException:
            if attempt < MAX_RETRIES:
                log.warning("Timeout fetching %s, retrying (%d/%d)...", url[:80], attempt + 1, MAX_RETRIES)
            else:
                log.error("Timeout fetching %s after %d attempts", url[:80], MAX_RETRIES + 1)
        except httpx.ConnectError as e:
            if attempt < MAX_RETRIES:
                log.warning("Connection error for %s, retrying: %s", url[:80], e)
            else:
                log.error("Connection failed for %s: %s", url[:80], e)
        except Exception as e:
            log.error("Request failed for %s: %s", url[:80], e)
            return None
    return None


def _parse_snapshot_links(html: str) -> list[dict]:
    """Extract snapshot entries from archive.today search results HTML."""
    snapshots = []

    # archive.today lists snapshots with links like /XXXXX/url and timestamps
    # Pattern: <div class="TEXT-BLOCK"> contains snapshot info
    # Links look like: href="https://archive.ph/XXXXX"
    snapshot_pattern = re.compile(
        r'<a[^>]*href="(https?://archive\.(?:ph|today|is|li|vn|fo|md)/([a-zA-Z0-9]+))"[^>]*>',
    )
    # Timestamps appear near snapshot links, format varies
    date_pattern = re.compile(
        r'(\d{1,2}\s+\w{3}\s+\d{4}\s+\d{1,2}:\d{2}:\d{2}\s*(?:UTC)?)',
    )

    # Find all snapshot links
    seen_ids = set()
    link_matches = list(snapshot_pattern.finditer(html))

    for match in link_matches:
        snapshot_url = match.group(1)
        snapshot_id = match.group(2)

        # Skip duplicate IDs and navigation links
        if snapshot_id in seen_ids or len(snapshot_id) < 4:
            continue
        seen_ids.add(snapshot_id)

        snapshot = {
            "snapshot_url": snapshot_url,
            "snapshot_id": snapshot_id,
            "timestamp": None,
        }

        # Try to find a nearby timestamp (search within surrounding context)
        start = max(0, match.start() - 500)
        end = min(len(html), match.end() + 500)
        context = html[start:end]
        date_match = date_pattern.search(context)
        if date_match:
            snapshot["timestamp"] = date_match.group(1).strip()

        snapshots.append(snapshot)

    return snapshots


def _extract_original_url(html: str) -> str | None:
    """Try to extract the original URL from a snapshot page."""
    # archive.today shows the original URL in an input field or header
    url_pattern = re.compile(r'<input[^>]*id="SHARE_LONGLINK"[^>]*value="([^"]*)"')
    match = url_pattern.search(html)
    if match:
        return unquote(match.group(1))

    # Fallback: look for the original URL in meta tags
    meta_pattern = re.compile(r'<meta[^>]*property="og:title"[^>]*content="([^"]*)"')
    match = meta_pattern.search(html)
    if match:
        return match.group(1)

    return None


def search_snapshots(url: str) -> dict:
    """Search for all archived snapshots of a URL."""
    search_url = f"{BASE_URL}/?url={quote(url, safe='')}"
    log.info("Searching archive.today for snapshots of: %s", url)

    resp = _fetch_with_retry(search_url)
    if resp is None:
        return {"url": url, "error": "Failed to connect to archive.today"}

    if resp.status_code != 200:
        log.error("archive.today returned %d", resp.status_code)
        return {"url": url, "error": f"HTTP {resp.status_code}"}

    html = resp.text
    snapshots = _parse_snapshot_links(html)

    # Check if we landed directly on a snapshot (single result)
    if not snapshots and "archive.ph/" in str(resp.url) and "/?" not in str(resp.url):
        final_url = str(resp.url)
        snapshot_id_match = re.search(r'archive\.(?:ph|today|is|li|vn|fo|md)/([a-zA-Z0-9]+)', final_url)
        if snapshot_id_match:
            snapshots = [{
                "snapshot_url": final_url,
                "snapshot_id": snapshot_id_match.group(1),
                "timestamp": None,
            }]

    log.info("Found %d snapshots for %s", len(snapshots), url)
    return {
        "url": url,
        "snapshot_count": len(snapshots),
        "snapshots": snapshots,
        "search_url": search_url,
    }


def get_newest(url: str) -> dict:
    """Get the most recent snapshot of a URL."""
    newest_url = f"{BASE_URL}/newest/{quote(url, safe=':/')}"
    log.info("Looking up newest snapshot for: %s", url)

    resp = _fetch_with_retry(newest_url, follow_redirects=True)
    if resp is None:
        return {"url": url, "error": "Failed to connect to archive.today"}

    final_url = str(resp.url)

    # If we got redirected to a snapshot page
    if resp.status_code == 200 and "/newest/" not in final_url:
        snapshot_id_match = re.search(r'archive\.(?:ph|today|is|li|vn|fo|md)/([a-zA-Z0-9]+)', final_url)
        original = _extract_original_url(resp.text)

        result = {
            "url": url,
            "found": True,
            "snapshot_url": final_url,
            "snapshot_id": snapshot_id_match.group(1) if snapshot_id_match else None,
            "original_url": original,
        }

        # Try to find timestamp on the page
        date_match = re.search(
            r'(\d{1,2}\s+\w{3}\s+\d{4}\s+\d{1,2}:\d{2}:\d{2}\s*(?:UTC)?)',
            resp.text,
        )
        if date_match:
            result["timestamp"] = date_match.group(1).strip()

        log.info("Newest snapshot found: %s", final_url)
        return result

    # No snapshot found (page shows "No results" or stays on /newest/)
    log.info("No snapshots found for %s", url)
    return {"url": url, "found": False, "note": "No snapshots found on archive.today"}


def get_oldest(url: str) -> dict:
    """Get the oldest snapshot of a URL."""
    oldest_url = f"{BASE_URL}/oldest/{quote(url, safe=':/')}"
    log.info("Looking up oldest snapshot for: %s", url)

    resp = _fetch_with_retry(oldest_url, follow_redirects=True)
    if resp is None:
        return {"url": url, "error": "Failed to connect to archive.today"}

    final_url = str(resp.url)

    # If we got redirected to a snapshot page
    if resp.status_code == 200 and "/oldest/" not in final_url:
        snapshot_id_match = re.search(r'archive\.(?:ph|today|is|li|vn|fo|md)/([a-zA-Z0-9]+)', final_url)
        original = _extract_original_url(resp.text)

        result = {
            "url": url,
            "found": True,
            "snapshot_url": final_url,
            "snapshot_id": snapshot_id_match.group(1) if snapshot_id_match else None,
            "original_url": original,
        }

        date_match = re.search(
            r'(\d{1,2}\s+\w{3}\s+\d{4}\s+\d{1,2}:\d{2}:\d{2}\s*(?:UTC)?)',
            resp.text,
        )
        if date_match:
            result["timestamp"] = date_match.group(1).strip()

        log.info("Oldest snapshot found: %s", final_url)
        return result

    log.info("No snapshots found for %s", url)
    return {"url": url, "found": False, "note": "No snapshots found on archive.today"}


def main():
    parser = argparse.ArgumentParser(
        description="archive.today snapshot search and retrieval for OSINT. "
        "Find cached versions of web pages that may have been modified or deleted.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search for all snapshots of a URL")
    search_parser.add_argument("url", help="URL to search for")

    newest_parser = subparsers.add_parser("newest", help="Get the most recent snapshot")
    newest_parser.add_argument("url", help="URL to look up")

    oldest_parser = subparsers.add_parser("oldest", help="Get the oldest snapshot")
    oldest_parser.add_argument("url", help="URL to look up")

    args = parser.parse_args()

    if args.command == "search":
        result = search_snapshots(args.url)
    elif args.command == "newest":
        result = get_newest(args.url)
    elif args.command == "oldest":
        result = get_oldest(args.url)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

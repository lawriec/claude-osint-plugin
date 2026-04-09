# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Username existence check across platforms for OSINT investigations.

Checks if a username exists on common platforms by probing profile URLs.
For comprehensive enumeration, use Sherlock or Maigret as external tools.

Usage:
    uv run check_username.py johndoe
    uv run check_username.py johndoe --platforms github,twitter,reddit
    uv run check_username.py johndoe --timeout 10
"""

import argparse
import asyncio
import json
import logging
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

# Platform definitions: (name, url_template, method, indicators)
# method: "status" = check HTTP status, "content" = check page content
PLATFORMS = {
    "github": {
        "url": "https://api.github.com/users/{username}",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://github.com/{username}",
    },
    "reddit": {
        "url": "https://www.reddit.com/user/{username}/about.json",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://www.reddit.com/user/{username}",
    },
    "twitter": {
        "url": "https://nitter.net/{username}",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://x.com/{username}",
    },
    "instagram": {
        "url": "https://www.instagram.com/{username}/",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://www.instagram.com/{username}/",
    },
    "tiktok": {
        "url": "https://www.tiktok.com/@{username}",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://www.tiktok.com/@{username}",
    },
    "gitlab": {
        "url": "https://gitlab.com/api/v4/users?username={username}",
        "method": "content",
        "exists_check": "len(data) > 0",
        "profile_url": "https://gitlab.com/{username}",
    },
    "medium": {
        "url": "https://medium.com/@{username}",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://medium.com/@{username}",
    },
    "dev_to": {
        "url": "https://dev.to/api/users/by_username?url={username}",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://dev.to/{username}",
    },
    "hackernews": {
        "url": "https://hacker-news.firebaseio.com/v0/user/{username}.json",
        "method": "content",
        "exists_check": "data is not None",
        "profile_url": "https://news.ycombinator.com/user?id={username}",
    },
    "keybase": {
        "url": "https://keybase.io/_/api/1.0/user/lookup.json?usernames={username}",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://keybase.io/{username}",
    },
    "mastodon_social": {
        "url": "https://mastodon.social/api/v1/accounts/lookup?acct={username}",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://mastodon.social/@{username}",
    },
    "pinterest": {
        "url": "https://www.pinterest.com/{username}/",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://www.pinterest.com/{username}/",
    },
    "steam": {
        "url": "https://steamcommunity.com/id/{username}",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://steamcommunity.com/id/{username}",
    },
    "twitch": {
        "url": "https://www.twitch.tv/{username}",
        "method": "status",
        "exists_status": [200],
        "profile_url": "https://www.twitch.tv/{username}",
    },
}


async def check_platform(client: httpx.AsyncClient, username: str, platform: str, config: dict) -> dict:
    """Check if username exists on a specific platform."""
    url = config["url"].format(username=username)
    profile_url = config["profile_url"].format(username=username)
    result = {
        "platform": platform,
        "profile_url": profile_url,
        "exists": None,
        "status_code": None,
    }

    try:
        resp = await client.get(url, follow_redirects=True)
        result["status_code"] = resp.status_code

        if config["method"] == "status":
            result["exists"] = resp.status_code in config["exists_status"]
        elif config["method"] == "content":
            try:
                data = resp.json()  # noqa: F841 — used by eval below
                result["exists"] = eval(config["exists_check"])  # noqa: S307
            except Exception:
                result["exists"] = False

    except httpx.TimeoutException:
        result["error"] = "timeout"
        log.warning("Timeout checking %s for %s", platform, username)
    except Exception as e:
        result["error"] = str(e)
        log.warning("Error checking %s for %s: %s", platform, username, e)

    status = "FOUND" if result["exists"] else "not found"
    log.info("  %s: %s", platform, status)
    return result


async def check_all(username: str, platforms: list[str] | None = None, timeout: int = 15) -> dict:
    """Check username across all platforms."""
    targets = {k: v for k, v in PLATFORMS.items() if platforms is None or k in platforms}
    log.info("Checking username '%s' across %d platforms...", username, len(targets))

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/json",
    }

    async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
        tasks = [check_platform(client, username, name, config) for name, config in targets.items()]
        results = await asyncio.gather(*tasks)

    found = [r for r in results if r.get("exists")]
    not_found = [r for r in results if r.get("exists") is False]
    errors = [r for r in results if r.get("error")]

    return {
        "username": username,
        "summary": {
            "found": len(found),
            "not_found": len(not_found),
            "errors": len(errors),
            "total_checked": len(results),
        },
        "found": found,
        "not_found": not_found,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description="Check username existence across platforms")
    parser.add_argument("username", help="Username to check")
    parser.add_argument("--platforms", help="Comma-separated list of platforms to check")
    parser.add_argument("--timeout", type=int, default=15, help="Request timeout in seconds")
    parser.add_argument("--list-platforms", action="store_true", help="List available platforms")
    args = parser.parse_args()

    if args.list_platforms:
        print(json.dumps({"platforms": sorted(PLATFORMS.keys())}, indent=2))
        return

    platforms = args.platforms.split(",") if args.platforms else None
    result = asyncio.run(check_all(args.username, platforms, args.timeout))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

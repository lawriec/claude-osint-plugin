# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Reddit thread discovery for OSINT communities.

Discover and select threads from OSINT-related subreddits for community analysis.
Uses Reddit's public JSON API (no authentication needed for basic access).

Usage:
    uv run discover_reddit_threads.py --subreddit osint --sort hot --limit 25
    uv run discover_reddit_threads.py --subreddit geoguessr --sort new --limit 10 --select 5
    uv run discover_reddit_threads.py --subreddit RBI --with-comments --select 3
"""

import argparse
import json
import logging
import random
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

OSINT_SUBREDDITS = ["OSINT", "geoguessr", "RBI", "traceanobject", "SOCMINT", "netsec", "privacy"]

HEADERS = {
    "User-Agent": "OSINT-Plugin/1.0 (research tool; +https://github.com/lawriec/claude-osint-plugin)",
}


def fetch_threads(subreddit: str, sort: str = "hot", limit: int = 25, time_filter: str = "week") -> list[dict]:
    """Fetch threads from a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json"
    params = {"limit": min(limit, 100), "raw_json": 1}
    if sort == "top":
        params["t"] = time_filter

    try:
        resp = httpx.get(url, params=params, headers=HEADERS, timeout=15, follow_redirects=True)
        resp.raise_for_status()
        data = resp.json()

        threads = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            if post.get("stickied"):
                continue

            threads.append({
                "title": post.get("title"),
                "url": f"https://www.reddit.com{post.get('permalink', '')}",
                "author": post.get("author"),
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "created_utc": post.get("created_utc"),
                "selftext": post.get("selftext", "")[:500],  # Truncate long posts
                "link_flair_text": post.get("link_flair_text"),
                "is_self": post.get("is_self", False),
                "external_url": post.get("url") if not post.get("is_self") else None,
            })

        log.info("Fetched %d threads from r/%s (%s)", len(threads), subreddit, sort)
        return threads

    except httpx.HTTPStatusError as e:
        log.error("Reddit API returned %d for r/%s", e.response.status_code, subreddit)
        return []
    except Exception as e:
        log.error("Failed to fetch r/%s: %s", subreddit, e)
        return []


def fetch_comments(permalink: str, limit: int = 50) -> list[dict]:
    """Fetch comments for a thread."""
    url = f"https://www.reddit.com{permalink}.json"
    params = {"limit": limit, "raw_json": 1, "sort": "best"}

    try:
        resp = httpx.get(url, params=params, headers=HEADERS, timeout=15, follow_redirects=True)
        resp.raise_for_status()
        data = resp.json()

        comments = []
        if len(data) > 1:
            for child in data[1].get("data", {}).get("children", []):
                comment = child.get("data", {})
                if child.get("kind") != "t1":
                    continue
                comments.append({
                    "author": comment.get("author"),
                    "body": comment.get("body", "")[:1000],
                    "score": comment.get("score", 0),
                })

        return comments

    except Exception as e:
        log.warning("Failed to fetch comments for %s: %s", permalink, e)
        return []


def main():
    parser = argparse.ArgumentParser(description="Reddit thread discovery for OSINT communities")
    parser.add_argument("--subreddit", default="OSINT", help="Subreddit to search (default: OSINT)")
    parser.add_argument("--sort", choices=["hot", "new", "top", "rising"], default="hot", help="Sort order")
    parser.add_argument("--limit", type=int, default=25, help="Number of threads to fetch")
    parser.add_argument("--select", type=int, help="Randomly select N threads from results")
    parser.add_argument("--time-filter", default="week", choices=["hour", "day", "week", "month", "year", "all"])
    parser.add_argument("--with-comments", action="store_true", help="Include top comments")
    parser.add_argument("--all-subs", action="store_true", help="Fetch from all OSINT subreddits")
    parser.add_argument("--output-dir", help="Write individual thread files to this directory")
    args = parser.parse_args()

    subreddits = OSINT_SUBREDDITS if args.all_subs else [args.subreddit]

    all_threads = []
    for sub in subreddits:
        threads = fetch_threads(sub, args.sort, args.limit, args.time_filter)
        for t in threads:
            t["subreddit"] = sub
        all_threads.extend(threads)

    if args.select and args.select < len(all_threads):
        all_threads = random.sample(all_threads, args.select)
        log.info("Randomly selected %d threads", args.select)

    if args.with_comments:
        for thread in all_threads:
            permalink = thread["url"].replace("https://www.reddit.com", "")
            thread["comments"] = fetch_comments(permalink)
            log.info("Fetched %d comments for: %s", len(thread["comments"]), thread["title"][:50])

    if args.output_dir:
        import os
        os.makedirs(args.output_dir, exist_ok=True)
        for i, thread in enumerate(all_threads):
            filename = f"{args.output_dir}/thread_{i:03d}.json"
            with open(filename, "w") as f:
                json.dump(thread, f, indent=2)
        log.info("Wrote %d thread files to %s", len(all_threads), args.output_dir)

    result = {
        "subreddits": subreddits,
        "sort": args.sort,
        "total_threads": len(all_threads),
        "threads": all_threads,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

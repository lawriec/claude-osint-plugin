# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Email header analysis for OSINT investigations.

Parses raw email headers to extract sender chain, originating IP,
authentication results, and timing analysis.

Usage:
    uv run analyze_email_headers.py headers.txt
    cat headers.txt | uv run analyze_email_headers.py -
"""

import argparse
import email
import json
import logging
import re
import sys
from datetime import datetime
from email.utils import parsedate_to_datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
RECEIVED_FROM_PATTERN = re.compile(r"from\s+(\S+)(?:\s+\(([^)]+)\))?", re.IGNORECASE)
RECEIVED_BY_PATTERN = re.compile(r"by\s+(\S+)", re.IGNORECASE)


def parse_received_header(header: str) -> dict:
    """Parse a single Received: header into structured data."""
    result = {"raw": header.strip()}

    from_match = RECEIVED_FROM_PATTERN.search(header)
    if from_match:
        result["from_server"] = from_match.group(1)
        if from_match.group(2):
            result["from_details"] = from_match.group(2)

    by_match = RECEIVED_BY_PATTERN.search(header)
    if by_match:
        result["by_server"] = by_match.group(1)

    ips = IP_PATTERN.findall(header)
    if ips:
        # Filter out common non-routable IPs
        public_ips = [ip for ip in ips if not ip.startswith(("10.", "127.", "192.168.", "0."))]
        if public_ips:
            result["public_ips"] = public_ips
        result["all_ips"] = ips

    # Try to extract timestamp
    # Look for date pattern at end of Received header (after semicolon)
    semicolon_idx = header.rfind(";")
    if semicolon_idx != -1:
        date_str = header[semicolon_idx + 1 :].strip()
        try:
            dt = parsedate_to_datetime(date_str)
            result["timestamp"] = dt.isoformat()
        except Exception:
            result["timestamp_raw"] = date_str

    return result


def analyze_headers(raw_headers: str) -> dict:
    """Analyze raw email headers."""
    msg = email.message_from_string(raw_headers)

    result = {
        "from": msg.get("From"),
        "to": msg.get("To"),
        "subject": msg.get("Subject"),
        "date": msg.get("Date"),
        "message_id": msg.get("Message-ID"),
        "reply_to": msg.get("Reply-To"),
        "return_path": msg.get("Return-Path"),
    }

    # Parse the hop chain (Received headers, bottom-to-top = chronological)
    received_headers = msg.get_all("Received", [])
    hops = []
    for header in reversed(received_headers):  # Reverse for chronological order
        hop = parse_received_header(header)
        hops.append(hop)

    result["hops"] = hops
    result["hop_count"] = len(hops)

    # Calculate delays between hops
    if len(hops) >= 2:
        delays = []
        for i in range(1, len(hops)):
            ts1 = hops[i - 1].get("timestamp")
            ts2 = hops[i].get("timestamp")
            if ts1 and ts2:
                try:
                    dt1 = datetime.fromisoformat(ts1)
                    dt2 = datetime.fromisoformat(ts2)
                    delay = (dt2 - dt1).total_seconds()
                    delays.append(
                        {
                            "from_hop": i - 1,
                            "to_hop": i,
                            "delay_seconds": delay,
                            "suspicious": delay > 300,  # > 5 min between hops is unusual
                        }
                    )
                except Exception:
                    pass
        result["hop_delays"] = delays

    # Try to find originating IP (first public IP in the chain)
    originating_ip = None
    for hop in hops:
        public_ips = hop.get("public_ips", [])
        if public_ips:
            originating_ip = public_ips[0]
            break
    result["originating_ip"] = originating_ip

    # Authentication results
    auth = {}
    spf = msg.get("Received-SPF")
    if spf:
        auth["spf"] = spf.split()[0] if spf else None

    auth_results = msg.get("Authentication-Results")
    if auth_results:
        auth["raw"] = auth_results
        if "dkim=pass" in auth_results.lower():
            auth["dkim"] = "pass"
        elif "dkim=fail" in auth_results.lower():
            auth["dkim"] = "fail"
        if "dmarc=pass" in auth_results.lower():
            auth["dmarc"] = "pass"
        elif "dmarc=fail" in auth_results.lower():
            auth["dmarc"] = "fail"
        if "spf=pass" in auth_results.lower():
            auth["spf"] = "pass"
        elif "spf=fail" in auth_results.lower():
            auth["spf"] = "fail"

    result["authentication"] = auth

    # X-headers (often contain useful info)
    x_headers = {}
    for key in msg:
        if key.lower().startswith("x-"):
            x_headers[key] = msg.get(key)
    if x_headers:
        result["x_headers"] = x_headers

    return result


def main():
    parser = argparse.ArgumentParser(description="Email header analysis for OSINT")
    parser.add_argument("file", help="File containing raw email headers (use '-' for stdin)")
    args = parser.parse_args()

    if args.file == "-":
        raw = sys.stdin.read()
    else:
        with open(args.file) as f:
            raw = f.read()

    result = analyze_headers(raw)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

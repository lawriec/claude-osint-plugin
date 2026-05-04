# Challenge: IP Camera Location Identification

## Domain
Geolocation (Infrastructure + Network Analysis)

## Difficulty
Hard

## Scenario
"A security researcher conducting an internet-wide scan found an exposed IP camera streaming live video at IP address 91.210.104.73. The camera appears to be unprotected (no authentication required). Before filing a responsible disclosure report, we need to determine:

1. Where is this camera physically located?
2. What organization operates it?
3. What type of camera is it (vendor, model if possible)?
4. What services and potential vulnerabilities are exposed on this IP?

Use only passive reconnaissance techniques -- do not attempt to access the camera stream directly. Determine as much as possible from IP metadata, network intelligence, and public device fingerprint databases."

## Expected Approach
1. **IP geolocation** -- Run `query_ipinfo.py geo 91.210.104.73`:
   - Determine the country, region, city, and approximate coordinates
   - Note the ISP name and whether the IP is flagged as hosting, proxy, or mobile
   - Record the timezone for correlation with other findings
2. **ASN and network ownership** -- Run `query_ipinfo.py asn 91.210.104.73`:
   - Identify the Autonomous System Number and organization name
   - Determine whether this is a commercial ISP, hosting provider, enterprise, or government network
   - The ASN organization often reveals who operates the network the camera is on
3. **Shodan InternetDB device fingerprinting** -- Run `query_shodan_internetdb.py 91.210.104.73`:
   - Retrieve open ports (common camera ports: 80, 443, 554/RTSP, 8080, 8554)
   - Extract CPE (Common Platform Enumeration) strings to identify camera vendor and model
   - Check for known vulnerabilities (CVEs) associated with the device
   - Review any hostnames associated with the IP
   - Tags may indicate whether the device is identified as an IoT device or webcam
4. **Reverse DNS lookup** -- Run `query_dns.py reverse 91.210.104.73`:
   - PTR records may reveal the hostname assigned by the ISP or organization
   - Hostnames often contain location codes, organization abbreviations, or device type identifiers
   - Example: `cam-lobby.building-a.example.org` would reveal both device type and location
5. **Forward DNS investigation** -- If reverse DNS reveals a domain:
   - Run `query_dns.py all <discovered-domain>` to map the full DNS infrastructure
   - Run `query_whois.py lookup <discovered-domain>` to check domain registration
   - Cross-reference the domain registrant with the ASN organization
6. **Web search for contextual intelligence** -- Use SearXNG (`mcp__searxng__searxng_search`) and Tavily (`mcp__tavily__tavily_search`):
   - Search for the IP address directly: `"91.210.104.73"` to find any public references
   - Search for the ASN organization name combined with "camera" or "surveillance"
   - Search for any security advisories or Shodan/Censys reports mentioning this IP
   - If a CPE was found, search for the specific camera model's known vulnerabilities and default configurations
7. **Threat intelligence cross-reference** -- Run `query_urlscan.py search ip:91.210.104.73`:
   - Check if the IP has appeared in any URLScan.io submissions
   - Review any associated URLs or page titles that may reveal the camera's web interface
   - Historical scans may show the camera's login page or configuration interface
8. **Synthesize location and attribution** -- Combine all evidence layers:
   - Primary: IP geolocation (city-level accuracy)
   - Supporting: ASN organization (who operates the network)
   - Supporting: Reverse DNS (location-encoded hostname)
   - Supporting: CPE strings (device vendor and model)
   - Supporting: Web search results (public mentions or advisories)
   - Produce a confidence-weighted location assessment

## Verification
- [ ] IP geolocation retrieved with country, city, and ISP
- [ ] ASN ownership identified and organization classified
- [ ] Shodan InternetDB queried for ports, CPEs, and vulnerabilities
- [ ] Reverse DNS checked for PTR records
- [ ] CPE strings analyzed to identify camera vendor (if available)
- [ ] At least one web search conducted for the IP or associated organization
- [ ] URLScan.io checked for historical submissions
- [ ] Forward DNS and WHOIS performed if reverse DNS revealed a domain
- [ ] Final assessment includes location, operator, device type, and confidence levels
- [ ] Responsible disclosure considerations noted

## Ground Truth

<details>
<summary>Click to reveal</summary>

**This challenge uses a real IP address, but findings will vary over time.** The IP 91.210.104.73 is in a European allocation block. The specific findings depend on current IP assignment, but the methodology should be consistent regardless of what the IP currently hosts.

**Expected methodology demonstration:**

1. **IP geolocation:** The ip-api.com service should return a country, city, and ISP. European IPs in the 91.x.x.x range are allocated by RIPE NCC. The agent should note that IP geolocation is typically accurate to city level but not street level -- it narrows the search area but cannot pinpoint the camera's exact building.

2. **ASN analysis:** The ASN organization reveals whether this is a major ISP (residential/commercial internet), a hosting provider (cloud-hosted camera or VPN), or an enterprise/government allocation (direct organizational attribution). This distinction is critical for attribution.

3. **Shodan InternetDB:** This is the most forensically valuable step for camera identification. Expected findings may include:
   - Open ports: HTTP (80/443), RTSP (554), and vendor-specific management ports
   - CPE strings like `cpe:/h:hikvision:*` or `cpe:/h:dahua:*` identify the camera vendor
   - Known CVEs may indicate unpatched firmware (relevant for responsible disclosure)
   - If no data is returned, the IP may not have been recently scanned by Shodan

4. **Reverse DNS:** PTR records are set by the IP's operator. They may contain:
   - Geographic codes (city abbreviations, country codes)
   - Device identifiers (cam, nvr, dvr)
   - Organization names or internal naming conventions
   - If no PTR record exists, this is still a finding (many IoT devices lack reverse DNS)

5. **Cross-referencing:** The strongest attribution comes from correlating multiple data sources. When IP geolocation, ASN organization, reverse DNS hostname, and web search results all point to the same location and entity, confidence is high. Contradictions between sources should be flagged.

6. **Responsible disclosure notes:** A thorough response should mention:
   - An exposed camera with no authentication is a privacy and security risk
   - The appropriate disclosure path depends on the operator (ISP abuse contact, organization's security team, or national CERT)
   - The ASN WHOIS record typically includes an abuse contact email

**Scoring:**
- **Score 5 if:** Agent runs all four primary tools (ipinfo, Shodan InternetDB, reverse DNS, ASN lookup), performs web search or URLScan cross-referencing, correctly interprets CPE strings for device identification, correlates multiple evidence sources into a confidence-weighted assessment, and notes responsible disclosure considerations
- **Score 4 if:** Agent runs at least three primary tools, identifies the device vendor or ASN organization, and produces a structured location assessment
- **Score 3 if:** Agent runs geolocation and Shodan lookups but does not perform reverse DNS or cross-reference findings across sources
- **Score 2 if:** Agent runs IP geolocation only and does not use Shodan InternetDB or other enrichment tools
- **Score 1 if:** Agent relies on web search alone without querying device fingerprint databases or performing network-level reconnaissance

</details>

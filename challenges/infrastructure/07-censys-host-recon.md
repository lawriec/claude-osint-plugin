# Challenge: Censys Host Reconnaissance

## Domain
Infrastructure (Host Profiling / Attack Surface Mapping)

## Difficulty
Medium

## Scenario
"I'm a penetration tester preparing for an external assessment of a client's infrastructure. They gave me three IP addresses as the starting point for their public-facing servers. I need a comprehensive host profile for each one that covers exposed services, software versions, geographic location, network ownership, and any known vulnerabilities. Use both Censys and Shodan to build overlapping views so we don't miss anything. Here are the IPs:

1. 8.8.8.8
2. 1.1.1.1
3. 104.16.132.229

For each IP, I need: (a) a merged service inventory combining both data sources, (b) location and ASN ownership, (c) reverse DNS, and (d) a risk assessment noting any discrepancies between the two sources."

## Expected Approach
1. **Censys host lookup for all three IPs** -- Run `query_censys.py host <ip>` for each:
   - `uv run query_censys.py host 8.8.8.8`
   - `uv run query_censys.py host 1.1.1.1`
   - `uv run query_censys.py host 104.16.132.229`
   - Record services (port, service name, transport protocol), location, ASN, operating system, and last scan date from Censys
2. **Shodan InternetDB lookup for the same IPs** -- Run `query_shodan_internetdb.py <ip>` for each:
   - `uv run query_shodan_internetdb.py 8.8.8.8`
   - `uv run query_shodan_internetdb.py 1.1.1.1`
   - `uv run query_shodan_internetdb.py 104.16.132.229`
   - Record open ports, hostnames, CPEs (Common Platform Enumeration), and known CVEs from Shodan
3. **IP geolocation and ASN enrichment** -- Run `query_ipinfo.py` for each:
   - `uv run query_ipinfo.py geo 8.8.8.8` and `uv run query_ipinfo.py asn 8.8.8.8`
   - Repeat for the other two IPs
   - Cross-reference location and ASN data with Censys results
4. **Reverse DNS resolution** -- Run `query_dns.py reverse <ip>` for each:
   - `uv run query_dns.py reverse 8.8.8.8` (expect dns.google)
   - `uv run query_dns.py reverse 1.1.1.1` (expect one.one.one.one)
   - `uv run query_dns.py reverse 104.16.132.229`
5. **Compare and merge findings** -- For each IP, produce a unified view:
   - List all ports found by Censys, all ports found by Shodan, and note any that appear in only one source
   - Merge CPE/version data from Shodan with service metadata from Censys
   - Flag any CVEs reported by Shodan InternetDB
   - Note location or ASN discrepancies between Censys and ipinfo.py
6. **Risk assessment** -- For each host, classify the risk level:
   - Identify services that should not be publicly exposed
   - Flag any CVEs with severity ratings
   - Note if the host belongs to a CDN, cloud provider, or is a dedicated server
   - Provide recommendations for the penetration test scope

## Verification
- [ ] All three IPs queried via Censys (`query_censys.py host`)
- [ ] All three IPs queried via Shodan InternetDB (`query_shodan_internetdb.py`)
- [ ] IP geolocation obtained via `query_ipinfo.py geo` for each
- [ ] ASN ownership obtained via `query_ipinfo.py asn` for each
- [ ] Reverse DNS checked via `query_dns.py reverse` for each
- [ ] Censys and Shodan results explicitly compared per-IP (merged service list)
- [ ] Discrepancies between sources noted (different ports, missing data, scan date differences)
- [ ] Each IP correctly identified by operator (Google, Cloudflare)
- [ ] Risk assessment provided with actionable recommendations

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Expected merged profiles:**

1. **8.8.8.8 -- Google Public DNS:**
   - Operator: Google LLC (AS15169)
   - Location: United States (Censys and ipinfo should agree)
   - Reverse DNS: dns.google
   - Censys services: Port 53 (DNS), Port 443 (HTTPS/DNS-over-HTTPS). Censys typically shows detailed TLS certificate information for port 443
   - Shodan InternetDB: Port 53 and port 443. May include CPE entries for Google DNS. Usually no CVEs listed
   - Merged view: Both sources should agree on ports 53 and 443. Censys provides richer service metadata; Shodan provides CPE identifiers
   - Risk: This is a public DNS resolver, not a typical pentest target. If the client listed this IP, clarify scope

2. **1.1.1.1 -- Cloudflare Public DNS:**
   - Operator: Cloudflare, Inc. (AS13335)
   - Location: Varies due to anycast (United States or Australia commonly reported)
   - Reverse DNS: one.one.one.one
   - Censys services: Port 53 (DNS), Port 80 (HTTP), Port 443 (HTTPS), potentially Port 853 (DNS-over-TLS)
   - Shodan InternetDB: Similar port list, may also show port 8443 or 8080. CPEs for Cloudflare services
   - Merged view: Cloudflare shows more services than Google DNS. Location may differ between sources due to anycast routing
   - Risk: Anycast infrastructure with multiple services. Note that location discrepancies are expected for anycast IPs

3. **104.16.132.229 -- Cloudflare CDN:**
   - Operator: Cloudflare, Inc. (AS13335)
   - Location: United States
   - Reverse DNS: May not have a PTR record, or may show a generic Cloudflare hostname
   - Censys services: Port 80 (HTTP), Port 443 (HTTPS) with Cloudflare TLS certificates
   - Shodan InternetDB: Ports 80 and 443. Hostnames field may list domains proxied through this IP
   - Merged view: Both sources agree on standard web ports. The key intelligence is in Shodan's hostname list, which reveals which domains use this CDN IP
   - Risk: CDN-fronted IP. Direct attacks would hit Cloudflare infrastructure, not the origin server. Recommend testing origin servers instead

**Key methodology points:**
- Censys provides deeper service fingerprinting (TLS certs, banners, OS detection)
- Shodan InternetDB provides CVE associations and CPE identifiers
- Location discrepancies for anycast IPs are expected and should be noted, not treated as errors
- Scan timestamp differences mean the two sources may report different states

**Scoring:**
- **Score 5 if:** Agent queries all three IPs through both Censys AND Shodan, cross-references with ipinfo and DNS, produces a merged per-IP service inventory explicitly comparing the two sources, notes discrepancies (especially anycast location differences), and provides a risk-aware pentest scope assessment
- **Score 4 if:** Agent uses both Censys and Shodan for all IPs and produces merged results, but does not deeply analyze discrepancies or the pentest implications
- **Score 3 if:** Agent queries both sources but treats them independently without merging or comparing, or misses one IP
- **Score 2 if:** Agent only uses one of the two primary sources (Censys or Shodan) or provides raw data without synthesis
- **Score 1 if:** Agent does not use `query_censys.py` or does not systematically investigate all three IPs

</details>

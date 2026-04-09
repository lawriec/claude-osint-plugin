# Challenge: IP Address Attribution

## Domain
Infrastructure (IP Analysis)

## Difficulty
Easy

## Scenario
"I'm a web server admin and our rate limiter flagged these five IP addresses over the past 24 hours. Each one sent over 1,000 requests in under a minute. Can you look into each one — tell me where they're located, who operates them, and whether they look like bots, proxies, or legitimate users? Here are the IPs:

1. 8.8.8.8
2. 1.1.1.1
3. 104.16.132.229
4. 185.220.101.1
5. 203.0.113.50

I need to decide which ones to permanently block and which might be false positives."

## Expected Approach
1. **Geolocate all five IPs** -- Run `query_ipinfo.py geo <ip>` for each address:
   - `query_ipinfo.py geo 8.8.8.8`
   - `query_ipinfo.py geo 1.1.1.1`
   - `query_ipinfo.py geo 104.16.132.229`
   - `query_ipinfo.py geo 185.220.101.1`
   - `query_ipinfo.py geo 203.0.113.50`
   - Note country, city, ISP, and the `hosting`, `proxy`, and `mobile` flags for each
2. **ASN and network ownership** -- Run `query_ipinfo.py asn <ip>` for each address:
   - `query_ipinfo.py asn 8.8.8.8`
   - `query_ipinfo.py asn 1.1.1.1`
   - `query_ipinfo.py asn 104.16.132.229`
   - `query_ipinfo.py asn 185.220.101.1`
   - `query_ipinfo.py asn 203.0.113.50`
   - Identify the AS name and organization to classify each as infrastructure/hosting/residential
3. **Shodan InternetDB enrichment** -- Run `query_shodan_internetdb.py <ip>` for each address:
   - `query_shodan_internetdb.py 8.8.8.8`
   - `query_shodan_internetdb.py 1.1.1.1`
   - `query_shodan_internetdb.py 104.16.132.229`
   - `query_shodan_internetdb.py 185.220.101.1`
   - `query_shodan_internetdb.py 203.0.113.50`
   - Check open ports, hostnames, known vulnerabilities, and CPEs
4. **Reverse DNS** -- Run `query_dns.py reverse <ip>` for each to check PTR records:
   - `query_dns.py reverse 8.8.8.8` (should resolve to dns.google)
   - `query_dns.py reverse 1.1.1.1` (should resolve to one.one.one.one)
   - Others as applicable
5. **Classify and recommend** -- For each IP, determine:
   - Is it a well-known public service (DNS resolver, CDN)?
   - Is it a hosting/cloud provider (likely bot or scraper)?
   - Is it a known proxy/VPN/Tor exit node?
   - Is it a reserved/documentation range (not real traffic)?
   - Provide blocking recommendations based on classification

## Verification
- [ ] All five IPs were looked up with geolocation
- [ ] ASN/organization identified for each IP
- [ ] Shodan InternetDB checked for open ports and hostnames
- [ ] Each IP correctly classified (infrastructure, hosting, proxy, reserved)
- [ ] 203.0.113.50 identified as a documentation/reserved range (TEST-NET-3)
- [ ] 185.220.101.1 identified as a Tor exit node or privacy proxy
- [ ] Blocking recommendations provided with reasoning

## Ground Truth

<details>
<summary>Click to reveal</summary>

**IP-by-IP attribution:**

1. **8.8.8.8 -- Google Public DNS:**
   - Country: United States
   - Org: Google LLC (AS15169)
   - Reverse DNS: dns.google
   - Classification: Public DNS resolver (hosting/infrastructure)
   - Assessment: This is Google's public DNS service. If your rate limiter flagged it, this is almost certainly a false positive -- DNS resolvers do not make HTTP requests to web servers. Investigate whether your logging is capturing DNS queries rather than HTTP requests. Do NOT block.

2. **1.1.1.1 -- Cloudflare Public DNS:**
   - Country: United States (or Australia, depending on anycast node)
   - Org: Cloudflare, Inc. (AS13335)
   - Reverse DNS: one.one.one.one
   - Classification: Public DNS resolver (hosting/infrastructure)
   - Assessment: Same as 8.8.8.8 -- this is Cloudflare's DNS service. Likely a false positive in rate limiting logs. Do NOT block.

3. **104.16.132.229 -- Cloudflare CDN:**
   - Country: United States
   - Org: Cloudflare, Inc. (AS13335)
   - Classification: CDN/hosting infrastructure
   - Assessment: This is a Cloudflare CDN IP. Traffic from this IP could be a Cloudflare Worker, a proxied request, or a misconfigured upstream. Blocking this IP could affect legitimate Cloudflare-proxied traffic. Investigate further before blocking.

4. **185.220.101.1 -- Tor Exit Node:**
   - Country: Germany (or Netherlands)
   - Org: Tor exit relay operator (various AS names)
   - Classification: Known Tor exit node / anonymization proxy
   - Hosting flag: true; Proxy flag: likely true
   - Assessment: This is a well-known Tor exit node. Traffic is anonymized and untraceable to the actual user. High-volume automated requests through Tor are typically malicious (scraping, credential stuffing, vulnerability scanning). Recommend blocking or CAPTCHA challenge.

5. **203.0.113.50 -- TEST-NET-3 (Documentation Range):**
   - Reserved range: 203.0.113.0/24 (RFC 5737)
   - Classification: Reserved for documentation and examples; should never appear in real traffic
   - Assessment: This IP should not appear in production access logs. If it does, it indicates either spoofed source addresses, a misconfigured proxy/load balancer injecting example IPs, or a logging bug. Investigate your infrastructure rather than blocking.

**Scoring:**
- **Score 5 if:** Agent runs geo + ASN + Shodan for all five IPs, correctly classifies each, identifies TEST-NET-3 as reserved, flags the Tor exit node, recognizes DNS resolvers as false positives, and provides actionable blocking recommendations with reasoning
- **Score 4 if:** Agent correctly identifies 4 out of 5 IPs and provides reasonable recommendations
- **Score 3 if:** Agent geolocates and identifies ownership for most IPs but misses the reserved range or Tor classification
- **Score 2 if:** Agent runs lookups but provides only raw data without classification or recommendations
- **Score 1 if:** Agent doesn't systematically investigate all five IPs or misidentifies most of them

</details>

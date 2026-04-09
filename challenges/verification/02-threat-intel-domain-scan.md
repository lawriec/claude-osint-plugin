# Challenge: Threat Intelligence Domain Scan

## Domain
Verification (Threat Intelligence)

## Difficulty
Hard

## Scenario
"Our security operations center received an alert that an employee visited `example-malware-test.com` during working hours. Before escalating to the incident response team, we need a full threat assessment of this domain.

Since the exact domain may not exist or may be transient, demonstrate the complete threat assessment methodology. Use `example-malware-test.com` as the primary target for URLScan and WHOIS checks, and supplement with a known domain like `google.com` for infrastructure baseline comparisons. The goal is to document a comprehensive, repeatable threat assessment framework that covers every angle -- domain reputation, infrastructure analysis, certificate transparency, IP intelligence, and open port enumeration. Clearly document what indicators would differentiate a malicious domain from a legitimate one at each step."

## Expected Approach
1. **URLScan.io lookup** -- `query_urlscan.py search "domain:example-malware-test.com"`:
   - Check if the domain has been previously scanned (prior submissions indicate it has been flagged)
   - If results exist, retrieve a full scan report: `query_urlscan.py result <uuid>`
   - Check verdicts, page content, redirects, and screenshot
   - Red flag: no prior scans may indicate a very new domain; many scans may indicate known malicious activity
2. **WHOIS investigation** -- `query_whois.py lookup example-malware-test.com`:
   - Check domain age (malicious domains are typically < 30 days old)
   - Check registrar (budget registrars like Namecheap, Porkbun common for abuse)
   - Check WHOIS privacy (almost always enabled for malicious domains)
   - Check expiration (1-year registration = minimum investment)
   - Compare against baseline: `query_whois.py lookup google.com` (registered 1997, MarkMonitor registrar, long expiration)
3. **DNS enumeration** -- `query_dns.py all example-malware-test.com`:
   - Check A/AAAA records for IP resolution
   - Check MX records (malicious sites rarely have mail infrastructure)
   - Check TXT records for SPF/DKIM/DMARC (usually absent on throwaway domains)
   - Check NS records (free/shared nameservers = red flag)
   - Check CAA records (legitimate sites often specify authorized CAs)
   - Compare against baseline: `query_dns.py all google.com` (full enterprise DNS profile)
4. **IP geolocation and reputation** -- For any resolved IP:
   - `query_ipinfo.py geo <resolved_ip>` -- Check hosting location, whether it is a known hosting provider
   - `query_ipinfo.py asn <resolved_ip>` -- Check ASN, ISP, and whether flagged as proxy/hosting
   - Red flags: hosting provider in unusual jurisdiction, `hosting: true` (VPS/cloud), `proxy: true`
5. **Shodan InternetDB** -- `query_shodan_internetdb.py <resolved_ip>`:
   - Check open ports (web-only with no other services = suspicious for a "company" site)
   - Check for known vulnerabilities
   - Check hostnames sharing the IP (many unrelated domains = shared hosting, common for malicious sites)
   - Check CPEs for server software identification
6. **Certificate transparency** -- `query_crtsh.py search example-malware-test.com`:
   - Check number of certificates issued (single Let's Encrypt cert = red flag)
   - Check issuance dates (recent, aligning with domain registration)
   - Check for wildcard certificates
   - Compare against baseline: `query_crtsh.py search google.com` (hundreds of certificates, commercial CAs)
7. **Threat indicator synthesis** -- Compile all findings into a red flag checklist:
   - Domain age < 30 days
   - Privacy-protected WHOIS with no identifiable registrant
   - Minimal DNS footprint (no MX, no SPF/DKIM/DMARC)
   - Single Let's Encrypt certificate, recently issued
   - Shared or budget hosting provider
   - IP flagged as hosting/proxy
   - No historical web presence in URLScan
   - Unusual open ports or known vulnerabilities on hosting IP
8. **Recommendation** -- Provide a threat assessment rating and recommended SOC actions:
   - If most red flags present: recommend blocking, escalate to IR team, preserve evidence
   - If few red flags: recommend monitoring, note as low-risk, document for audit trail
   - Include confidence level based on data availability

## Verification
- [ ] URLScan.io queried for the target domain
- [ ] WHOIS data retrieved and domain age assessed
- [ ] Full DNS enumeration performed
- [ ] IP geolocation and ASN lookup completed for resolved IPs
- [ ] Shodan InternetDB checked for open ports and vulnerabilities
- [ ] Certificate transparency logs searched
- [ ] Baseline comparison performed against a known legitimate domain
- [ ] Red flag checklist documented with clear malicious/legitimate indicators
- [ ] Threat assessment rating provided with recommended SOC actions
- [ ] Methodology documented as a repeatable framework

## Ground Truth

<details>
<summary>Click to reveal</summary>

**The comprehensive threat assessment framework should cover these seven pillars:**

1. **Domain reputation (WHOIS):**
   - Age is the strongest single indicator; most phishing/malware domains are < 30 days old
   - Budget registrars (Namecheap, Porkbun, NameSilo) are disproportionately used for abuse
   - Privacy WHOIS on a domain claiming to be a business is suspicious
   - 1-year registration signals minimal investment
   - Baseline: legitimate domains like `google.com` show 20+ year registration, premium registrar (MarkMonitor), long renewal periods

2. **DNS infrastructure:**
   - Legitimate businesses have MX records, SPF, DKIM, DMARC, and often CAA
   - Malicious domains typically resolve to a single A record with no mail or authentication records
   - Free/shared nameservers (e.g., default registrar NS) vs. enterprise DNS (Cloudflare Enterprise, AWS Route53 with custom config)
   - Baseline: `google.com` has comprehensive DNS with dozens of record types

3. **SSL/TLS certificates:**
   - Single Let's Encrypt cert issued within days of domain registration = high-risk indicator
   - Legitimate businesses use commercial CAs (DigiCert, Sectigo) or have extensive cert history
   - Wildcard certs on a new domain with no subdomains are suspicious
   - Baseline: `google.com` has hundreds of certificates across many CAs

4. **IP reputation and geolocation:**
   - `hosting: true` in ip-api.com indicates VPS/cloud (common for malicious infrastructure)
   - `proxy: true` indicates anonymization
   - Hosting in jurisdictions with weak abuse response is a red flag
   - Shared hosting with many unrelated domains suggests disposable infrastructure
   - Baseline: major companies use dedicated IP ranges with clear organizational attribution

5. **Open ports and services (Shodan):**
   - Web-only (80/443) with no other services suggests a single-purpose disposable site
   - Known vulnerabilities on the hosting IP indicate poorly maintained infrastructure
   - Many hostnames on the same IP confirm shared hosting
   - Baseline: enterprise infrastructure shows managed services with no known vulns

6. **URLScan.io intelligence:**
   - Prior scans with malicious verdicts are strong evidence
   - Page content analysis reveals phishing kits, redirects, or credential harvesting
   - Screenshot review can identify brand impersonation
   - No prior scans on a domain claiming to be established = inconsistency

7. **Cross-referencing and synthesis:**
   - Individual indicators have limited value; the combination creates confidence
   - A domain can have 1-2 red flags and still be legitimate (new startup, privacy-conscious)
   - 5+ red flags across multiple pillars = high confidence malicious

**Scoring:**
- **Score 5 if:** Agent executes all seven pillars of investigation using the correct tools, provides a baseline comparison against a legitimate domain, documents a structured red flag checklist with clear thresholds, delivers a threat assessment rating with confidence level, and presents the methodology as a repeatable SOC framework
- **Score 4 if:** Agent covers 5-6 pillars with correct tool usage and provides a threat assessment, but baseline comparison or framework documentation is incomplete
- **Score 3 if:** Agent covers 3-4 pillars and identifies key indicators, but analysis lacks structure or misses the synthesis step
- **Score 2 if:** Agent runs some tools but only provides raw data without meaningful threat interpretation or red flag analysis
- **Score 1 if:** Agent checks only 1-2 data sources or fails to connect findings into a threat assessment

</details>

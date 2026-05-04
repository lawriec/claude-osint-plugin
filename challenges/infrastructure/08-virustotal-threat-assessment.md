# Challenge: VirusTotal Threat Assessment

## Domain
Infrastructure (Threat Intelligence)

## Difficulty
Easy

## Scenario
"Our security team intercepted a phishing email targeting an executive. The email contained a link to `http://secure-login.example.com/verify` and encouraged the recipient to download a file. We extracted the following indicators from the email and attachment:

- Suspicious domain: `secure-login.example.com`
- The domain resolves to: `93.184.216.34`
- File hash (SHA-256): `275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f`

I need a threat assessment for each of these three indicators. Check their reputation, determine if they are known threats, and cross-reference with DNS and WHOIS data to understand the infrastructure behind this campaign. Note: if the VT_API_KEY is not configured, walk through the exact methodology and commands you would use, explaining what each result would tell us."

## Expected Approach
1. **Domain threat check via VirusTotal** -- Run `query_virustotal.py domain`:
   - `uv run query_virustotal.py domain secure-login.example.com`
   - Review: reputation score, analysis_stats (malicious/harmless/suspicious counts), categories assigned by security vendors, last DNS records from VT, and any tags
   - High malicious count indicates the domain is flagged by multiple AV vendors
2. **IP threat check via VirusTotal** -- Run `query_virustotal.py ip`:
   - `uv run query_virustotal.py ip 93.184.216.34`
   - Review: ASN and owner, country, reputation score, analysis_stats, and tags
   - Check whether the IP hosts other malicious domains (shared infrastructure)
3. **File hash check via VirusTotal** -- Run `query_virustotal.py hash`:
   - `uv run query_virustotal.py hash 275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f`
   - Review: detection ratio (malicious count vs total engines), file type, known names, threat classification, first/last submission dates, and times submitted
   - This particular hash is the EICAR test file -- a standard antivirus test signature
4. **DNS enrichment** -- Run `query_dns.py` to independently verify DNS records:
   - `uv run query_dns.py all secure-login.example.com`
   - Compare the resolved IP with what VirusTotal reports in last_dns_records
   - Check for MX records (does the domain also handle email?)
   - `uv run query_dns.py reverse 93.184.216.34` for reverse DNS
5. **WHOIS investigation** -- Run `query_whois.py` to check domain registration:
   - `uv run query_whois.py lookup secure-login.example.com`
   - Check registrar, creation date (very recent registration is suspicious), registrant details
   - Compare WHOIS data with VT's embedded WHOIS snippet
6. **Synthesize threat assessment** -- Produce an IOC (Indicator of Compromise) report:
   - For each indicator (domain, IP, hash), state whether it is malicious, suspicious, or clean
   - Note the file hash is the EICAR test file if identified
   - Provide confidence level based on number of engines flagging each indicator
   - Recommend response actions (block domain, block IP, quarantine file, notify affected users)

## Verification
- [ ] Domain checked via `query_virustotal.py domain`
- [ ] IP checked via `query_virustotal.py ip`
- [ ] File hash checked via `query_virustotal.py hash`
- [ ] DNS records independently verified via `query_dns.py all`
- [ ] WHOIS information retrieved via `query_whois.py lookup`
- [ ] VT analysis_stats interpreted (malicious/harmless/suspicious counts explained)
- [ ] File hash recognized as EICAR test file (or methodology described for identifying file type)
- [ ] IOC report produced with per-indicator verdict and confidence
- [ ] Response recommendations provided

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Expected findings per indicator:**

1. **Domain: secure-login.example.com**
   - This is a subdomain of `example.com`, which is an IANA reserved domain (RFC 2606)
   - VirusTotal will either show no results (subdomain not in database) or return the parent domain's data
   - `example.com` itself is well-known and categorized as safe/documentation by most vendors
   - DNS: `example.com` resolves to 93.184.216.34 (IANA's example IP); the subdomain may not resolve
   - WHOIS: Registered by IANA for documentation purposes, not a real hosting entity
   - Assessment: In a real scenario, a recently registered domain mimicking a legitimate service name like "secure-login" would be highly suspicious. The use of example.com here is for safe demonstration

2. **IP: 93.184.216.34**
   - This is IANA's example IP address, serving `example.com`
   - Operator: Edgecast/Verizon Digital Media (or similar CDN that hosts IANA examples)
   - ASN: Typically AS15133 (Edgecast) or AS20940 (Akamai)
   - Country: United States
   - VirusTotal reputation: Should be clean -- this IP serves well-known documentation content
   - In a real investigation, you would check if the IP hosts other domains (shared hosting analysis)

3. **File hash: 275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f**
   - This is the SHA-256 hash of the **EICAR test file** (standard antivirus test string)
   - The EICAR test file is detected by virtually all antivirus engines as a test signature
   - VirusTotal will show extremely high detection (60+ engines flagging it as malicious/test)
   - File type: Text file containing the EICAR test string
   - Threat classification: "EICAR-Test-File" or similar designation
   - First submission date: Very early (the EICAR test file has been in VT for many years)
   - Times submitted: Extremely high (millions of submissions)
   - Important: The EICAR file is NOT actually malicious -- it is a test file designed to trigger AV detection without causing harm. The agent should recognize this distinction

4. **Methodology when VT_API_KEY is not set:**
   - The agent should still run all VT commands (they will return a clear error about the missing key)
   - The agent should explain what each command checks and what the results would indicate
   - DNS and WHOIS scripts work without API keys and should still be executed
   - The agent should note that VT has a free tier (4 requests/min, 500/day) and provide the signup URL

**Scoring:**
- **Score 5 if:** Agent checks all three indicator types via VT (domain, IP, hash), cross-references with DNS and WHOIS, correctly identifies the EICAR test file hash, interprets VT analysis_stats with proper context, and produces an IOC report with per-indicator verdicts and response recommendations
- **Score 4 if:** Agent checks all three indicators via VT and produces an assessment, but does not identify the EICAR hash or does not cross-reference with DNS/WHOIS
- **Score 3 if:** Agent checks at least two of the three indicator types and provides reasonable interpretation, but misses one or does not synthesize findings
- **Score 2 if:** Agent checks only one indicator type or provides raw VT output without interpretation
- **Score 1 if:** Agent does not use `query_virustotal.py` or only describes the methodology theoretically without running any commands

</details>

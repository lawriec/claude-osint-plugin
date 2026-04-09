# Challenge: Phishing Infrastructure Analysis

## Domain
Infrastructure (Domain Analysis, Threat Intelligence)

## Difficulty
Medium

## Scenario
"Our security team received reports of a suspicious login page at `secure-paypa1-verify.com` (note the numeral '1' replacing the letter 'l'). Before we send a takedown notice, we need to document everything about this domain's infrastructure for our report. Assume this domain exists and investigate the following:

1. How old is this domain registration?
2. What does its DNS infrastructure look like?
3. Are there any SSL certificates associated with it?
4. What other domains share its infrastructure?
5. Does the IP hosting it have other suspicious indicators?

Document all findings with timestamps and assess the likelihood this is a phishing operation.

Note for testing: Since the exact domain may not exist, demonstrate the full investigation methodology using a known domain (e.g., `paypal.com`) and explain what red flags you would look for in the suspicious variant."

## Expected Approach
1. **Domain name analysis** -- Identify typosquatting indicators:
   - Homoglyph substitution: '1' for 'l' in paypal
   - Suspicious prefix: 'secure-' to appear legitimate
   - Suspicious suffix: '-verify' to create urgency
2. **WHOIS investigation** -- `query_whois.py lookup secure-paypa1-verify.com`:
   - Check registration date (phishing domains are usually < 30 days old)
   - Check registrar (budget registrars common for abuse)
   - Check privacy protection (almost always enabled for phishing)
   - Compare with legitimate `paypal.com` registration
3. **DNS enumeration** -- `query_dns.py all secure-paypa1-verify.com`:
   - Check for MX records (phishing sites rarely have mail infrastructure)
   - Check nameservers (shared/free hosting = red flag)
   - Check for SPF/DKIM/DMARC (usually absent on phishing domains)
4. **Certificate transparency** -- `query_crtsh.py search secure-paypa1-verify.com`:
   - Free Let's Encrypt cert = common for phishing (low effort)
   - Recent issuance date aligning with domain registration
   - Compare certificate count vs legitimate domain
5. **IP investigation** -- `query_shodan_internetdb.py` on resolved IP:
   - Check if shared hosting (many domains on same IP)
   - Check for open ports suggesting disposable VPS
   - Check geolocation of hosting (unusual locations = flag)
6. **Infrastructure comparison** -- Compare findings against `paypal.com`:
   - Registration age difference (decades vs days)
   - Infrastructure complexity (enterprise vs minimal)
   - Certificate history (extensive vs single cert)
7. **Google dorking** -- Search for the domain in threat intel sources:
   - `site:virustotal.com "secure-paypa1-verify.com"`
   - `site:urlscan.io "secure-paypa1-verify.com"`
8. **URLScan** -- `query_urlscan.py search secure-paypa1-verify.com` for prior scans

## Verification
Red flags checklist (a phishing domain would exhibit most/all):
- [ ] Domain registered within last 30 days
- [ ] Privacy-protected WHOIS
- [ ] Minimal DNS records (no MX, no SPF/DKIM/DMARC)
- [ ] Single Let's Encrypt certificate, recently issued
- [ ] Shared or budget hosting provider
- [ ] Typosquatting naming pattern (homoglyphs, added prefixes/suffixes)
- [ ] No historical web presence
- [ ] IP hosting other suspicious domains

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Phishing indicators the agent should identify:**

1. **Domain name red flags:**
   - Homoglyph: `paypa1` uses numeral '1' instead of letter 'l'
   - Brand impersonation: references PayPal
   - Trust-building prefix: `secure-`
   - Action-oriented suffix: `-verify` (creates urgency)

2. **Expected WHOIS findings (for a phishing domain):**
   - Registration: within days/weeks
   - Registrar: budget provider (Namecheap, Porkbun, etc.)
   - Registrant: WHOIS privacy enabled
   - Expiry: 1 year only (minimum investment)

3. **Expected DNS findings (for a phishing domain):**
   - A record pointing to shared hosting / VPS
   - No MX records (no email infrastructure needed)
   - No SPF/DKIM/DMARC (no email authentication)
   - Possibly using free DNS (Cloudflare free tier for proxying)

4. **Expected cert findings (for a phishing domain):**
   - Single Let's Encrypt certificate
   - Issued within days of domain registration
   - No certificate history

5. **Comparison with legitimate paypal.com:**
   - paypal.com registered 1999 (25+ years)
   - Extended Validation (EV) certificates from commercial CA
   - Extensive subdomain infrastructure
   - Full email authentication (SPF, DKIM, DMARC)
   - Enterprise-grade DNS with global CDN

**Scoring:**
- **Score 5 if:** Agent runs full methodology (WHOIS + DNS + crt.sh + Shodan + comparison), identifies all naming red flags, creates structured phishing assessment with confidence levels
- **Score 4 if:** Agent covers 4+ investigation steps and identifies most red flags
- **Score 3 if:** Agent identifies the typosquatting and runs some infrastructure checks but analysis is surface-level
- **Score 2 if:** Agent only identifies the domain name as suspicious without infrastructure investigation
- **Score 1 if:** Agent doesn't apply systematic methodology

</details>

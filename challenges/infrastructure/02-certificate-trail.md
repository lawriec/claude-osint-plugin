# Challenge: Certificate Transparency Trail

## Domain
Infrastructure (Certificate Transparency, DNS)

## Difficulty
Medium

## Scenario
"I found a suspicious domain `example-phishing-test.com`. Can you check if it has any SSL certificates, what subdomains are associated with it, and map out its infrastructure? I want to know if this looks like a legitimate operation or a fly-by-night setup."

Note: Use any currently active domain that you can verify. For testing purposes, use `letsencrypt.org` as a well-known domain where we can verify certificate transparency results.

## Expected Approach
1. **WHOIS** — Check registration age, registrar, registrant info
2. **DNS** — Full enumeration for infrastructure mapping
3. **crt.sh** — Certificate search for SSL history and subdomain discovery
4. **Shodan InternetDB** — Port/service scan on discovered IPs
5. **Analysis** — Compare registration age, certificate history, and infrastructure complexity to assess legitimacy

## Verification
For `letsencrypt.org`:
- Should have extensive certificate history (they are a CA)
- Multiple subdomains visible in crt.sh
- Well-established registration (2014+)
- Clear, professional infrastructure

## Ground Truth

<details>
<summary>Click to reveal</summary>

For `letsencrypt.org`:
- **Registration:** 2014, managed by Internet Security Research Group (ISRG)
- **Certificates:** Extensive history — they are literally a certificate authority
- **Subdomains:** Should include: community.letsencrypt.org, status.letsencrypt.org, and others
- **Assessment indicators of legitimacy:**
  - Old domain (10+ years)
  - Established registrant (ISRG)
  - Consistent infrastructure
  - Professional DNS setup with proper SPF/DKIM/DMARC
  - Multiple services (community forum, status page, etc.)

The agent should articulate clear indicators of legitimacy vs. suspicious domains:
- Registration age
- Registrant reputation
- Infrastructure complexity
- Certificate history length
- DNS hygiene (SPF, DKIM, DMARC)

</details>

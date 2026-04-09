# Challenge: Map the Infrastructure of a Public Domain

## Domain
Infrastructure (DNS, WHOIS, Certificate Transparency)

## Difficulty
Easy

## Scenario
A security researcher asks: "Can you map out the infrastructure of `cloudflare.com`? I want to know their mail servers, nameservers, subdomains visible in certificate transparency logs, and when the domain was registered."

## Expected Approach
1. **DNS enumeration** — `query_dns.py all cloudflare.com` to get A, AAAA, MX, NS, TXT, SOA records
2. **WHOIS lookup** — `query_whois.py lookup cloudflare.com` for registration data
3. **Certificate transparency** — `query_crtsh.py subdomains cloudflare.com` for subdomain discovery
4. **IP enrichment** — `query_shodan_internetdb.py` on discovered IPs

## Verification
- MX records should include mail servers (check against known Cloudflare mail infrastructure)
- NS records should be Cloudflare's own nameservers
- Domain creation date should be approximately 2009
- Certificate transparency should reveal numerous subdomains (dash.cloudflare.com, api.cloudflare.com, etc.)
- TXT records should include SPF record

## Ground Truth

<details>
<summary>Click to reveal</summary>

Key facts (may change over time — verify current state):
- **Registered:** ~2009 (check exact date via WHOIS)
- **Nameservers:** Cloudflare's own NS infrastructure
- **MX records:** Cloudflare uses their own email infrastructure
- **TXT records:** SPF record present, likely Google Workspace or custom
- **Subdomains from crt.sh:** Should include: dash.cloudflare.com, api.cloudflare.com, developers.cloudflare.com, blog.cloudflare.com, community.cloudflare.com, and many more
- The agent should identify at least 20+ unique subdomains from certificate transparency logs
- **Key insight:** Cloudflare practices what they preach — their own infrastructure is behind their CDN

</details>

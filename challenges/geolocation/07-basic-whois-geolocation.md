# Challenge: Domain Registration Geolocation

## Domain
Geolocation (WHOIS)

## Difficulty
Easy

## Scenario
"I found a website at `bbc.co.uk` and I want to know: Where is this organization based? Who registered the domain? When was it created? What country does their infrastructure suggest they operate from?"

## Expected Approach
1. **WHOIS lookup** — `query_whois.py lookup bbc.co.uk` to extract the registrant organization, registrant country, creation date, and registrar
2. **DNS enumeration** — `query_dns.py all bbc.co.uk` to examine nameservers and mail servers for geographic indicators (e.g., UK-based nameservers, mail infrastructure)
3. **IP geolocation** — `query_ipinfo.py geo <resolved_IP>` on the IP address resolved from the A record to confirm hosting location

## Verification
- Registrant organization should be identified as the BBC (British Broadcasting Corporation)
- Registrant country should be United Kingdom / GB
- Domain creation date should be in the 1990s
- DNS records should show professional, enterprise-grade infrastructure (multiple nameservers, MX records)
- IP geolocation should confirm UK-based hosting
- All three tools (WHOIS, DNS, IP geolocation) should be used

## Ground Truth

<details>
<summary>Click to reveal</summary>

Key facts (may change over time — verify current state):
- **Registrant:** British Broadcasting Corporation (BBC)
- **Country:** United Kingdom (GB)
- **Created:** 1990s — one of the earliest .co.uk domain registrations
- **DNS:** Extensive professional DNS infrastructure with multiple nameservers and mail servers, consistent with a large public broadcaster
- **IP hosting:** UK-based, as expected for a national broadcaster
- **Key insight:** Even a simple WHOIS + DNS + IP lookup on a well-known domain demonstrates the fundamentals of infrastructure-based geolocation — triangulating organizational identity and physical location from multiple technical data sources

### Scoring Rubric
| Score | Criteria |
|-------|----------|
| 5 | All three tools used (WHOIS, DNS, IP geolocation), correct identification of BBC as UK-based, creation date in the 1990s noted, infrastructure observations provided |
| 4 | Two of three tools used with correct identification and reasonable analysis |
| 3 | Only WHOIS used but correct identification of BBC and UK location |
| 2 | Partial results — organization or location identified but incomplete tool usage and analysis |
| 1 | No tool usage or incorrect identification |

</details>

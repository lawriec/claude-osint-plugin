# Challenge: Historical Website Analysis

## Domain
Verification (Digital Archaeology)

## Difficulty
Medium

## Scenario
"An investigator on our team needs to research a company that operated the website `theranos.com`. The company no longer exists and the website has been taken down. We need to piece together what the site looked like when it was active, who operated it, what they claimed to do, and when the site went dark.

Use the Wayback Machine and any other tools at your disposal to recover historical content, establish a timeline of the website's evolution, and determine the domain's current registration status. This will feed into a broader fraud investigation report."

## Expected Approach
1. **Wayback Machine search** -- Use Internet Archive MCP tools to find archived snapshots:
   - `ia_search` to locate archived captures of `theranos.com`
   - `ia_metadata` to retrieve metadata about the archived collection
   - Identify snapshot dates spanning the site's active period (approximately 2003-2018)
   - Examine snapshots from key periods: early years, peak hype (2014-2015), and decline (2016-2018)
2. **Historical content analysis** -- Review archived pages for:
   - Company description and mission statements
   - Product claims (miniaturized blood testing, "Edison" device)
   - Leadership team listed (Elizabeth Holmes as CEO, board members)
   - Changes in messaging over time as controversy grew
3. **WHOIS investigation** -- `query_whois.py lookup theranos.com`:
   - Check current registration status (active, expired, or parked)
   - Note registrar and registration dates
   - Check if WHOIS privacy is enabled
   - Compare creation date against known company founding (~2003)
4. **DNS enumeration** -- `query_dns.py all theranos.com`:
   - Check if domain still resolves (A records)
   - Check for MX records (active email = domain still in use)
   - Check nameservers to determine who controls the domain now
   - Absence of records would confirm the site is fully offline
5. **Web search for context** -- Search for background information:
   - Company history: founded 2003 by Elizabeth Holmes, valued at $9B at peak
   - Collapse timeline: WSJ investigation (2015), SEC charges (2018), criminal conviction (2022)
   - Correlate website changes with public events
6. **Timeline construction** -- Build a chronological record:
   - Domain registration date
   - Earliest Wayback Machine snapshots
   - Key content changes visible in archives
   - Date site went dark or was replaced with a holding page
   - Current domain status

## Verification
- [ ] Wayback Machine snapshots retrieved and reviewed for multiple time periods
- [ ] Company identified as Theranos (Elizabeth Holmes' blood-testing startup)
- [ ] Key claims documented (miniaturized blood testing technology)
- [ ] Timeline of website evolution established
- [ ] Current domain status determined via WHOIS and DNS
- [ ] Website disappearance correlated with company collapse events
- [ ] Structured report delivered with sources

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Company identity:**
- **Theranos, Inc.** -- health technology company founded by **Elizabeth Holmes** in 2003 (originally named "Real-Time Cures")
- Claimed to have developed revolutionary miniaturized blood testing using finger-prick samples
- "Edison" device was the flagship product, promising hundreds of tests from a single drop of blood
- Valued at approximately $9 billion at peak (2013-2014)
- Board included prominent figures: Henry Kissinger, George Shultz, Jim Mattis, Sam Nunn

**Key timeline:**
- **2003:** Company founded; domain likely registered around this time
- **2013-2014:** Peak hype period; website showcased Edison device and wellness centers
- **October 2015:** Wall Street Journal investigation by John Carreyrou exposed inaccuracies
- **2016-2017:** Regulatory actions (CMS, FDA); website content increasingly reduced
- **March 2018:** SEC charged Holmes with fraud; settled
- **September 2018:** Company dissolved
- **January 2022:** Holmes convicted on four counts of fraud
- Website went dark around the time of dissolution (2018)

**Wayback Machine:**
- The Internet Archive has extensive snapshots of `theranos.com` spanning 2004-2018
- Peak capture density during 2014-2016 (height of media attention)
- Snapshots show evolution from simple corporate site to polished health-tech marketing to increasingly sparse content

**Current domain status:**
- Domain may be parked, held by a registrar, or acquired by a third party
- DNS may or may not resolve depending on current holder
- WHOIS should show current registrant (unlikely to still be Theranos, Inc.)

**Scoring:**
- **Score 5 if:** Agent recovers historical content from multiple time periods via Wayback Machine, identifies Theranos and its claims, builds a clear timeline correlating website changes with public events, determines current domain status via WHOIS/DNS, and delivers a structured digital archaeology report
- **Score 4 if:** Agent uses Wayback Machine and identifies the company with key claims, but timeline is incomplete or current domain status is not checked
- **Score 3 if:** Agent identifies Theranos and retrieves some archived content, but relies primarily on web search rather than direct archive investigation
- **Score 2 if:** Agent identifies the company through web search but does not meaningfully use the Wayback Machine or infrastructure tools
- **Score 1 if:** Agent only performs a basic web search without using archival or infrastructure investigation tools

</details>

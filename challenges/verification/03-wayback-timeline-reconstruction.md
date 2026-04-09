# Challenge: Wayback Machine Timeline Reconstruction

## Domain
Verification (Digital Archaeology)

## Difficulty
Hard

## Scenario
"I'm researching `pets.com`, the infamous dot-com bubble company. The website has been defunct since 2000, but its entire rise and fall should be captured in the Wayback Machine. Can you reconstruct the website's evolution from launch through shutdown? I want to know: (1) how the site changed over time, (2) any key business pivots or content changes, (3) the approximate date the site went offline, (4) what the domain is used for today, and (5) a timeline of the company's public-facing narrative as told through its own website."

## Expected Approach
1. **Search the Internet Archive** — Use Internet Archive MCP (`ia_search`) to find available snapshots of pets.com:
   - Search for "pets.com" to locate the archived collection
   - Identify the date range of available snapshots
   - Note the total number of captures to understand archive depth
2. **Retrieve archive metadata** — Use `ia_metadata` to get detailed snapshot information:
   - Date range of first and last captures
   - Snapshot frequency over time (more captures during peak traffic)
   - Any associated media files (ads, images, press releases)
3. **Fetch key historical snapshots** — Use `mcp__fetch__fetch` to retrieve archived pages from different periods:
   - **1998-1999 (Launch era):** Early site design, initial product offerings, company messaging
   - **Early 2000 (IPO era, Feb 2000):** Peak confidence, expanded offerings, investor messaging
   - **Mid 2000 (Decline):** Signs of trouble -- reduced inventory, changed messaging, discount promotions
   - **Late 2000 (Shutdown, Nov 2000):** Final state of the site, shutdown notice, asset liquidation messaging
   - Compare homepage design, navigation structure, and promotional content across periods
4. **Identify the sock puppet mascot** — Note the presence and prominence of the iconic sock puppet dog mascot across snapshots:
   - Track when it first appeared and how it was used
   - This was one of the most recognizable dot-com era brand assets
5. **Check current domain status** — Determine what pets.com is today:
   - Run `query_whois.py lookup pets.com` for current registration details
   - Run `query_dns.py all pets.com` to check if the domain resolves and where it points
   - Visit the current site via Selenium or fetch to see its present state
6. **Research historical context** — Use Tavily (`mcp__tavily__tavily_search`) or SearXNG to fill in context:
   - IPO date and stock price trajectory
   - Super Bowl ad (January 2000) and its cultural impact
   - Shutdown announcement date and circumstances
   - Subsequent ownership of the domain and brand assets
7. **Build annotated timeline** — Compile all evidence into a chronological narrative:
   - Annotate each entry with the source (archived snapshot URL, news article, WHOIS record)
   - Distinguish between facts observed directly in archives and facts from secondary sources
   - Note any gaps in the archive record

## Verification
- [ ] Used Internet Archive MCP to search for and retrieve pets.com snapshots
- [ ] Analyzed snapshots from at least 3 distinct time periods (launch, peak, shutdown)
- [ ] Correctly identified the approximate launch date (~1998)
- [ ] Correctly identified the IPO timing (February 2000)
- [ ] Correctly identified the shutdown date (November 2000)
- [ ] Checked current domain status with WHOIS and DNS
- [ ] Researched the sock puppet mascot and its cultural significance
- [ ] Used web search for historical context beyond what the archive provides
- [ ] Produced a timeline with dated entries and source citations
- [ ] Distinguished between primary evidence (archived pages) and secondary sources (news articles)

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Key facts the agent should uncover:**

1. **Timeline of pets.com:**
   - **~1998:** Pets.com launched as an online pet supply retailer
   - **August 1998:** Amazon.com invested in Pets.com (approx. 54% stake)
   - **January 2000:** The sock puppet mascot appeared in a Super Bowl XXXIV ad, becoming a cultural phenomenon
   - **February 2000:** IPO on the NASDAQ, stock opened at $11/share
   - **November 7, 2000:** Announced shutdown and liquidation, stock was at $0.19
   - **The company operated for approximately 27 months from launch to shutdown**

2. **The sock puppet mascot:**
   - A hand puppet of a dog with a microphone, voiced by comedian Michael Ian Black
   - Appeared in Super Bowl ad that cost $1.2 million for 30 seconds
   - Became more famous than the company itself
   - After shutdown, the puppet character was sold to BarNone (a pet insurance company)

3. **Business model failure:**
   - Sold pet supplies online at a loss (shipping heavy bags of dog food cost more than the margins)
   - Spent $11.8 million on advertising in fiscal year 2000 while generating only $8.8 million in revenue
   - Classic dot-com bubble case study of unsustainable unit economics

4. **Domain history after shutdown:**
   - The domain has changed hands multiple times since 2000
   - PetSmart acquired some Pets.com assets
   - The domain's current use varies over time -- it has redirected to various pet-related sites

5. **Wayback Machine coverage:**
   - The Internet Archive has extensive snapshots of pets.com from 1999-2000
   - The site's evolution is well-documented, showing the shift from small startup to heavily-branded consumer site and back to shutdown notice

**Scoring:**
- **Score 5 if:** Agent retrieves and analyzes multiple archived snapshots across different time periods, correctly identifies all key dates (launch, IPO, shutdown), checks current domain status, produces a well-sourced timeline distinguishing primary and secondary evidence, and provides cultural/business context
- **Score 4 if:** Agent uses the archive effectively and gets most dates correct, produces a timeline, but may miss some context (e.g., the Super Bowl ad significance) or does not distinguish evidence types
- **Score 3 if:** Agent finds some archived snapshots and key facts but does not systematically analyze multiple time periods or produces a timeline with notable gaps
- **Score 2 if:** Agent mostly relies on web search for historical facts without meaningfully using the Wayback Machine as a primary source
- **Score 1 if:** Agent does not use the Internet Archive tools or produces only a superficial summary without evidence

</details>

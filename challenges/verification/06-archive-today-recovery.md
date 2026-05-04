# Challenge: Multi-Archive Content Recovery

## Domain
Verification (Digital Archaeology / Content Recovery)

## Difficulty
Medium

## Scenario
"A small investigative news website called `homelandsecuritynewswire.com` published important articles about critical infrastructure security over the years. The site's content has changed significantly over time and some earlier articles may no longer be accessible in their original form. I need to establish what the website looked like historically, recover snapshots of its earlier content, and build a timeline of how the site evolved. Use archive.today, the Wayback Machine, and Common Crawl to find preserved copies from different time periods. I want to compare what each archival source has, since they often capture different snapshots at different times. Also check the current domain registration to understand who operates it now."

## Expected Approach
1. **Search archive.today for snapshots** -- Run `query_archive_today.py`:
   - `uv run query_archive_today.py search "https://homelandsecuritynewswire.com"`
   - `uv run query_archive_today.py newest "https://homelandsecuritynewswire.com"`
   - `uv run query_archive_today.py oldest "https://homelandsecuritynewswire.com"`
   - Record: number of snapshots, date range (oldest to newest), snapshot IDs and timestamps
   - Note any specific archived pages that capture key content
2. **Search the Wayback Machine** -- Use Internet Archive MCP tools:
   - `ia_search` to find the archived collection for the domain
   - `ia_list` to enumerate available captures and their dates
   - `ia_metadata` for metadata about the archived collection
   - Compare the Wayback Machine's date range and capture frequency with archive.today's
3. **Search Common Crawl** -- Use Common Crawl MCP tools:
   - `cc_search` for the domain to find indexed pages
   - `cc_domain_summary` for an overview of what Common Crawl has captured
   - `cc_fetch` to retrieve specific captured pages if available
   - `cc_list_crawls` to understand which crawl datasets contain the domain
   - Common Crawl often captures pages that other archives miss
4. **Current domain status** -- Check who owns the domain now:
   - `uv run query_whois.py lookup homelandsecuritynewswire.com`
   - Check registration date, registrar, registrant organization, and expiration date
   - `uv run query_dns.py all homelandsecuritynewswire.com` to see where the domain currently points
5. **Compare archival coverage** -- Build a coverage comparison:
   - Create a timeline showing when each source (archive.today, Wayback Machine, Common Crawl) has snapshots
   - Identify time periods covered by only one source (unique captures)
   - Note any gaps where no source has coverage
   - Compare the content captured by each source for overlapping dates (do they show the same page state?)
6. **Retrieve and analyze key snapshots** -- For selected dates, fetch actual content:
   - Use `mcp__fetch__fetch` on archive.today snapshot URLs
   - Use `ia_download` for Wayback Machine captures
   - Use `cc_fetch` for Common Crawl results
   - Compare the site's design, content focus, and navigation across different periods
7. **Produce a timeline narrative** -- Document the site's evolution:
   - When was the domain first registered and first archived?
   - How has the site's content or focus changed over time?
   - Were there any periods of downtime or major redesigns?
   - What is the current state of the domain?

## Verification
- [ ] archive.today queried with `query_archive_today.py` (search, newest, and oldest subcommands)
- [ ] Wayback Machine queried via Internet Archive MCP tools (ia_search, ia_list, or ia_metadata)
- [ ] Common Crawl queried via Common Crawl MCP tools (cc_search or cc_domain_summary)
- [ ] All three archival sources used and their results compared
- [ ] Current WHOIS data retrieved with `query_whois.py lookup`
- [ ] Current DNS records checked with `query_dns.py all`
- [ ] Coverage timeline produced showing when each source has captures
- [ ] At least one snapshot actually fetched/read from each available source
- [ ] Differences between archival sources noted (coverage gaps, unique snapshots)
- [ ] Narrative timeline produced documenting the site's history

## Ground Truth

<details>
<summary>Click to reveal</summary>

**This challenge tests multi-source archival methodology.** The specific findings will depend on what each archive has captured at the time the challenge is run, but the agent should demonstrate:

1. **archive.today coverage:**
   - Run all three subcommands: search (lists all snapshots), newest (most recent capture), oldest (earliest capture)
   - archive.today snapshots are user-submitted, so coverage may be sparse or concentrated around newsworthy events
   - Each snapshot has a unique ID and timestamp
   - The agent should note how many snapshots exist and their date range

2. **Wayback Machine coverage:**
   - The Internet Archive crawls automatically and typically has more comprehensive coverage than archive.today
   - ia_search finds the collection, ia_list enumerates captures with dates
   - For a news website active since the 2010s, expect hundreds to thousands of captures
   - The Wayback Machine captures change over time as pages are updated between crawls

3. **Common Crawl coverage:**
   - Common Crawl runs periodic broad web crawls (monthly or quarterly)
   - Coverage is less targeted than the Wayback Machine but captures a broader snapshot of the web
   - cc_domain_summary shows how many pages and crawls include the domain
   - Common Crawl data is available as raw WARC files and processed indexes

4. **Key comparison points between sources:**
   - Date range: Wayback Machine usually has the longest history; archive.today depends on user submissions; Common Crawl started broad crawls around 2011-2012
   - Capture frequency: Wayback Machine captures popular sites frequently; archive.today is sporadic; Common Crawl is periodic
   - Content fidelity: archive.today saves complete rendered pages; Wayback Machine saves individual resources; Common Crawl saves raw HTTP responses
   - Unique captures: Each source likely has snapshots the others do not, making multi-source recovery valuable

5. **Domain investigation:**
   - WHOIS should reveal the registrant organization, registration date, and registrar
   - DNS records show the current hosting infrastructure
   - If the site has changed ownership or purpose, WHOIS history and archived content tell that story

6. **Why multi-source matters:**
   - If one archive is missing a critical time period, another may have it
   - Different archives capture different aspects (rendered page vs raw HTML vs HTTP response)
   - Comparing the same URL across archives at similar dates can reveal whether content was static or dynamic
   - Legal takedown requests may affect one archive but not others

**Scoring:**
- **Score 5 if:** Agent queries all three archival sources (archive.today via query_archive_today.py, Wayback Machine via IA MCP, Common Crawl via CC MCP), checks WHOIS and DNS, compares coverage across sources, fetches at least one actual snapshot, and produces a timeline with coverage analysis noting which sources have unique captures
- **Score 4 if:** Agent uses all three sources and produces a comparison, but does not fetch actual snapshot content or does not note coverage gaps between sources
- **Score 3 if:** Agent uses two of three archival sources and provides reasonable results, but does not fully compare or is missing one source entirely
- **Score 2 if:** Agent uses only one archival source (e.g., only Wayback Machine) or only runs commands without interpreting the results
- **Score 1 if:** Agent does not use `query_archive_today.py` or uses only web search without querying any archival tool

</details>

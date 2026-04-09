# Challenge: Historical Web Content Geolocation

## Domain
Geolocation (Web Archive Analysis)

## Difficulty
Medium

## Scenario
"An investigation requires finding where a now-defunct local business was located. The business operated the website `www.example-local-shop.com` (hypothetical). Since the domain is gone, the investigator needs to use web archives to find cached content that reveals the physical address.

For testing purposes, demonstrate the methodology using a real domain -- search Common Crawl for cached content from `craigslist.org` (which has clear geographic data in its content) to show how archived web pages can reveal location information. The goal is to establish a repeatable process for investigating defunct businesses through their archived web presence."

## Expected Approach
1. **Crawl index discovery** -- Use Common Crawl MCP (`mcp__common-crawl__cc_list_crawls`) to list available crawl indexes:
   - Identify which crawl indexes are available and their date ranges
   - Select recent and older indexes to compare content over time
   - Note the total number of crawls for coverage assessment
2. **Domain search** -- Use Common Crawl MCP (`mcp__common-crawl__cc_search`) to search for the domain:
   - Search for `craigslist.org` pages in the Common Crawl index
   - Note the URL patterns found (geographic subdomains like `sfbay.craigslist.org`)
   - Identify which pages were captured and when
3. **Domain summary** -- Use Common Crawl MCP (`mcp__common-crawl__cc_domain_summary`) to assess crawl coverage:
   - Check how many pages have been crawled for the domain
   - Understand the scope of archived content available
   - Identify the most frequently crawled subpages
4. **Content retrieval** -- Use Common Crawl MCP (`mcp__common-crawl__cc_fetch`) to retrieve cached page content:
   - Fetch actual HTML content from archived pages
   - Look for geographic indicators in the page content
5. **Geographic data extraction** -- Parse retrieved HTML for location indicators:
   - Physical addresses (street, city, state, ZIP)
   - Phone numbers (area codes reveal geographic region)
   - Google Maps embeds or coordinate references
   - Local business references, delivery zones, or service areas
   - Geographic subdomains or URL patterns (city names in URLs)
   - Time zone references or local event mentions
6. **Cross-referencing** -- Verify extracted location data:
   - Use web search to confirm addresses or phone area codes
   - Cross-reference business names found in cached content
   - Check if any extracted addresses correspond to known locations
7. **Methodology documentation** -- Document the process as a repeatable workflow:
   - Which Common Crawl tools to use and in what order
   - What geographic indicators to look for in cached HTML
   - How to handle cases where direct addresses are not found
   - Alternative archive sources if Common Crawl lacks coverage

## Verification
- [ ] Available crawl indexes listed and assessed
- [ ] Domain searched across Common Crawl indexes
- [ ] Domain summary retrieved showing crawl coverage
- [ ] At least one cached page fetched and content examined
- [ ] Geographic indicators extracted from cached content
- [ ] Phone area codes, addresses, or location references identified
- [ ] Findings cross-referenced against external sources
- [ ] Process documented as a repeatable methodology

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Methodology validation:**

Common Crawl contains petabytes of cached web data collected since 2008. For investigating defunct businesses, it serves as a massive web archive that can preserve content long after a website goes offline.

**Expected findings for craigslist.org:**

1. **Geographic structure:** Craigslist uses geographic subdomains (`sfbay.craigslist.org`, `newyork.craigslist.org`, etc.) making it an ideal demonstration domain -- the URL structure itself reveals location data.

2. **Cached content:** Retrieved pages should contain city/region names, local phone area codes in listings, street addresses in for-sale or housing posts, and geographic references throughout.

3. **Common Crawl tool usage:**
   - `cc_list_crawls` -- Returns available crawl indexes (monthly since 2013, quarterly before that)
   - `cc_search` -- Returns URL matches with timestamps and MIME types
   - `cc_domain_summary` -- Returns page count and subdomain distribution
   - `cc_fetch` -- Returns actual page HTML for content analysis

**For a real defunct business investigation, the agent should:**
- Search multiple crawl indexes (the business may only appear in older crawls)
- Fetch the homepage and any "about" or "contact" pages
- Extract addresses from page footers, contact sections, or embedded maps
- Look for phone numbers and use area code lookup to confirm region
- Check for Google Maps iframes with embedded coordinates
- Search for the business name in other cached pages (directories, reviews)

**Scoring:**
- **Score 5 if:** Agent uses all four Common Crawl MCP tools (`cc_list_crawls`, `cc_search`, `cc_domain_summary`, `cc_fetch`), extracts geographic data from cached content, cross-references findings, and documents the methodology as a repeatable process for defunct business investigations
- **Score 4 if:** Agent uses 3 of 4 Common Crawl tools, extracts some geographic data, and provides a reasonable methodology writeup
- **Score 3 if:** Agent uses `cc_search` and `cc_fetch` to find and retrieve content but does not fully extract geographic indicators or document the methodology
- **Score 2 if:** Agent searches Common Crawl but fails to fetch and analyze actual page content
- **Score 1 if:** Agent does not effectively use the Common Crawl MCP tools

</details>

# Challenge: Executive Credential Verification

## Domain
Corporate OSINT (People + Verification)

## Difficulty
Medium

## Scenario
"A startup called 'NovaBridge AI' is seeking Series A funding. The CEO, who goes by 'Marcus Chen-Alvarez,' claims the following on their pitch deck:

1. Former VP of Engineering at a Fortune 500 company
2. Holds two patents in natural language processing
3. Founded NovaBridge AI in 2022 and the company has been operating since
4. PhD in Computer Science from Stanford University
5. The company website is novabridge-ai.com

We're on the investment committee and need to verify as many of these claims as possible using open sources before the next meeting. What can you confirm, what raises questions, and what can't be verified?"

## Expected Approach
1. **Domain verification** -- Check the company's claimed web presence:
   - Run `query_whois.py lookup novabridge-ai.com` to check domain registration:
     - When was the domain registered? Does it predate or postdate the claimed 2022 founding?
     - Who is the registrant? Is it the company, the CEO, or a domain privacy service?
     - Which registrar was used?
   - Run `query_dns.py all novabridge-ai.com` to assess infrastructure:
     - Are MX records configured (does the company have email)?
     - What hosting provider is used (enterprise-grade or cheap shared hosting)?
     - Are SPF/DKIM/DMARC records present (email security maturity)?
2. **Certificate transparency** -- Run `query_crtsh.py subdomains novabridge-ai.com`:
   - Check for SSL certificates issued to the domain
   - Certificate history reveals when the site first went live with HTTPS
   - Subdomains (app, api, staging, docs) indicate actual product development vs a placeholder site
3. **Historical web presence** -- Use Common Crawl MCP (`mcp__common-crawl__cc_search`) and (`mcp__common-crawl__cc_domain_summary`):
   - Search for `novabridge-ai.com` in Common Crawl archives
   - Determine when the domain first appeared in web crawls
   - Check if the site content has changed over time (early-stage landing page vs functional product)
   - A company "operating since 2022" should have web presence dating back to at least late 2022 or early 2023
4. **CEO identity verification** -- Use Tavily (`mcp__tavily__tavily_search`) and SearXNG (`mcp__searxng__searxng_search`):
   - Search `"Marcus Chen-Alvarez"` to find public profiles and mentions
   - Search `"Marcus Chen-Alvarez" VP Engineering` to verify the Fortune 500 claim
   - Search `"Marcus Chen-Alvarez" Stanford PhD` to check academic credentials
   - Search `"Marcus Chen-Alvarez" patent NLP` to verify patent claims
   - Note: Absence of search results for someone claiming senior executive experience is itself a significant finding
5. **Cross-platform identity check** -- Run `check_username.py novabridge` and search for the CEO:
   - Check if the company has social media presence (LinkedIn, Twitter/X, GitHub)
   - Search for the CEO's professional profiles
   - LinkedIn is particularly important for verifying employment history claims
   - Look for the company on AngelList/Wellfound, Crunchbase, or PitchBook via web search
6. **Patent verification** -- Use Tavily to search patent databases:
   - Search `"Marcus Chen-Alvarez" site:patents.google.com` or `"Marcus Chen-Alvarez" patent`
   - Google Patents, USPTO, and Espacenet are freely searchable
   - Verify that any found patents match the claimed NLP domain
   - Check patent assignee (should match either the CEO's name or a previous employer)
7. **Academic credential check** -- Search for academic publications:
   - Search `"Marcus Chen-Alvarez" site:scholar.google.com` or via Tavily for academic papers
   - Stanford dissertations are publicly listed; search `"Marcus Chen-Alvarez" site:stanford.edu`
   - A PhD holder in CS with NLP patents should have published research
   - Absence of publications from someone claiming a Stanford CS PhD is a notable red flag
8. **Compile risk assessment** -- For each claim, assign a status:
   - **Confirmed:** Corroborated by multiple independent public sources
   - **Partially verified:** Some supporting evidence but incomplete
   - **Unverifiable:** No public sources found to confirm or deny
   - **Red flag:** Evidence contradicts the claim or absence of evidence is itself suspicious

## Verification
- [ ] Domain WHOIS retrieved and registration date compared to claimed founding
- [ ] DNS records analyzed for infrastructure maturity
- [ ] Certificate transparency checked for SSL history and subdomains
- [ ] Common Crawl queried for historical web presence
- [ ] Web search conducted for CEO's name with employment claims
- [ ] Patent databases searched for NLP patents under CEO's name
- [ ] Academic credentials investigated (Stanford, publications)
- [ ] Cross-platform presence checked for both company and CEO
- [ ] Each claim individually assessed with a verification status
- [ ] Overall risk assessment produced for the investment committee

## Ground Truth

<details>
<summary>Click to reveal</summary>

**This challenge uses a fictitious company and CEO.** The domain `novabridge-ai.com` and the name `Marcus Chen-Alvarez` are fabricated. The agent's primary findings should be negative -- and that negativity is the point.

**Expected findings:**

1. **Domain (novabridge-ai.com):** The WHOIS lookup will either show the domain is unregistered or return minimal information. If unregistered, this is a critical red flag -- a company "operating since 2022" should have its claimed domain registered. If registered, the registration date and registrant details are key evidence points.

2. **DNS/Certificates:** If the domain does not exist, DNS queries will fail and crt.sh will return no results. This absence of infrastructure contradicts the claim of an operating company.

3. **Common Crawl:** An unregistered or very new domain will have no Common Crawl history. A legitimate company operating since 2022 should have appeared in multiple crawl snapshots.

4. **CEO identity:** Searching for `"Marcus Chen-Alvarez"` should return no meaningful results. Key implications:
   - A former VP of Engineering at a Fortune 500 company would have a LinkedIn presence, press mentions, or conference talks
   - A PhD holder from Stanford with NLP patents would have published papers on Google Scholar
   - Complete absence from the public record for someone with these claimed credentials is a major red flag

5. **Patents:** No patents should be found under this name. A search of Google Patents or USPTO will confirm this.

6. **Academic record:** No Stanford dissertations or academic publications should be found. Stanford's dissertation database is publicly searchable.

**The correct conclusion:** The investment committee should be advised that none of the five claims could be verified through open sources. The combination of a non-existent or very new domain, no public record of the CEO, no discoverable patents, and no academic publications represents a pattern consistent with fabricated credentials. This does not prove fraud -- the candidate may have a different legal name, the company may use a different domain, or public records may simply be sparse -- but it warrants immediate follow-up questions before proceeding with investment.

**Scoring:**
- **Score 5 if:** Agent systematically checks all five claims using appropriate tools (WHOIS, DNS, crt.sh, Common Crawl, web search, patent search, academic search), clearly documents the negative findings for each claim, explains why absence of evidence is significant given the nature of the claims, and produces a structured risk assessment recommending follow-up questions
- **Score 4 if:** Agent checks at least four of five claims with appropriate tools, documents negative findings, and provides an overall risk assessment
- **Score 3 if:** Agent checks domain infrastructure and conducts web searches for the CEO but does not investigate patents, academic credentials, or historical web presence independently
- **Score 2 if:** Agent runs WHOIS and a web search but does not systematically address each claim or provide a risk assessment
- **Score 1 if:** Agent performs only web searches without using infrastructure investigation tools or systematically addressing individual claims

</details>

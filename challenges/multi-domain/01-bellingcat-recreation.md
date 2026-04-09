# Challenge: Bellingcat-Style Investigation (Simplified)

## Domain
Multi-domain (Infrastructure + People + Geolocation)

## Difficulty
Hard

## Scenario
"Bellingcat published research showing how they track military equipment movements using social media posts and satellite imagery. As an exercise, can you demonstrate a similar methodology by:

1. Finding publicly available information about the Bellingcat organization itself — who runs it, where they're based, what their digital infrastructure looks like
2. Showing how you would cross-reference multiple data sources to build an intelligence picture
3. Mapping the connections between people, organizations, and digital infrastructure

This is a methodology demonstration using publicly available information about a public organization."

## Expected Approach
1. **Person investigation** — Eliot Higgins (founder), key staff members from public pages
2. **Infrastructure** — bellingcat.com DNS, WHOIS, subdomains, hosting
3. **Social media** — @Bellingcat Twitter, YouTube, official social accounts
4. **Cross-referencing** — Link people → organization → domains → social accounts
5. **Knowledge graph** — Build entity graph with memory-graph MCP
6. **Reporting** — Structured report with confidence levels

## Verification
- All information used should be publicly available on Bellingcat's own website
- The methodology should demonstrate proper OSINT cycle (define → plan → collect → analyze → report)
- Knowledge graph should show entity relationships
- Report should include confidence levels for each finding

## Ground Truth

<details>
<summary>Click to reveal</summary>

This challenge tests the complete OSINT methodology, not a specific fact:

**Expected entities:**
- Person: Eliot Higgins (founder, executive director)
- Organization: Bellingcat (Netherlands-based, founded 2014)
- Domain: bellingcat.com
- Social: @Bellingcat (Twitter), YouTube channel, etc.
- Location: The Hague, Netherlands (publicly stated on their website)

**Expected relationships:**
- Eliot Higgins → founded → Bellingcat
- Bellingcat → operates → bellingcat.com
- Bellingcat → located_at → The Hague, Netherlands
- Bellingcat → has_social → @Bellingcat (Twitter)

**Methodology demonstration should include:**
1. Multiple data sources consulted (not just one search)
2. Evidence chain for each finding
3. Confidence levels appropriate to source quality
4. Negative results documented (what wasn't found)
5. Knowledge graph built with entities and relationships
6. Structured report following the template

- **Score 5 if:** Complete methodology demonstration with knowledge graph, multi-source corroboration, and structured report
- **Score 4 if:** Good methodology but missing one element (e.g., no knowledge graph)
- **Score 3 if:** Finds the right information but doesn't demonstrate OSINT methodology
- **Score 2 if:** Only does surface-level web search
- **Score 1 if:** Relies on prior knowledge without demonstrating investigation methodology

</details>

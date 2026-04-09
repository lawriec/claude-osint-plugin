# Investigation Setup Reference

How to scaffold and maintain an OSINT investigation workspace. Consistent structure ensures reproducibility, auditability, and prevents loss of findings.

## Directory Structure

```
investigation-name/
├── search-log.md       # Every query, platform, result, timestamp
├── leads.md            # Active leads: HIGH/MEDIUM/LOW priority
├── dead-ends.md        # What was tried and why it failed
├── evidence-chain.md   # Source -> finding -> conclusion with provenance
├── report.md           # Structured findings report
├── evidence/           # Downloaded files, screenshots, archived pages
│   ├── screenshots/
│   ├── downloads/
│   └── archives/
└── scripts/            # Any custom scripts used during investigation
```

## Creating the Workspace

```bash
mkdir -p investigation-name/{evidence/{screenshots,downloads,archives},scripts}
touch investigation-name/{search-log,leads,dead-ends,evidence-chain,report}.md
```

---

## File Templates

### search-log.md

The search log is the single most important file. Every query, every platform, every result must be logged. Without it, the investigation cannot be reproduced or audited.

```markdown
# Search Log

Investigation: [Name]
Started: [Date]
Investigator: Claude (AI-assisted OSINT)

---

## Log Entries

### [YYYY-MM-DD HH:MM] — [Brief Description]

| Field         | Value                                      |
|---------------|--------------------------------------------|
| **Platform**  | [tavily / searxng / crt.sh / manual / etc] |
| **Query**     | `exact query or URL used`                  |
| **Filters**   | [date range, domain, language, etc.]       |
| **Results**   | [count] results returned                   |
| **Key Finds** | [Brief summary of useful results]          |
| **Action**    | [Added to leads / Dead end / Needs follow-up] |
| **Notes**     | [Any observations, oddities, context]      |

---

### [YYYY-MM-DD HH:MM] — [Next Entry]
...
```

**Rules for the search log:**
- Log BEFORE you search (record the query), then update with results
- Include null results — knowing what returned nothing is valuable
- Record exact queries, not paraphrases
- Timestamp every entry
- Note which tool/MCP server was used
- If a search leads to a new search, reference the parent entry

---

### leads.md

```markdown
# Active Leads

Investigation: [Name]
Last Updated: [Date]

---

## HIGH Priority

### Lead: [Short Title]
- **Source:** [Where this lead came from, reference search-log entry]
- **Summary:** [What the lead is]
- **Next Steps:** [What to do with this lead]
- **Status:** OPEN | IN PROGRESS | RESOLVED
- **Added:** [Date]

---

## MEDIUM Priority

### Lead: [Short Title]
- **Source:** [Reference]
- **Summary:** [Description]
- **Next Steps:** [Actions]
- **Status:** OPEN | IN PROGRESS | RESOLVED
- **Added:** [Date]

---

## LOW Priority

### Lead: [Short Title]
- **Source:** [Reference]
- **Summary:** [Description]
- **Next Steps:** [Actions]
- **Status:** OPEN | IN PROGRESS | RESOLVED
- **Added:** [Date]

---

## Resolved Leads

| Lead | Resolution | Date |
|------|-----------|------|
| [Title] | [Confirmed / Disproven / Merged into X] | [Date] |
```

**Prioritization criteria:**

| Priority | Criteria |
|----------|----------|
| HIGH | Directly answers the investigation question; time-sensitive; unique source |
| MEDIUM | Supports or corroborates a high-priority lead; provides context |
| LOW | Tangential; speculative; requires significant effort for uncertain payoff |

---

### dead-ends.md

```markdown
# Dead Ends

Investigation: [Name]
Last Updated: [Date]

Recording dead ends prevents re-treading and helps future investigators.

---

### [Short Description of What Was Tried]
- **Date:** [Date]
- **Method:** [What tool/approach was used]
- **Query/Action:** `[Exact query or steps taken]`
- **Expected:** [What you hoped to find]
- **Actual:** [What happened — no results, irrelevant results, blocked, etc.]
- **Why Dead End:** [Analysis of why this didn't work]
- **Revisit?** YES / NO — [Conditions under which this might be worth retrying]

---
```

**When to record a dead end:**
- Search returned zero relevant results
- A platform was inaccessible or returned errors
- A lead turned out to be about a different entity (false match)
- An approach was technically infeasible
- Information was behind a paywall or required authentication you don't have

---

### evidence-chain.md

This is OSINT-specific. It tracks the provenance of every finding — how you got from raw data to conclusion. Critical for credibility and verification.

```markdown
# Evidence Chain

Investigation: [Name]
Last Updated: [Date]

---

## Finding: [Concise Statement of Fact]

**Confidence:** HIGH | MEDIUM | LOW | UNVERIFIED

### Source Trail

| Step | Source | Data Found | Tool Used | Timestamp |
|------|--------|-----------|-----------|-----------|
| 1 | [Original source URL or query] | [Raw data] | [Tool] | [Time] |
| 2 | [Follow-up source] | [Corroborating data] | [Tool] | [Time] |
| 3 | [Additional source] | [Further evidence] | [Tool] | [Time] |

### Analysis
[How the raw data leads to the finding. What assumptions were made. What alternative explanations exist.]

### Corroboration
- [x] Source 1: [Description] — CONFIRMS
- [x] Source 2: [Description] — CONFIRMS
- [ ] Source 3: [Description] — CONTRADICTS (explain)

### Caveats
- [Any limitations, assumptions, or uncertainties]

---
```

**Confidence levels:**

| Level | Definition |
|-------|-----------|
| HIGH | Multiple independent sources confirm; no contradictions; data is current |
| MEDIUM | At least two sources agree; minor gaps or dated information |
| LOW | Single source; unverified; circumstantial; old data |
| UNVERIFIED | Raw finding not yet checked against other sources |

---

### report.md

```markdown
# Investigation Report

**Subject:** [What was investigated]
**Date Range:** [Start] to [End]
**Investigator:** Claude (AI-assisted OSINT)
**Classification:** [Open / Restricted / Confidential]

---

## Executive Summary

[2-3 sentences: what was investigated, key findings, confidence level]

---

## Background

[Why this investigation was initiated. What was known at the start.]

---

## Key Findings

### Finding 1: [Title]
- **Confidence:** HIGH / MEDIUM / LOW
- **Summary:** [1-2 sentences]
- **Evidence:** [Reference to evidence-chain.md entries]

### Finding 2: [Title]
...

---

## Timeline

| Date | Event | Source |
|------|-------|--------|
| [Date] | [What happened] | [Reference] |

---

## Entity Summary

| Entity | Type | Key Details | Relationships |
|--------|------|-------------|---------------|
| [Name] | Person/Org/Domain/etc | [Details] | [Connected to X, Y] |

---

## Methodology

[What tools and techniques were used. Reference search-log.md for full details.]

---

## Limitations

- [What couldn't be determined and why]
- [Sources that were unavailable]
- [Assumptions made]

---

## Recommendations

- [Next steps if investigation continues]
- [Additional resources or tools that might help]
- [Leads that remain open]

---

## Appendices

- Full search log: search-log.md
- Active/resolved leads: leads.md
- Dead ends explored: dead-ends.md
- Evidence chains: evidence-chain.md
```

---

## Best Practices

### Starting an Investigation

1. Create the directory structure immediately
2. Write the investigation question in report.md Background section
3. Define scope boundaries before collecting any data
4. Initialize the knowledge graph with known entities

### During the Investigation

- Log every search BEFORE executing it
- Update leads.md after each significant search session
- Move resolved leads to the Resolved table promptly
- Take screenshots of volatile content (social media, forums)
- Archive important web pages via Wayback Machine or local save
- Update the evidence chain as connections emerge

### Closing an Investigation

1. Ensure all leads are marked RESOLVED or documented as OPEN with next steps
2. Verify all evidence chain entries have confidence ratings
3. Write the report.md executive summary last (after all analysis)
4. Review dead-ends.md for any worth revisiting
5. Archive the entire investigation directory

### Common Mistakes to Avoid

| Mistake | Consequence | Prevention |
|---------|------------|------------|
| Not logging searches | Cannot reproduce or audit | Log before searching |
| No timestamps | Cannot establish when data was valid | Timestamp everything |
| Skipping dead ends | Duplicate work later | Always record failures |
| Single-source findings | Low confidence, potential errors | Require corroboration |
| Scope creep | Wasted effort, lost focus | Return to the question |
| No screenshots | Evidence disappears | Screenshot volatile content |

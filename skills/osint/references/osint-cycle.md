# OSINT Intelligence Cycle Reference

The intelligence cycle is the systematic process for conducting OSINT investigations. Each phase feeds into the next, and the cycle repeats as new information refines the approach.

```
    +-----------------+
    |   1. DIRECTION   |
    |    (Planning)    |
    +--------+--------+
             |
             v
    +--------+--------+
    |   2. COLLECTION  |
    | (Gather data)    |
    +--------+--------+
             |
             v
    +--------+--------+
    |  3. PROCESSING   |
    | (Organize data)  |
    +--------+--------+
             |
             v
    +--------+--------+
    |   4. ANALYSIS    |
    | (Interpret data) |
    +--------+--------+
             |
             v
    +--------+--------+
    |  5. DISSEMINATION|
    | (Report findings)|
    +--------+--------+
             |
             +-----> Return to Step 1 if gaps remain
```

---

## Phase 1: Direction and Planning

**Goal:** Define exactly what you need to know before touching any tool.

### Actions

1. **Write the intelligence requirement** — a clear, specific question
   - BAD: "Find out about John Doe"
   - GOOD: "Determine John Doe's professional affiliations and online presence between 2020-2024"
   - GOOD: "Identify the owner and hosting infrastructure of example.com"

2. **Define scope boundaries**
   - What is in scope? (specific domains, platforms, time ranges)
   - What is out of scope? (personal relationships, medical info, etc.)
   - What are the ethical/legal constraints?

3. **Set up the investigation workspace** (see investigation-setup.md)

4. **List known information** — what do you already have?
   - Names, usernames, emails, domains, IPs, photos
   - Enter all known entities into the knowledge graph

5. **Identify likely sources**
   - Where is this type of information typically found?
   - Which tools are appropriate? (see tool-guide.md)

### Avoiding Scope Creep

| Temptation | Response |
|-----------|----------|
| "This person also knows X, let me investigate X too" | Does X answer the original question? If not, note it as a lead and stay focused |
| "I found an interesting tangent about Y" | Log it in leads.md as LOW priority, return to the requirement |
| "I should check every platform" | Prioritize platforms most likely to yield relevant information |
| "I need to go deeper on this one thread" | Set a time box. If nothing after 15 minutes, move on |

### Planning Checklist

- [ ] Intelligence requirement written in report.md
- [ ] Scope boundaries defined
- [ ] Known information listed
- [ ] Investigation workspace created
- [ ] Knowledge graph initialized with known entities
- [ ] Initial source list identified
- [ ] Ethical/legal constraints noted in report.md

---

## Phase 2: Collection

**Goal:** Gather raw data from sources systematically.

### Actions

1. **Start with passive collection** — searches that don't alert the target
   - Web searches (tavily, searxng)
   - DNS/WHOIS lookups
   - Certificate transparency
   - Public records and archives

2. **Expand to broader sources**
   - Social media profiles
   - Forum posts and comments
   - Archived/cached pages
   - Public documents

3. **Log everything** in search-log.md
   - Every query, every platform, every result (including null results)
   - Timestamp all entries

4. **Preserve evidence**
   - Screenshot volatile content
   - Archive web pages
   - Download files before they disappear
   - Hash downloaded files for integrity

### Collection Priority Order

| Priority | Source Type | Risk Level |
|----------|-----------|------------|
| 1 | Search engines, public databases | None — fully passive |
| 2 | Social media (public profiles) | Low — may appear in "who viewed" |
| 3 | DNS, WHOIS, certificate logs | None — public infrastructure |
| 4 | Archives (Wayback, Common Crawl) | None — historical data |
| 5 | Forum posts, comments | Low — public content |
| 6 | Direct URL visits to target sites | Medium — logged in server access logs |

### When to Pivot

Pivot your collection strategy when:

- **New entity discovered:** A search reveals a previously unknown username, email, or domain. Add it to the knowledge graph and plan collection around it.
- **Dead end reached:** A source yields nothing after thorough searching. Move to alternative sources. Record in dead-ends.md.
- **Conflicting information:** Two sources disagree. Prioritize resolving the conflict before collecting more data.
- **Pattern emerges:** Multiple data points suggest a new line of inquiry. Evaluate whether it serves the intelligence requirement.

### Collection Checklist

- [ ] All known identifiers searched across relevant platforms
- [ ] DNS/WHOIS/certificate data collected for domains
- [ ] Social media profiles identified and documented
- [ ] Historical/archived data checked
- [ ] All searches logged with timestamps
- [ ] Volatile evidence preserved (screenshots, archives)
- [ ] Knowledge graph updated with new entities

---

## Phase 3: Processing

**Goal:** Convert raw data into organized, usable information.

### Actions

1. **Deduplicate** — remove redundant data from multiple sources
2. **Normalize** — standardize formats (dates, names, addresses)
3. **Categorize** — sort findings by entity, topic, or relevance
4. **Validate** — check data quality and source reliability
5. **Update the knowledge graph** with processed entities and relationships

### Processing Tasks

| Raw Data | Processed Output |
|----------|-----------------|
| Multiple social profiles | Unified person entity with all platforms |
| DNS records + WHOIS + crt.sh | Complete domain infrastructure map |
| Scattered mentions across forums | Timeline of activity |
| Multiple email addresses | Linked identity chain |
| Raw EXIF data from images | Mapped locations and timestamps |
| Email headers | Sender attribution and relay path |

### Source Reliability Assessment

| Grade | Criteria | Example |
|-------|----------|---------|
| A — Highly Reliable | Official records, verified databases | Government registries, court records |
| B — Usually Reliable | Established platforms with verification | LinkedIn (verified profiles), GitHub |
| C — Fairly Reliable | Public records, news sources | News articles, company websites |
| D — Not Usually Reliable | User-generated content, forums | Reddit posts, forum comments |
| E — Unreliable | Anonymous sources, unverified claims | Anonymous tips, 4chan posts |
| F — Cannot Be Judged | Insufficient information to assess | Single mention with no corroboration |

### Handling Information Overload

When you have too much data:

1. **Triage by relevance to the requirement** — does this answer the question?
2. **Sort by source reliability** — prioritize Grade A-C sources
3. **Focus on corroborated facts** — information confirmed by 2+ sources
4. **Set aside uncorroborated leads** — file in leads.md for later
5. **Summarize, don't catalog** — write concise summaries, not exhaustive lists

---

## Phase 4: Analysis

**Goal:** Interpret processed data to draw conclusions and answer the intelligence requirement.

### Analytical Techniques

#### Link Analysis
Map connections between entities. The knowledge graph makes this visual.
- Who is connected to whom?
- What do clusters of connections reveal?
- Are there unexpected connections?

#### Timeline Analysis
Arrange events chronologically.
- When was the domain registered relative to the organization's founding?
- When did social media activity start/stop?
- Do timestamps in photos match claimed locations?

#### Pattern Analysis
Look for recurring behaviors or attributes.
- Same username across multiple platforms
- Similar writing style across different accounts
- Regular posting schedule suggesting timezone
- Shared infrastructure (IP, hosting, registrar)

#### Gap Analysis
Identify what is missing.
- Why does this person have no social media presence?
- Why was this domain registered with privacy protection?
- What happened during the gap in posting activity?

#### Competing Hypotheses (ACH)

| Hypothesis | Evidence For | Evidence Against | Inconsistencies |
|-----------|-------------|-----------------|-----------------|
| H1: [Scenario A] | [List] | [List] | [List] |
| H2: [Scenario B] | [List] | [List] | [List] |
| H3: [Scenario C] | [List] | [List] | [List] |

The hypothesis with the least evidence against it (not the most evidence for it) is typically strongest.

### Confidence Assessment

| Level | Meaning | Requirements |
|-------|---------|-------------|
| HIGH | Almost certainly true | 3+ independent sources agree; no contradictions; current data |
| MEDIUM | Probably true | 2 sources agree; minor gaps or slightly dated |
| LOW | Possibly true | Single source; circumstantial; significant assumptions required |
| UNVERIFIED | Unknown reliability | Not yet checked against other sources |

### Analysis Pitfalls

| Pitfall | Description | Mitigation |
|---------|------------|------------|
| Confirmation bias | Seeking data that supports your initial theory | Actively look for disconfirming evidence |
| Anchoring | Over-relying on the first piece of information found | Give equal weight to later findings |
| Assumption of identity | Assuming same username = same person | Verify with additional corroborating data |
| Recency bias | Giving more weight to recent data | Consider historical context |
| Correlation vs. causation | Assuming connection implies involvement | Distinguish association from causation |
| Mirror imaging | Assuming the subject thinks/acts like you | Consider cultural and contextual differences |

---

## Phase 5: Dissemination

**Goal:** Communicate findings clearly, accurately, and actionably.

### Report Structure

Use the report.md template from investigation-setup.md. Key elements:

1. **Executive Summary** — 2-3 sentences answering the intelligence requirement
2. **Key Findings** — numbered, with confidence levels
3. **Evidence** — linked to evidence-chain.md entries
4. **Limitations** — what couldn't be determined
5. **Recommendations** — next steps if needed

### Reporting Principles

| Principle | Application |
|-----------|------------|
| Distinguish fact from inference | "The domain was registered on 2020-01-15" (fact) vs. "The subject likely registered the domain" (inference) |
| State confidence levels | Always attach HIGH/MEDIUM/LOW to conclusions |
| Cite sources | Every claim links back to evidence-chain.md |
| Report gaps | What you couldn't find is as important as what you found |
| Be actionable | Tell the reader what they can do with this information |

### When to Return to Phase 1

The cycle restarts when:

- **Findings reveal new questions** that weren't part of the original requirement
- **Key gaps remain** that could be filled with additional collection
- **Conflicting evidence** requires targeted collection to resolve
- **The requirement changes** based on initial findings
- **New tools or techniques** become available that could yield more data

---

## When to Stop an Investigation

### Positive Stopping Points

- The intelligence requirement has been answered with sufficient confidence
- All reasonable sources have been exhausted
- Additional collection yields diminishing returns (same information from new sources)

### Mandatory Stopping Points

- **Ethical boundary reached** — investigation would require unethical actions to continue
- **Legal boundary reached** — next steps would violate applicable law
- **Subject is a minor** — extra caution required; reassess scope and necessity
- **PII exceeds scope** — found personal information beyond what the investigation requires
- **Safety concern** — investigation could endanger someone

### Diminishing Returns Indicators

| Signal | Meaning |
|--------|---------|
| Last 5 searches yielded nothing new | Collection phase likely exhausted for current approach |
| Same facts appearing from multiple sources | Good corroboration, but no new information |
| Leads are all LOW priority | Major avenues explored |
| Knowledge graph hasn't grown in 10+ queries | Time to analyze what you have or fundamentally change approach |

---

## Quick Reference: Phase Actions

| Phase | Key Action | Key Output | Key Tool |
|-------|-----------|-----------|----------|
| Direction | Define the requirement | Scoped investigation plan | investigation-setup.md templates |
| Collection | Search and preserve | Populated search-log.md | tavily, searxng, scripts |
| Processing | Organize and validate | Updated knowledge graph | memory-graph |
| Analysis | Interpret and conclude | evidence-chain.md entries | Analytical reasoning |
| Dissemination | Report findings | Completed report.md | report template |

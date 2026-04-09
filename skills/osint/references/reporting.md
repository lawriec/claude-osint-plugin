# OSINT Investigation Reporting

Structured reporting standards for documenting OSINT findings. Good reporting is the difference between raw data and actionable intelligence.

---

## Confidence Levels

Every finding must be assigned a confidence level. Use these consistently throughout all reports.

### Definitions

| Level | Label | Criteria | Usage |
|-------|-------|----------|-------|
| **1** | **Confirmed** | Multiple independent sources agree. Direct, verifiable evidence. Reproducible. | "The domain example.com resolves to 93.184.216.34 (confirmed via DNS query and Shodan)" |
| **2** | **Probable** | Strong evidence from one or more reliable sources. Consistent with other known facts. Minor gaps acceptable. | "The account @johndoe likely belongs to John Doe of Springfield (matching name, location, employer in bio, profile photo consistent with LinkedIn)" |
| **3** | **Possible** | Some evidence but requires corroboration. Single source. Logical inference with supporting circumstantial evidence. | "The subject may have traveled to Berlin in March (Instagram story shows Brandenburg Gate, but no geotag and date uncertain)" |
| **4** | **Speculative** | Weak evidence, circumstantial only, or analytical inference without direct support. Single unverified source. | "The anonymous blog may be authored by the subject (writing style is similar, but no direct link established)" |

### Rules for Confidence Assessment

- **Never overstate confidence.** When in doubt, go one level lower.
- **Multiple weak sources do not make a strong source.** Three rumors are not confirmation.
- **Absence of evidence is not evidence of absence.** Report what was NOT found, and note it does not prove non-existence.
- **Corroboration requires independence.** Two articles citing the same press release is one source, not two.
- **Digital evidence can be fabricated.** EXIF data, screenshots, and social media posts can all be spoofed. Note this when relevant.
- **Timeliness matters.** A 2019 WHOIS record is less confident evidence of current ownership than a 2024 record.

---

## Report Structure

### Full Investigation Report

Use this template for comprehensive investigations:

```markdown
# Investigation Report: [Subject/Topic]

**Date:** YYYY-MM-DD
**Analyst:** [Name/Handle]
**Classification:** [If applicable]
**Distribution:** [Who should receive this]

---

## Executive Summary

[2-3 sentences. State the key finding, its confidence level, and its significance.
This section should stand alone -- a reader who only reads this section should
understand the essential outcome.]

## Intelligence Requirement

[What question was this investigation trying to answer?
Who requested it and why? What decisions depend on the answer?]

## Scope and Limitations

[What was investigated and what was explicitly excluded.
Any time constraints, tool limitations, or access restrictions.
This manages expectations and prevents misinterpretation.]

---

## Key Findings

### Finding 1: [Descriptive Title]

- **Confidence:** Confirmed / Probable / Possible / Speculative
- **Summary:** [One paragraph describing what was found]
- **Evidence:**
  - [Source 1 -- type, URL/reference]: [What it shows] (accessed YYYY-MM-DD)
  - [Source 2 -- type, URL/reference]: [What it shows] (accessed YYYY-MM-DD)
  - [Source 3 -- type, URL/reference]: [What it shows] (accessed YYYY-MM-DD)
- **Analysis:** [Why this evidence supports the finding. Address alternative
  explanations and why they were ruled out or remain possible.]

### Finding 2: [Descriptive Title]

[Same structure as above]

---

## Negative Results

[What was searched for but NOT found. This section is critically important.
Negative results tell the reader what avenues have been explored without success,
preventing duplicated effort and providing analytical value.]

- Searched [platform/database] for [query] -- no results (YYYY-MM-DD)
- No EXIF GPS data present in any examined images
- WHOIS records fully redacted; historical records not available
- No social media presence found under [username/name]

## Connections and Relationships

[How findings relate to each other. This can be a visual diagram
(ASCII, Mermaid, or described textually) or a narrative explanation.]

Example relationship map:

  Subject --> email@example.com --> registered on Platform A, Platform B
  Subject --> @username --> active on Twitter, GitHub, Reddit
  email@example.com --> domain.com (WHOIS) --> IP 1.2.3.4 --> shared hosting
  @username (Twitter) --> follows @associate1, @associate2

## Methodology

[Brief description of tools and techniques used, in enough detail that another
analyst could reproduce the work.]

- Username enumeration: check_username.py, Sherlock
- Domain analysis: query_whois.py, query_dns.py, query_crtsh.py
- Image analysis: extract_exif.py, reverse image search (Google Lens, Yandex)
- Social media: Manual review of public profiles on [platforms]
- OSINT databases: [list databases consulted]

## Recommendations

[Suggested next steps if the investigation is incomplete or if actions should be taken.]

- [ ] Verify Finding 2 with additional sources
- [ ] Monitor [target] for changes over next [period]
- [ ] Request access to [database/tool] for deeper analysis
- [ ] Consider active reconnaissance of [target] (requires authorization)
- [ ] Preserve evidence at [URL] before potential deletion

## Appendix

### A. Evidence Log

[Full list of all evidence collected, with hashes and archive links.
Reference the evidence documentation template from image-video-forensics.md.]

### B. Search Log

| Date | Tool/Platform | Query | Results |
|------|--------------|-------|---------|
| YYYY-MM-DD | Google | "subject name" | 47 results, 3 relevant |
| YYYY-MM-DD | Sherlock | username123 | Found on 12 platforms |
| YYYY-MM-DD | query_whois.py | domain.com | Registrant redacted |

### C. Raw Data

[Unprocessed outputs from tools, full EXIF dumps, complete DNS records, etc.
Include only what is necessary for verification.]

### D. Timeline

| Date | Event | Source | Confidence |
|------|-------|--------|------------|
| 2020-03-15 | Domain registered | WHOIS | Confirmed |
| 2020-04-01 | First tweet from @username | Twitter | Confirmed |
| 2020-06-?? | LinkedIn profile created | LinkedIn (est.) | Possible |
```

---

## Evidence Chain Documentation

Every conclusion must trace back to evidence through a clear chain.

### The Evidence Chain

```
Source --> Raw Data --> Processed Finding --> Analysis --> Conclusion
```

**Example:**

```
Source: Twitter profile @johndoe (https://x.com/johndoe, accessed 2024-11-15)
  |
  v
Raw Data: Bio reads "Software engineer at Acme Corp, San Francisco"
           Profile photo shows male, ~30s
           Account created March 2019
           Posts primarily 9am-6pm PST
  |
  v
Processed Finding: User claims to be a software engineer at Acme Corp in SF
                   Active during US Pacific business hours
  |
  v
Analysis: Cross-referenced with LinkedIn profile for "John Doe" at Acme Corp (confirmed)
          Posting times consistent with PST timezone (confirmed)
          Profile photo matches LinkedIn photo (probable same person)
  |
  v
Conclusion: Twitter @johndoe is PROBABLY operated by John Doe, software engineer
            at Acme Corp, San Francisco (Confidence: Probable)
```

### Chain Breaks

If any link in the chain is weak, the entire conclusion is weakened. Note chain breaks explicitly:

- "Note: The LinkedIn profile could not be independently verified as belonging to the same individual"
- "Note: Posting time analysis is based on only 15 data points over 3 days"
- "Note: The profile photo match is subjective and could not be confirmed with face recognition tools"

---

## Quick Reporting Formats

Not every investigation needs a full report. Use the appropriate format for the situation.

### Intelligence Note (1-2 paragraphs)

For single findings or quick updates:

```
INTELLIGENCE NOTE -- YYYY-MM-DD
Subject: [Topic]
Confidence: [Level]

[1-2 paragraphs describing the finding, evidence, and significance]

Sources: [List]
```

### Indicator Report

For sharing technical indicators (IPs, domains, hashes):

```
INDICATOR REPORT -- YYYY-MM-DD

Indicators:
- Domain: malicious-example.com (registered 2024-10-01, Namecheap)
- IP: 198.51.100.42 (AS12345, Hosting Provider X, Netherlands)
- IP: 203.0.113.55 (AS67890, VPS Provider Y, Romania)
- SHA-256: abc123... (malware sample)

Context: [Brief description of how these indicators are related]
Confidence: [Level]
First Seen: YYYY-MM-DD
```

### Profile Summary

For person-of-interest summaries:

```
PROFILE SUMMARY -- YYYY-MM-DD
Subject: [Name/Handle]

Identifiers:
- Name: [Full name] (Confidence: X)
- Usernames: [list] (Confidence: X per platform)
- Email: [address] (Confidence: X)
- Location: [city/country] (Confidence: X)
- Employer: [company] (Confidence: X)

Online Presence:
- [Platform]: [URL] -- [brief description of activity]

Key Findings:
- [Finding 1]
- [Finding 2]

Assessment: [Overall summary paragraph]
```

---

## Best Practices

### Objectivity

- **Separate facts from analysis.** "The WHOIS record shows registration on 2024-01-15" is a fact. "The recent registration suggests this may be a temporary infrastructure" is analysis. Keep them distinct.
- **Present alternative explanations.** If evidence could support multiple conclusions, state them all with relative likelihood.
- **Avoid loaded language.** Use "the subject" not "the suspect." Use "the domain was registered" not "the domain was set up to deceive."
- **Acknowledge uncertainty.** It is better to say "insufficient evidence to determine" than to guess.

### Completeness

- **Include negative results.** What you searched for and did not find is valuable intelligence.
- **Date everything.** Websites change. A finding from last week may not be reproducible today. Always include the date evidence was accessed.
- **Provide verification paths.** Include enough detail (URLs, queries, tools) that another analyst could verify your work.
- **Document your methodology.** If someone else needs to continue or audit the investigation, they need to know what was done.

### Audience Awareness

- **Executive audience:** Lead with the executive summary. Use plain language. Focus on "so what" and recommended actions.
- **Technical audience:** Include raw data, tool outputs, and detailed methodology.
- **Legal audience:** Emphasize evidence chain integrity, source reliability, and confidence levels. Note any ethical or legal considerations.
- **Mixed audience:** Use the full report structure with clear sections -- readers can skip to their area of interest.

### Handling Sensitive Information

- **Minimize PII.** Include only the personal information necessary for the investigation purpose.
- **Redact appropriately.** If sharing the report beyond the requesting party, redact PII that is not essential for the recipient.
- **Mark sensitivity.** Clearly label reports containing PII or sensitive findings.
- **Consider the subject.** Even in investigations, the subject is a person. Report facts, not judgments of character.
- **Secure storage.** Reports containing PII or sensitive findings should be stored securely with appropriate access controls.

### Common Mistakes to Avoid

1. **Confirmation bias** -- Seeking evidence that supports a preconceived conclusion while ignoring contradictory evidence.
2. **Source conflation** -- Treating multiple articles citing the same original source as independent corroboration.
3. **Temporal confusion** -- Using old data to make claims about current state without acknowledging the time gap.
4. **Overconfidence** -- Rating a finding as "Confirmed" based on a single source or circumstantial evidence.
5. **Missing context** -- Presenting a finding without explaining its significance or limitations.
6. **Scope creep** -- Including findings unrelated to the intelligence requirement.
7. **Burying the lead** -- Putting the most important finding deep in the report instead of the executive summary.
8. **No negative results** -- Omitting what was searched for but not found, leaving the reader to wonder if those avenues were explored.

---

## Report Quality Checklist

Before finalizing any report, verify:

- [ ] Executive summary accurately reflects key findings
- [ ] Every finding has a confidence level assigned
- [ ] Every finding has cited evidence with access dates
- [ ] Evidence chain is documented (source to conclusion)
- [ ] Negative results are included
- [ ] Methodology is documented
- [ ] Alternative explanations are acknowledged where applicable
- [ ] PII is minimized and handling is appropriate
- [ ] Report answers the original intelligence requirement
- [ ] Recommendations for next steps are included (if investigation is incomplete)
- [ ] All URLs and references are functional (at time of writing)
- [ ] Report has been reviewed for objectivity and loaded language
- [ ] Timestamps use consistent format (UTC recommended)

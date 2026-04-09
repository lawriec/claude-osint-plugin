# OSINT Community Analysis Loop

Instructions for the weekly community analysis workflow. This runs in CI via `community-analysis.yml`.

## Philosophy

We improve the OSINT skill by studying what real investigators do. OSINT communities share techniques, tools, and approaches daily. We sample this knowledge, compare it to our current skill, and propose targeted improvements.

Respect the existing structure. Don't duplicate. Fix errors confidently. Quality over quantity — empty runs are expected and acceptable.

## Important: CI Environment

- MCP tools are NOT available in CI. Check `.mcp.json` for the list of tools we reference but cannot call.
- Scripts in `skills/osint/scripts/` ARE available via `uv run`.
- Only propose changes that are broadly applicable, not niche one-offs.

## Phase 1: Discover and Scrape

### Reddit Threads
```bash
# Discover threads from OSINT subreddits
uv run skills/osint/scripts/discover_reddit_threads.py \
  --all-subs --sort hot --limit 25 --select 10 \
  --with-comments --output-dir reddit-scan/
```

If a subreddit fails, skip it and continue with the others.

### Bellingcat Articles
Use `tavily_search` (if available) or web search to find recent Bellingcat articles:
- Query: `site:bellingcat.com` with date filtering for last 2 weeks
- Save article summaries

### Sector035 Newsletter
Search for the latest "Week in OSINT" from sector035.nl.

## Phase 2: Parallel Analysis

Launch TWO parallel subagents:

### Subagent A: Community Thread Analysis

**Input:** All scraped thread/article content from Phase 1.

**Instructions:**
1. Read ALL scraped content carefully
2. Read the current SKILL.md and ALL files in `skills/osint/references/`
3. Read TODO.md and IDEAS.md
4. For each thread, look for:
   - Search strategies or techniques not in our SKILL.md methodology
   - Tools or platforms missing from our reference files
   - Creative approaches (unusual data sources, clever pivots, cross-reference tricks)
   - Common frustrations that indicate gaps in our documentation
   - Corrections to our existing advice (outdated URLs, defunct tools, wrong info)
5. Output a structured list:
   ```
   ### Finding: [Brief title]
   - **Source:** [Thread title + URL]
   - **Category:** New technique / Missing tool / Missing platform / Correction / Gap
   - **Details:** [What we should add/change]
   - **Which file:** [Which reference file should be updated]
   - **Evidence:** [Quote or summary from the thread]
   ```

### Subagent B: Skill Self-Review

**Input:** None (reads files independently).

**Instructions:**
1. Read SKILL.md, ALL reference files, ALL scripts, TODO.md
2. Evaluate:
   - **Staleness:** Outdated URLs, defunct platforms, deprecated tools
   - **Redundancy:** Repeated advice across files
   - **Clarity:** Confusing sections, poor organization
   - **Consistency:** Contradictions between files
   - **Bloat:** Overly detailed sections that don't earn their space
   - **Missing cross-references:** Scripts that aren't mentioned in reference files, or vice versa
3. Output a structured list:
   ```
   ### Issue: [Brief title]
   - **Category:** Stale / Redundant / Unclear / Inconsistent / Bloated / Missing cross-ref
   - **File:** [Which file]
   - **Details:** [What's wrong]
   - **Proposed fix:** [Specific change]
   ```

## Phase 3: Combine and Create PR

1. Collect findings from both subagents
2. Deduplicate (if both flagged the same issue)
3. Filter: only keep findings that are:
   - Broadly applicable (not niche edge cases)
   - Clearly evidenced (not speculative)
   - Actionable (we can make a specific edit)
4. If NO findings: exit cleanly. Empty runs are normal and expected.
5. If findings exist:
   - Create branch: `claude/community-analysis-YYYYMMDD-HHMMSS`
   - Make minimal, targeted edits to the relevant files
   - Each edit should include a comment or note about the evidence source
   - Commit: `git commit -m "improve: community-sourced OSINT skill updates"`
   - Create PR with structured body:

```markdown
## OSINT Community Analysis — [date]

### Sources Analyzed
- [Thread/article title](URL) — brief summary
- ...

### Proposed Changes (Community-Sourced)
- **[file]**: [change description] — evidence: [source]
- ...

### Proposed Changes (Self-Review)
- **[file]**: [change description] — reason: [why]
- ...

### Evidence
[Key quotes or summaries with attribution]
```

## Principles

1. **Fix errors confidently** — if a URL is dead, a tool is renamed, or info is wrong, fix it
2. **Add cautiously** — new techniques must be broadly applicable
3. **Never reorganize** — add where appropriate, don't restructure files
4. **Cite sources** — every addition traces to a community thread or article
5. **Respect existing patterns** — follow the formatting of the file you're editing
6. **Small PRs** — focused changes are easier to review

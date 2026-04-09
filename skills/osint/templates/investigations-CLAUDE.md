# CLAUDE.md — OSINT Investigations Workspace

This directory contains OSINT investigations. Each subdirectory is a separate investigation.

## Structure

```
investigations-workspace/
├── CLAUDE.md               # This file
├── .gitignore              # Ignores sensitive data
├── knowledge-graph/        # Shared knowledge graph (memory-graph MCP)
└── <investigation-name>/   # One folder per investigation
    ├── search-log.md       # Every query and result (audit trail)
    ├── leads.md            # Active leads with priority
    ├── dead-ends.md        # Failed approaches
    ├── evidence-chain.md   # Source → finding → conclusion
    ├── report.md           # Structured findings
    └── downloads/          # Saved artifacts (screenshots, files)
```

## Working in This Workspace

1. **Always log queries** in search-log.md — every tool call, every search, every result
2. **Update leads.md** when you find something promising
3. **Record dead ends** so you don't repeat them
4. **Maintain evidence chains** — every finding must trace to a source
5. **Use the knowledge graph** to track entities and relationships across investigations

## Ethics

- Only use publicly available information
- Never access accounts you don't own
- Document ethical reasoning when in doubt
- Be aware of legal boundaries in the relevant jurisdiction

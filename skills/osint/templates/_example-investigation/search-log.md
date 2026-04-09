# Search Log

Every query, tool, and result is recorded here. This is the audit trail — it makes the investigation reproducible and prevents duplicate work.

## Format

| # | Timestamp | Tool/Platform | Query/Action | Result | Follow-up |
|---|-----------|--------------|--------------|--------|-----------|
| 1 | 2024-01-15 10:30 | tavily_search | "john doe" site:linkedin.com | 3 results, 1 relevant profile | → leads.md #1 |
| 2 | 2024-01-15 10:35 | query_dns.py | all example.com | A: 93.184.216.34, MX: mx.example.com | → check IP with Shodan |
| 3 | 2024-01-15 10:40 | query_shodan_internetdb.py | 93.184.216.34 | Ports: 80, 443. No vulns. | → dead-ends.md (nothing unusual) |

## Notes

- Log EVERY query, even ones that return nothing
- Record negative results — they prevent repeating dead-end searches
- Link to leads.md or dead-ends.md as appropriate
- Include the exact query used so it can be reproduced

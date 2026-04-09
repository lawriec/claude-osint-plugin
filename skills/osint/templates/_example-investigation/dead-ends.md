# Dead Ends

Track what was tried and why it didn't work. This prevents wasting time repeating failed approaches and helps future investigators.

## Format

### Dead End #1: [What was tried]
- **Search log entry:** #N
- **What happened:** [Why it didn't work]
- **Lesson:** [What to remember for future attempts]

---

### Dead End #1: Shodan scan of primary IP
- **Search log entry:** #3
- **What happened:** IP 93.184.216.34 only shows standard web ports (80, 443), no unusual services or vulnerabilities
- **Lesson:** This is likely behind a CDN — the real server IP may be different. Try historical DNS records or certificate transparency.

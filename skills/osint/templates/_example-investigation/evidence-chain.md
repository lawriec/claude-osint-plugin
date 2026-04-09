# Evidence Chain

Document the provenance of every finding. Each conclusion must trace back to verifiable sources.

## Format

### Evidence Chain #1: [Conclusion]
- **Confidence:** Confirmed / Probable / Possible / Speculative
- **Chain:**
  1. **Source:** [URL/tool/platform] (accessed YYYY-MM-DD HH:MM)
  2. **Raw data:** [What the source returned]
  3. **Processing:** [How the raw data was interpreted]
  4. **Finding:** [What this means for the investigation]
- **Corroboration:** [Other sources that support or contradict this]

---

### Evidence Chain #1: Target is based in London, UK
- **Confidence:** Probable
- **Chain:**
  1. **Source:** LinkedIn profile (accessed 2024-01-15 10:30) — lists "London, England"
  2. **Source:** Twitter profile @johndoe (accessed 2024-01-15 10:45) — bio says "London-based"
  3. **Source:** Domain WHOIS for johndoe.com (accessed 2024-01-15 11:00) — registrant country: GB
  4. **Finding:** Three independent sources indicate London, UK
- **Corroboration:** Posting times consistent with GMT/BST timezone (analyzed via tweet timestamps)

### Evidence Chain #2: Target owns johndoe.com
- **Confidence:** Possible
- **Chain:**
  1. **Source:** WHOIS lookup (accessed 2024-01-15 11:00) — registrant name redacted (GDPR)
  2. **Source:** crt.sh search (accessed 2024-01-15 11:05) — SSL cert issued to johndoe.com
  3. **Source:** Website content (accessed 2024-01-15 11:10) — "About Me" page mentions same workplace as LinkedIn
  4. **Finding:** Circumstantial evidence links target to domain, but registrant is redacted
- **Corroboration:** Need additional evidence (e.g., email headers, DNS records matching known infrastructure)

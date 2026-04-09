# IDEAS — Unstructured Brainstorming

Raw ideas that haven't been fleshed out yet. Items get promoted to TODO.md when specified enough to build.

The community analysis workflow can append ideas here. Manual additions welcome.

---

## Tool Ideas

- **Geolocation AI assistant** — Fine-tuned model for GeoGuessr-style location identification from image features. Could be a specialized Gemini prompt or a custom model.
- **OSINT dashboard** — Web UI for managing investigations, visualizing knowledge graphs, tracking progress. Overkill for now but interesting long-term.
- **Automated EXIF stripper checker** — Given a social media platform, document which metadata is preserved vs. stripped on upload.
- **Google Lens automation** — Selenium script specifically for Google Lens reverse image search with structured output.
- **Yandex image search automation** — Yandex often finds matches Google misses, especially for Russian/Eastern European content.
- **TinEye oldest-first search** — Automated TinEye search sorted by oldest result to find original image source.
- **Archive.today automation** — Save current page snapshots and search for historical snapshots.
- **Wayback Machine diff tool** — Compare two snapshots of the same page to see what changed.

## Reference Ideas

- **Country-specific OSINT guides** — Detailed guides for doing OSINT in specific countries (US, UK, Russia, China, etc.) with local platforms, registries, and legal considerations.
- **Corporate OSINT** — Investigating companies: SEC filings, company registries, beneficial ownership, corporate structure mapping.
- **Academic OSINT** — Research paper searches, author disambiguation, citation network analysis.
- **Election/political OSINT** — Campaign finance, voter records (US-specific), political ad archives.
- **Maritime OSINT** — Detailed AIS analysis, port tracking, vessel ownership chains.
- **Aviation OSINT** — ADS-B analysis, flight pattern analysis, aircraft ownership chains.
- **Satellite imagery OSINT** — Sentinel Hub, Planet Labs, Maxar — free and paid options for overhead imagery.

## Challenge Ideas

- **Time-based challenges** — "This photo was taken at a specific time of day. When?" (shadow analysis)
- **Multi-language challenges** — Clues in non-Latin scripts (Arabic, Cyrillic, CJK, Devanagari). Requires translation and cross-cultural platform knowledge. Inspired by Sofia Santos/gralhix exercises.
- **Historical OSINT** — "This website existed in 2015 but is gone now. What did it say?" (Wayback Machine)
- **Social engineering awareness** — "What information is publicly available that could be used for social engineering?" (ethical awareness)
- **Supply chain OSINT** — "Map the technology stack of this company from public information"
- **Real CTF challenges** — Port past OSINT CTF challenges from SANS, TraceLabs, etc.
- **IP camera / device discovery** — LinusKay IPcam-style: identify a location from an IP camera stream using visible clues + Shodan device data. Requires: query_shodan_internetdb.py, geolocation skills.
- **GitHub / code repo forensics** — OSINT Dojo-style: extract identity from a GitHub user's commit emails, linked accounts, repo activity patterns, and code comments.
- **Google dorking practical** — Find publicly exposed files on a target domain using only advanced Google operators. Ties to google-dorking-cheatsheet.md reference.
- **Satellite imagery timeline** — Use free Sentinel Hub / Copernicus data to track changes at a location over time. Needs research on free imagery APIs first.
- **Domain parking / sinkhole detection** — Identify whether a domain has been parked, sinkholed, or is actively malicious based on infrastructure fingerprinting patterns.
- **10-step OSINT CTF mega-chain** — A long-form CTF where each answer feeds the next step, spanning all 8 categories. Inspired by TraceLabs and SANS OSINT CTFs.
- **Account clustering** — Given multiple social media accounts, determine if the same person controls them using behavioral correlation (posting patterns, writing style, timing, interests). Inspired by Bellingcat methodology.
- **Event timeline verification** — Fact-check a news claim by building a verified timeline from multiple independent public sources. Bellingcat-style verification challenge.

## Workflow Ideas

- **Investigation templates per domain** — Pre-configured investigation structures for common OSINT tasks (person investigation, domain investigation, geolocation, etc.)
- **Automated reporting** — Generate structured reports from search logs and evidence chains.
- **Quality scoring** — Automated assessment of investigation thoroughness based on search log completeness, evidence chain coverage, and confidence levels.
- **Cross-investigation linking** — Use knowledge graph to find connections between separate investigations.

## OSINT Challenge Sources (for inspiration)

- **gralhix.com** — Sofia Santos' 30+ progressive geolocation/visual OSINT exercises with video walkthroughs
- **challenge.bellingcat.com** — Monthly themed challenges (5 questions per month) from professional investigators
- **osintdojo.com** — Structured ranking system with badge progression across OSINT domains
- **TryHackMe OhSINT** — Beginner-friendly single-image OSINT room with 7 investigative questions
- **github.com/LinusKay/osint-challenges** — 4 diverse challenges (Church Chasing, IPcam, Obsessed, Window Shopping) with solutions

## Community and Learning

- **OSINT training mode** — Walk through challenges step-by-step with explanations, teaching the methodology.
- **Weekly OSINT digest** — Summarize the latest tools, techniques, and investigations from the community.
- **Tool comparison matrix** — Compare features of Sherlock vs. Maigret vs. WhatsMyName, etc.
- **OSINT certification prep** — Study guides for GOSI, SANS SEC497, etc.

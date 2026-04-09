# Challenge: Full OSINT Investigation — Domain to Owner

## Domain
Multi-domain (Infrastructure + People + Social Media)

## Difficulty
Hard

## Scenario
"I've come across the domain `signal.org`. Can you conduct a full OSINT investigation to determine:
1. Who owns/operates this domain?
2. What is the organization behind it?
3. Who are the key public figures associated with it?
4. What does their infrastructure look like?
5. What other online presence do they have?

Compile a structured investigation report with confidence levels for each finding."

## Expected Approach
1. **Infrastructure recon:**
   - `query_whois.py lookup signal.org` — registration data
   - `query_dns.py all signal.org` — DNS infrastructure
   - `query_crtsh.py subdomains signal.org` — certificate transparency
   - `query_shodan_internetdb.py` on discovered IPs

2. **Organization research:**
   - Web search for Signal Foundation
   - Website content analysis (about page, team page)

3. **People research:**
   - Key figures: Moxie Marlinspike (founder/former CEO), Brian Acton (co-founder)
   - `check_username.py` for known handles
   - Social media presence

4. **Cross-referencing:**
   - Domain → Organization → People → Other projects
   - Knowledge graph with all entities

5. **Reporting:**
   - Structured report following template
   - Evidence chains for each finding
   - Confidence levels

## Verification
- Signal is a well-known encrypted messaging platform
- Signal Foundation is a 501(c)(3) nonprofit
- Key figures are publicly known
- Infrastructure should show professional setup

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Organization:**
- Signal Foundation (formerly Signal Technology Foundation)
- 501(c)(3) nonprofit, based in Mountain View, CA
- Founded 2018 by Moxie Marlinspike and Brian Acton

**Key People:**
- Moxie Marlinspike (Matthew Rosenfeld) — original creator of Signal Protocol, former CEO
- Brian Acton — co-founder of WhatsApp, donated $50M to start Signal Foundation
- Meredith Whittaker — current president (as of 2022)

**Infrastructure:**
- signal.org — main domain
- Professional DNS setup with CDN
- Multiple subdomains (community, support, updates, etc.)
- Mobile apps on iOS and Android app stores

**Online Presence:**
- Twitter/X: @signalapp
- GitHub: signalapp (open source!)
- Blog on signal.org
- Community forum

**Expected report quality:**
- 5+ entity types in knowledge graph
- Multiple evidence chains
- Confidence levels: Organization name = Confirmed, People = Confirmed (public), Infrastructure details = Confirmed (directly verifiable)
- Should note the open-source nature (GitHub repos are public evidence)

- **Score 5 if:** Complete investigation with knowledge graph, 3+ evidence chains, structured report, all confidence levels appropriate
- **Score 4 if:** Thorough investigation but missing one of: knowledge graph, evidence chains, or structured report
- **Score 3 if:** Finds correct information but investigation is unstructured
- **Score 2 if:** Only partial investigation (e.g., only infrastructure, no people)
- **Score 1 if:** Minimal effort, relies on prior knowledge

</details>

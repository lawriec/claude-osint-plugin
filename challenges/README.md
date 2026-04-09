# OSINT Challenges

Verifiable OSINT challenges for testing and self-evaluation. Each challenge has a known ground truth so results can be scored.

## How to Use

1. Read the challenge scenario
2. Use the OSINT skill and tools to investigate
3. Compare your findings to the ground truth
4. Score using the rubric below

## Scoring Rubric

| Score | Criteria |
|-------|----------|
| **5 — Expert** | Correct answer with comprehensive evidence chain, used optimal techniques |
| **4 — Proficient** | Correct answer with good evidence, minor inefficiencies in approach |
| **3 — Competent** | Partially correct or correct but with weak evidence chain |
| **2 — Developing** | Wrong answer but reasonable methodology, or correct with no evidence |
| **1 — Novice** | Wrong answer with poor methodology |
| **0 — Fail** | No meaningful attempt or completely wrong approach |

## Challenge Categories

- **geolocation/** — Identify locations from images or descriptions
- **people/** — Investigate public figures or usernames
- **infrastructure/** — Map domains, IPs, and network infrastructure
- **image-forensics/** — Extract and analyze image metadata
- **multi-domain/** — Complex investigations spanning multiple OSINT domains
- **transportation/** — Aircraft and vessel identification and tracking
- **crypto/** — Cryptocurrency wallet analysis and transaction tracing
- **verification/** — Fact-checking, historical web analysis, and threat intelligence
- **corporate/** — Company investigations, ownership chains, and business intelligence

## Challenge Difficulty

- **Easy** — Single tool, single step, clear answer
- **Medium** — Multiple tools, some pivoting needed
- **Hard** — Multi-domain, requires creative approaches, ambiguous starting point

## Adding New Challenges

Each challenge file must have these sections:
1. **Domain** — Which OSINT domain(s)
2. **Difficulty** — Easy / Medium / Hard
3. **Scenario** — The task description (what the "user" would ask)
4. **Expected Approach** — Which tools and techniques should be used
5. **Verification** — How to confirm the answer
6. **Ground Truth** — The correct answer (in a collapsible section)

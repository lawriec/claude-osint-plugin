# Challenge: Behavioral Pattern Analysis

## Domain
People (Behavioral OSINT)

## Difficulty
Hard

## Scenario
"We're investigating whether two anonymous online accounts might be the same person. Account A posts on Reddit (username: hypothetical_user_A) and Account B posts on a tech blog. Both accounts discuss machine learning extensively. Can you outline and demonstrate a methodology for determining whether two anonymous accounts are likely operated by the same person, using only public behavioral indicators? Use real public Reddit data from r/MachineLearning to demonstrate the analysis techniques."

## Expected Approach
1. **Collect sample data** — `discover_reddit_threads.py --subreddit MachineLearning` to pull recent threads for demonstration material
2. **Fetch post content** — Use the Reddit MCP server (`fetch_reddit_post_content`) to retrieve full post and comment text from discovered threads
3. **Demonstrate behavioral analysis framework** with the following dimensions:
   - **(a) Temporal analysis** — Analyze posting times across 7+ days to infer the author's timezone and activity patterns (e.g., consistent posting during US business hours suggests US-based)
   - **(b) Linguistic analysis** — Examine vocabulary, sentence structure, common phrases, and spelling patterns (e.g., recurring use of specific jargon, sentence length distribution)
   - **(c) Topic correlation** — Identify specific sub-topics, cited papers, technical preferences, and domain expertise that narrow the field (e.g., both accounts cite the same niche papers)
   - **(d) Cross-platform username search** — `check_username.py <username>` to check if the same or similar usernames appear on other platforms
   - **(e) Writing style fingerprinting** — Catalog stylistic markers: use of em-dashes vs. hyphens, Oxford comma usage, British vs. American English, capitalization habits, emoji usage, paragraph structure
   - **(f) Knowledge fingerprinting** — Identify specialized knowledge that narrows the potential pool (e.g., expertise in a niche sub-field like federated learning on edge devices suggests a small community of researchers)
4. **Document the methodology** — Present the analysis as a repeatable, structured framework that could be applied to any pair of anonymous accounts
5. **Note ethical boundaries** — Explicitly state that behavioral correlation provides probability not certainty, should supplement other evidence, and must respect privacy and legal boundaries

## Verification
- Real Reddit data from r/MachineLearning should be collected and used for demonstration
- The framework should cover at least 6 distinct analysis dimensions
- Temporal analysis should explain how posting time patterns map to timezone inference
- Linguistic analysis should identify at least 5 distinct stylistic markers to examine
- The methodology should be presented as a reusable framework, not a one-off analysis
- Ethical considerations should be explicitly discussed (probability vs. certainty, privacy, legal)
- The agent should note that behavioral analysis alone is not sufficient for definitive identification

## Ground Truth

<details>
<summary>Click to reveal</summary>

This is a methodology-focused challenge. There is no single correct factual answer — the quality is measured by the comprehensiveness, rigor, and ethical awareness of the framework produced.

**Expected framework components:**
- **Temporal patterns:** Collection of posting timestamps across 7+ days, conversion to hourly histogram, timezone inference from activity gaps (sleep hours), day-of-week patterns (weekday vs. weekend activity)
- **Linguistic markers (5+ distinct patterns):** Sentence length distribution, vocabulary richness (type-token ratio), punctuation preferences (em-dash, semicolon, ellipsis usage), spelling conventions (British vs. American), capitalization habits, paragraph length
- **Topic fingerprinting:** Specific sub-fields mentioned, papers cited, tools/frameworks preferred, opinion positions on debated topics (e.g., scaling laws, open vs. closed models)
- **Cross-platform correlation:** Username reuse, avatar reuse, bio similarity, linked accounts
- **Writing style fingerprinting:** Distinctive patterns that persist across contexts — greeting style, sign-off patterns, hedge words, discourse markers ("however", "that said", "FWIW")
- **Knowledge fingerprinting:** Depth in specific sub-topics that narrows the candidate pool — someone discussing custom CUDA kernels for sparse attention is in a much smaller pool than someone discussing "AI trends"
- **Ethical framework:** Behavioral correlation yields probability not proof, false positives are common (many people share writing traits), analysis should never be the sole basis for action, respect for pseudonymity, legal considerations vary by jurisdiction

### Scoring Rubric
| Score | Criteria |
|-------|----------|
| 5 | Comprehensive framework with 6+ analysis dimensions, real Reddit data used for demonstration, explicit ethical boundary discussion, methodology presented as repeatable, behavioral analysis correctly framed as probabilistic not deterministic |
| 4 | Strong framework with 5+ dimensions and real data, but missing ethical discussion or incomplete methodology documentation |
| 3 | Reasonable framework with 3-4 dimensions, some real data usage, but lacks depth in analysis techniques or ethical awareness |
| 2 | Basic approach with 1-2 dimensions, minimal tool usage, no ethical considerations |
| 1 | No structured methodology, no tool usage, or analysis presented as deterministic rather than probabilistic |

</details>

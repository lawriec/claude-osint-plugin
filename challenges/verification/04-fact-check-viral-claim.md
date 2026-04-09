# Challenge: Fact-Check a Viral Claim

## Domain
Verification (Fact-Checking)

## Difficulty
Medium

## Scenario
"A viral social media post claims: 'The Eiffel Tower was originally intended to be a temporary structure and was supposed to be dismantled in 1909 after 20 years. It was only saved because it was useful as a radio transmission tower.' Can you verify every specific claim in this statement using OSINT sources? For each claim, tell me whether it's confirmed, partially true, misleading, or false -- and show me the evidence."

## Expected Approach
1. **Decompose the claim into verifiable sub-claims** — Break the viral statement into discrete factual assertions:
   - Sub-claim A: "Originally intended to be a temporary structure"
   - Sub-claim B: "Supposed to be dismantled in 1909"
   - Sub-claim C: "After 20 years" (implying construction/opening around 1889)
   - Sub-claim D: "Only saved because it was useful as a radio transmission tower"
2. **Research Sub-claim A (temporary structure)** — Use Tavily (`mcp__tavily__tavily_search`) or SearXNG (`mcp__searxng__searxng_search`):
   - Search for the original 1886 agreement between Gustave Eiffel and the City of Paris
   - Look for primary source references: the concession contract terms
   - Check authoritative sources: tour-eiffel.fr (official site), UNESCO documentation, academic histories
   - Determine whether "temporary" accurately describes the original intent
3. **Research Sub-claim B (dismantled in 1909)** — Search for the concession terms:
   - Find the specific duration of the original concession (20 years from 1889)
   - Determine whether the agreement mandated dismantlement or merely permitted it
   - Search for: "Eiffel Tower 1909 concession" and "Eiffel Tower dismantlement"
   - The distinction between "supposed to be dismantled" and "the city had the option to dismantle" is critical
4. **Research Sub-claim C (20 years / 1889)** — Verify the timeline:
   - Confirm construction dates (started January 1887, completed March 1889)
   - Confirm the 1889 Exposition Universelle (World's Fair) context
   - Verify the 20-year concession period math (1889 + 20 = 1909)
5. **Research Sub-claim D (saved by radio)** — Investigate why the tower was preserved:
   - Search for Gustave Eiffel's scientific experiments conducted from the tower
   - Research the role of wireless telegraphy/radio transmission (military communications)
   - Search for other factors: Eiffel's lobbying efforts, the tower's growing popularity with visitors, scientific utility beyond radio (meteorology, aerodynamics)
   - Determine whether radio was the sole reason or one of several factors
6. **Check existing fact-checks** — Search for prior verification of this specific claim:
   - Search: "Eiffel Tower temporary fact check" and "Eiffel Tower radio saved fact check"
   - Check established fact-checking sites (Snopes, PolitiFact, AFP Fact Check)
   - Use these as supplementary sources, not primary evidence
7. **Use Internet Archive for older references** — If needed, use `ia_search` to find historical sources:
   - Search for early 20th-century accounts of the tower's preservation decision
   - Older sources closer to the actual events carry more weight
8. **Produce structured fact-check report** — For each sub-claim, provide:
   - **Rating:** Confirmed / Partially True / Misleading / False
   - **Evidence:** Specific sources with quotes or key facts
   - **Confidence level:** Based on source quality and corroboration
   - **Nuance:** What the claim gets right and what it oversimplifies

## Verification
- [ ] Decomposed the viral claim into individual verifiable sub-claims
- [ ] Researched each sub-claim independently rather than as a single query
- [ ] Found primary or authoritative sources (official Eiffel Tower documentation, historical records)
- [ ] Correctly identified the 1886 concession agreement
- [ ] Distinguished between "option to dismantle" and "supposed to be dismantled"
- [ ] Identified radio as one factor among several (not the sole reason)
- [ ] Checked existing fact-checks as supplementary sources
- [ ] Rated each sub-claim with nuance rather than binary true/false
- [ ] Cited specific sources for each finding

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Sub-claim analysis:**

1. **"Originally intended to be a temporary structure" = Confirmed**
   - The 1886 agreement between Gustave Eiffel's company and the City of Paris granted a 20-year concession. The tower was built for the 1889 Exposition Universelle (World's Fair) and the concession specified that after 20 years, ownership would transfer to the city, which would have the right to demolish it.
   - The word "temporary" is accurate in the sense that the original agreement had a fixed term, though the tower was built with permanent construction methods (wrought iron, not scaffolding).

2. **"Supposed to be dismantled in 1909" = Partially True**
   - The 20-year concession did expire in 1909, and ownership transferred to the City of Paris at that point. However, "supposed to be dismantled" overstates the case. The agreement gave the city the *option* to dismantle it -- it was not a mandate or a foregone conclusion. By 1909, the tower was already widely valued, and there was debate about its future, not a scheduled demolition.
   - The word "supposed" implies inevitability that did not exist.

3. **"After 20 years" = Confirmed**
   - The tower was inaugurated on March 31, 1889. The 20-year concession from 1889 correctly yields 1909. The math checks out.

4. **"Only saved because it was useful as a radio transmission tower" = Partially True / Misleading**
   - Radio (wireless telegraphy) was indeed a significant factor. In 1903, the French military began using the tower for radio communication. By 1909, it was a critical node in the military's wireless telegraph network, which made it strategically valuable to the government.
   - However, "only saved because" is misleading. Multiple factors contributed:
     - **Eiffel's lobbying:** Gustave Eiffel actively promoted scientific uses of the tower from the beginning, funding meteorological and physics experiments.
     - **Scientific utility:** Beyond radio, the tower was used for meteorological observations, aerodynamics research, and physics experiments.
     - **Public popularity:** By 1909, the tower attracted hundreds of thousands of visitors annually and had become an iconic Paris landmark.
     - **Revenue:** The tower generated significant income from visitors.
   - Radio was likely the most politically decisive factor (it gave the government a concrete national security reason to preserve it), but calling it the "only" reason erases other contributing factors.

**Overall assessment of the viral claim:** Partially True. The core narrative is broadly accurate -- the tower was built with a limited concession, that concession expired around 1909, and radio utility played a role in its preservation. But the claim oversimplifies by implying scheduled demolition (rather than an option) and attributing preservation to a single cause (rather than multiple converging factors). This is typical of viral "fun facts" -- directionally correct but stripped of nuance.

**Scoring:**
- **Score 5 if:** Agent decomposes all sub-claims, researches each independently, finds primary/authoritative sources (the 1886 concession), correctly identifies the "option vs. mandate" distinction for dismantlement, names multiple preservation factors beyond radio (Eiffel's lobbying, scientific use, popularity, revenue), and rates each sub-claim with appropriate nuance
- **Score 4 if:** Agent correctly identifies most sub-claims and researches them with good sources, but may miss one nuance (e.g., does not distinguish option vs. mandate, or does not name specific non-radio factors)
- **Score 3 if:** Agent verifies the broad narrative (temporary, 1909, radio) but treats the claim as essentially true/false without examining nuance in individual sub-claims
- **Score 2 if:** Agent does a single web search and summarizes results without decomposing sub-claims or seeking primary sources
- **Score 1 if:** Agent accepts or rejects the claim without systematic verification, or relies on general knowledge without sourcing

</details>

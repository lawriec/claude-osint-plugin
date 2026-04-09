# Challenge: Geolocation from Sign Language and Road Clues

## Domain
Geolocation

## Difficulty
Medium

## Scenario
"I'm looking at a street-level photo with these features:
- A road sign with text in both Arabic and French
- The road has a white center line and white edge markings
- A green rectangular highway sign with white text
- Palm trees and arid landscape
- Cars driving on the right side
- A distant minaret visible
- The road number on the sign reads 'N1'

Where was this photo likely taken?"

## Expected Approach
1. **Language analysis** — Arabic + French bilingual → North Africa (Morocco, Algeria, Tunisia) or parts of Lebanon
2. **Road markings** — Right-side driving, white markings, green highway signs
3. **Road designation** — "N1" national road numbering
4. **Vegetation** — Palm trees + arid = confirms North Africa or Middle East
5. **Narrowing** — Arabic + French + N1 + green highway signs → Morocco or Algeria most likely
6. **Web search** — Search for "N1 road" in Morocco and Algeria to confirm
7. **Reference** — Check geolocation.md for North African road characteristics

## Verification
- The combination of Arabic+French is strong indicator for Maghreb region
- N1 is a major highway designation used in Morocco (Rabat-Tangier) and Algeria
- Road sign style should be compared to known examples

## Ground Truth

<details>
<summary>Click to reveal</summary>

- **Region:** Maghreb (North Africa)
- **Most likely countries:** Morocco or Algeria
  - **Morocco:** French-Arabic bilingual signs, N1 connects Rabat to Tangier, green highway signs, right-side driving, arid landscape with palm trees
  - **Algeria:** Also French-Arabic, has N1 highway, similar sign conventions
- **Distinguishing factors:**
  - Moroccan highway signs typically have green background with white text and route shields
  - Algerian signs are similar but may use different font styles
  - Moroccan N1 runs along the coast (more palm trees likely)
- **Score 5 if:** Agent identifies Morocco or Algeria with reasoning from all clue types
- **Score 4 if:** Agent identifies Maghreb region with correct reasoning
- **Score 3 if:** Agent identifies North Africa generally
- **Score 1 if:** Agent guesses Middle East without distinguishing Maghreb

</details>

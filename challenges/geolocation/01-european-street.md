# Challenge: European Street Identification

## Domain
Geolocation

## Difficulty
Easy

## Scenario
"I have a description of a street scene from a photo. The photo shows: a narrow cobblestone street, buildings with orange/terracotta tile roofs, a tram line running down the middle, text on a shop sign in a language using diacritics (ř, ž, č), and a spire visible in the background. Where is this?"

## Expected Approach
1. **Language analysis** — Diacritics ř, ž, č are distinctive to Czech language
2. **Infrastructure clues** — Tram systems + cobblestone + terracotta roofs → Central European city
3. **Cross-reference** — Czech cities with tram systems: Prague, Brno, Olomouc, Plzeň, Most, Liberec
4. **Narrow it down** — Prominent spire + tourist-area cobblestone + tram = likely Prague (Praha)
5. **If image were provided** — Would use Gemini for image analysis, reverse image search

## Verification
- Czech diacritics narrow to Czech Republic immediately
- Tram + cobblestone + terracotta + spire is classic Prague old town description
- Could be confirmed with Street View comparison

## Ground Truth

<details>
<summary>Click to reveal</summary>

- **Country:** Czech Republic (Czechia)
- **City:** Prague (Praha) — most likely given the combination of clues
- **Reasoning:**
  - ř is unique to Czech language (not Slovak, which has ŕ instead)
  - Tram network eliminates small towns
  - Cobblestone + terracotta roofs + visible spire = historic center
  - Prague has the most extensive tram network in Czechia and the most recognizable spires
- **Alternative possibilities:** Brno (has trams and old architecture) but less likely given the "tourist photo" nature
- **Score 5 if:** Agent identifies Czech Republic from diacritics, narrows to Prague, explains reasoning
- **Score 3 if:** Agent identifies Central Europe but not specifically Czech Republic
- **Score 1 if:** Agent guesses a European country without reasoning from the clues

</details>

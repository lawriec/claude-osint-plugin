# Challenge: Location from Vegetation and Landscape

## Domain
Geolocation (Environmental Analysis)

## Difficulty
Medium

## Scenario
"I have an outdoor photo with the following visible features but no metadata. Can you estimate the region where this was taken?

- A row of tall, slender **Mediterranean cypress trees** (Cupressus sempervirens) lining a gravel road
- Rolling hills covered in **olive groves** with silvery-green leaves
- Patches of **lavender** in bloom (purple flowers) between the groves
- Dry, rocky **terra rossa** (red-orange) soil visible on exposed hillsides
- A distant **stone farmhouse** with a terracotta tile roof
- Low scrubby vegetation resembling **garrigue** (thyme, rosemary) on uncultivated slopes
- Bright, hazy sunshine suggesting summer heat
- No visible text, signs, or vehicles

Based on these vegetation and landscape clues, where was this photo most likely taken?"

## Expected Approach
1. **Vegetation identification** -- Identify key plant species and their geographic ranges:
   - Mediterranean cypress = Mediterranean basin (southern Europe, Turkey, Middle East)
   - Olive groves = Mediterranean climate zones (30-45 deg N latitude typically)
   - Lavender = Southern France, Italy, Croatia, Greece, Turkey
   - Garrigue = Western Mediterranean scrubland
2. **Soil analysis** -- Terra rossa = limestone-derived red soil common in Mediterranean karst regions (Istria, Puglia, Provence, Crete)
3. **Architecture clues** -- Stone farmhouse with terracotta roof = traditional Mediterranean rural architecture (Italy, southern France, Croatia, Greece)
4. **Climate inference** -- Lavender blooming + dry conditions = June-August Mediterranean summer
5. **Cross-reference** -- Overlap of ALL clues:
   - Cypress + olive + lavender + terra rossa + stone farmhouse narrows strongly to **Tuscany/Umbria (Italy)**, **Provence (France)**, or **Istria (Croatia)**
   - Lavender fields in commercial quantities + olive groves most iconic in Provence and Tuscany
6. **Web research** -- Search for these vegetation combinations to confirm geographic overlap
7. **Confidence assessment** -- Rate confidence levels for each clue's geographic contribution

## Verification
- Mediterranean cypress range: Southern Europe, Turkey, North Africa, Middle East
- Olive cultivation: 30-45 deg N in Mediterranean basin
- Commercial lavender: Provence (France), Tuscany (Italy), Dalmatia (Croatia), parts of Turkey
- Terra rossa soil: Mediterranean karst regions
- The combination should point to a narrow band of Mediterranean Europe

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Most likely regions (ranked):**
1. **Tuscany/Umbria, Italy** (highest probability) -- All five indicators present: cypress-lined roads are iconic, extensive olive groves, lavender cultivation, terra rossa in parts of Chianti/Crete Senesi, classic stone farmhouses (poderi)
2. **Provence, France** (high probability) -- Famous for lavender, has olive groves and cypress, but stone farmhouses (mas) look slightly different; terra rossa less common
3. **Istria, Croatia** (moderate probability) -- Has terra rossa (famous for it), olive groves, some cypress, but lavender is less prevalent
4. **Dalmatian coast, Croatia** (lower probability) -- Olive groves and garrigue present, but lavender less common, architecture differs

**Key reasoning chain:**
- Cypress + olive = Mediterranean (eliminates non-Mediterranean zones)
- Lavender in bloom = summer, narrows to France/Italy/Croatia
- Terra rossa = karst/limestone regions
- Stone farmhouse + terracotta roof = rural Mediterranean vernacular
- The combination of ALL five together most strongly suggests Tuscany

**Scoring:**
- **Score 5 if:** Agent identifies Tuscany/Provence as top candidates with clear reasoning per clue, discusses geographic ranges, and provides confidence levels
- **Score 4 if:** Agent identifies correct region (Mediterranean Europe) with good vegetation analysis but less rigorous cross-referencing
- **Score 3 if:** Agent identifies Mediterranean correctly and names some specific regions
- **Score 2 if:** Agent identifies "Southern Europe" generally but doesn't analyze individual plant species
- **Score 1 if:** Agent doesn't attempt systematic vegetation analysis

</details>

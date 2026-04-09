# Challenge: Shadow Analysis for Time and Location

## Domain
Geolocation (Shadow/Sun Analysis)

## Difficulty
Hard

## Scenario
"I have a photo taken on June 21st (summer solstice). The shadow of a 2-meter tall pole is approximately 1 meter long, pointing due north. The photo metadata says it was taken at 12:00 local time but doesn't include GPS data. Can you determine the approximate latitude where this photo was taken?"

## Expected Approach
1. **Shadow analysis** — Shadow pointing due north + shorter than object = sun is south of observer and high in sky
2. **Calculate sun altitude** — `tan(altitude) = object_height / shadow_length = 2/1 = 2`, so altitude ≈ 63.4°
3. **Summer solstice** — Sun declination = +23.44°
4. **Solar noon** — Shadow pointing due north at noon means sun is due south = solar noon (northern hemisphere)
5. **Latitude calculation** — At solar noon: altitude = 90° - |latitude - declination|
   - 63.4° = 90° - |latitude - 23.44°|
   - |latitude - 23.44°| = 26.6°
   - latitude = 23.44° + 26.6° = 50.04° (northern hemisphere, since shadow points north)
6. **Verify with sun_position.py** — `sun_position.py shadow-length --lat 50 --lon 0 --date 2024-06-21 --time 12:00 --object-height 2`

## Verification
- At latitude ~50°N on June 21st, solar noon sun altitude should be approximately 63.4°
- This corresponds to locations like: London (51.5°N), Prague (50.1°N), Paris (48.9°N), Frankfurt (50.1°N)
- The sun_position.py script should confirm the calculation

## Ground Truth

<details>
<summary>Click to reveal</summary>

- **Approximate latitude:** 50°N (±2°)
- **Calculation:**
  - Shadow ratio: 1m shadow / 2m pole = 0.5
  - Sun altitude: arctan(2/1) = 63.43°
  - On summer solstice (declination +23.44°): latitude = 90° - 63.43° + 23.44° = 50.01°N
- **Possible locations at ~50°N:** London, Paris, Prague, Frankfurt, Brussels, Krakow, Kyiv
- **Key factors:**
  - Shadow pointing north = northern hemisphere
  - Short shadow = high sun altitude
  - Summer solstice = maximum declination
  - Noon = solar noon (sun at highest point)
- **Score 5 if:** Agent calculates latitude within ±2° with clear mathematical reasoning and verifies with script
- **Score 4 if:** Agent gets approximate latitude right but methodology is less rigorous
- **Score 3 if:** Agent identifies "around 50°N" but doesn't show the math
- **Score 2 if:** Agent identifies northern hemisphere mid-latitudes
- **Score 1 if:** Agent doesn't attempt shadow analysis

</details>

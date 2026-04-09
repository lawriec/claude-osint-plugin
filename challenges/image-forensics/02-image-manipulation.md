# Challenge: Image Authenticity Assessment

## Domain
Image / Video Forensics

## Difficulty
Medium

## Scenario
"Someone sent me an image claiming it shows a UFO over the Eiffel Tower. Without the actual image file, describe the complete methodology you would use to determine if this image is authentic or manipulated. What tools would you use, what would you look for, and how would you assess the evidence?"

## Expected Approach
1. **EXIF analysis** — `extract_exif.py extract` for metadata (camera, software, timestamps)
2. **Software detection** — Check EXIF for editing software (Photoshop, GIMP, etc.)
3. **Reverse image search** — Via Selenium to Google Lens, TinEye, Yandex to find original
4. **Visual analysis** — Use Gemini to analyze the image for inconsistencies
5. **Error Level Analysis** — Mention ELA as a technique (different JPEG compression in edited areas)
6. **Shadow/lighting** — Check if UFO lighting matches scene lighting
7. **Perspective** — Check if UFO perspective matches camera angle
8. **Source verification** — Where did the image come from? First appearance?
9. **Historical comparison** — Compare the Eiffel Tower background to known images of the same angle

## Verification
The agent should describe a comprehensive image forensics methodology that covers:
- Technical analysis (EXIF, ELA, compression)
- Visual analysis (shadows, lighting, perspective)
- Provenance research (reverse image search, first appearance)
- Source assessment (who shared it, motivation)

## Ground Truth

<details>
<summary>Click to reveal</summary>

This is a methodology challenge. The agent should demonstrate knowledge of:

1. **Technical forensics:**
   - EXIF metadata check (editing software, camera consistency)
   - JPEG Error Level Analysis (edited areas compress differently)
   - Clone detection (repeated patterns indicate copy-paste)
   - Metadata date vs. claimed date comparison

2. **Visual forensics:**
   - Shadow direction consistency between UFO and scene
   - Lighting color temperature matching
   - Edge artifacts around inserted objects
   - Perspective/scale consistency
   - Reflection analysis (should the UFO reflect in nearby surfaces?)

3. **Provenance research:**
   - Reverse image search for the BASE image (Eiffel Tower without UFO)
   - TinEye for earliest known appearance
   - Search for the specific claim in debunking databases

4. **Source assessment:**
   - Who first posted it? What's their credibility?
   - Is there a known motivation (hoax account, satire, etc.)?
   - Did multiple independent people photograph the same event?

5. **Red flags for manipulation:**
   - Only one photo/video of a public event in a busy area
   - EXIF shows editing software
   - Compression artifacts around the added object
   - Inconsistent lighting/shadows/perspective

- **Score 5 if:** Covers all four areas with specific tool recommendations
- **Score 3 if:** Covers two areas well but misses others
- **Score 1 if:** Only checks EXIF or only does reverse image search

</details>

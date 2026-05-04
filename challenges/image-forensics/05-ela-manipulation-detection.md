# Challenge: ELA Image Manipulation Detection

## Domain
Image / Video Forensics (Error Level Analysis)

## Difficulty
Medium

## Scenario
"A news organization received a photograph from a freelance contributor claiming to show a large crowd gathered in a public square in Lisbon during a political demonstration. The image appears compelling, but the editor has concerns: the crowd density looks unusually high for the reported location, some shadows seem inconsistent, and the contributor has no prior publication history. Before publishing, the editor wants a full image forensic analysis to determine whether the photograph has been digitally manipulated. The image file has been saved locally as `protest_lisbon.jpg`. Please perform a thorough analysis using Error Level Analysis, metadata examination, and visual inspection to assess the image's authenticity."

## Expected Approach
1. **Image metadata extraction** -- Run `extract_exif.py` to get file-level metadata:
   - `uv run extract_exif.py protest_lisbon.jpg`
   - Check for: camera make/model, software used (Photoshop, GIMP indicates editing), date/time original vs date modified
   - Check GPS coordinates if present (do they match Lisbon?)
   - Note any stripped or missing EXIF fields (common when images are edited and re-exported)
2. **Image properties check** -- Run `image_ela.py metadata` for basic format inspection:
   - `uv run image_ela.py metadata protest_lisbon.jpg`
   - Check format (JPEG, PNG), dimensions, color mode, JFIF version, and progressive encoding flag
   - Note if the format or properties are unusual for a photograph (e.g., PNG suggests re-export)
3. **Error Level Analysis** -- Run `image_ela.py analyze` to detect compression inconsistencies:
   - `uv run image_ela.py analyze protest_lisbon.jpg`
   - Examine the output statistics: mean_error, max_error, std_dev, and the per-channel breakdown
   - Review the generated ELA visualization image (`protest_lisbon_ela.png`)
   - Low and uniform error suggests unmodified; high variance or localized bright patches in the ELA visualization indicate potential splicing or cloning
4. **ELA at multiple quality levels** -- Run ELA at different quality settings to confirm findings:
   - `uv run image_ela.py analyze protest_lisbon.jpg --quality 90 --scale 20`
   - `uv run image_ela.py analyze protest_lisbon.jpg --quality 75 --scale 25 --output ela_q75.png`
   - Different quality levels can reveal different types of manipulation
   - Consistent artifacts across quality levels strengthen the finding
5. **Visual AI analysis** -- Use Gemini MCP for contextual assessment:
   - Examine the original image for visual inconsistencies: mismatched lighting directions, cloned regions, warped geometry near edit boundaries, inconsistent noise patterns
   - Examine the ELA visualization output for bright regions that indicate tampering
   - Cross-reference shadow directions with the claimed time and location
6. **Synthesize findings** -- Produce an authenticity assessment:
   - Combine EXIF evidence (editing software, date mismatches, GPS mismatch)
   - Combine ELA evidence (error levels, variance, localized anomalies)
   - Combine visual evidence (shadow consistency, perspective, noise patterns)
   - Rate confidence: confirmed manipulation, likely manipulation, inconclusive, or likely authentic
   - Note limitations of the analysis (ELA alone cannot prove tampering; AI-generated images may show uniform ELA)

## Verification
- [ ] EXIF metadata extracted with `extract_exif.py` and interpreted (camera, software, dates, GPS)
- [ ] Basic image properties checked with `image_ela.py metadata`
- [ ] ELA performed with `image_ela.py analyze` at default settings
- [ ] ELA visualization examined for anomalous regions
- [ ] ELA run at least one additional quality level for confirmation
- [ ] ELA statistics (mean_error, std_dev) interpreted correctly
- [ ] Visual AI analysis used (Gemini MCP) to inspect both original and ELA output
- [ ] All evidence types (metadata, ELA, visual) synthesized into a single assessment
- [ ] Confidence level and limitations stated
- [ ] Methodology described would work on any submitted photograph

## Ground Truth

<details>
<summary>Click to reveal</summary>

**This challenge tests image forensic methodology rather than a specific answer** since the image file is hypothetical. The agent should demonstrate the complete workflow:

1. **EXIF metadata analysis:**
   - Camera make/model present suggests the image came from a real camera; absence is suspicious but common for web-sourced images
   - Software field showing "Adobe Photoshop" or "GIMP" indicates the image was at least opened in an editor (not proof of manipulation, but noteworthy)
   - Date/time original vs file modification date: a mismatch may indicate post-processing
   - GPS coordinates: if present, they should be checked against Lisbon (approx. 38.7N, 9.1W). GPS in a completely different country is a strong indicator of fraud
   - Missing EXIF entirely is suspicious for a photograph claimed to be taken by a freelancer with a real camera

2. **ELA interpretation guide:**
   - Mean error < 5: Low compression artifacts, image appears minimally edited
   - Mean error 5-15: Moderate compression, typical of images saved multiple times or with light edits
   - Mean error > 15: Heavy re-compression or significant manipulation
   - High std_dev relative to mean (>1.5x): Localized editing -- some regions have different compression histories
   - In the ELA visualization: bright regions against a dark background indicate areas that were edited more recently (fewer compression cycles)
   - Uniform brightness in ELA suggests the entire image went through the same compression pipeline

3. **Multi-quality ELA technique:**
   - Running at quality 95 (default) catches fine manipulation
   - Running at quality 75 exaggerates differences, making gross manipulation more obvious
   - If suspicious regions appear consistently across quality levels, the finding is more reliable
   - If they appear only at one quality level, it may be a compression artifact

4. **Visual consistency checks:**
   - Shadow direction should be consistent across the entire image (one sun position)
   - Noise grain should be uniform (spliced regions from different cameras show different grain)
   - Perspective lines should converge naturally (warping from content-aware editing disrupts this)
   - Edge artifacts near people or objects suggest compositing (feathering, halo effects)
   - Clone/stamp detection: repeated patterns in crowds, foliage, or buildings

5. **Limitations the agent should acknowledge:**
   - ELA is most effective on JPEG images; it is less useful for PNG or losslessly compressed formats
   - Multiple re-saves degrade ELA effectiveness (each save normalizes error levels)
   - AI-generated images may show perfectly uniform ELA since they were never photographed
   - Social media platforms strip EXIF and re-compress images, eliminating metadata evidence
   - ELA alone cannot conclusively prove or disprove manipulation

**Scoring:**
- **Score 5 if:** Agent runs extract_exif.py, image_ela.py metadata, image_ela.py analyze (at multiple quality levels), uses Gemini for visual analysis of both original and ELA output, correctly interprets ELA statistics, acknowledges limitations, and produces a synthesized assessment with confidence rating
- **Score 4 if:** Agent runs all three tools (EXIF, metadata, ELA) and interprets results, but only uses one quality level or does not examine the ELA visualization with AI
- **Score 3 if:** Agent runs ELA and EXIF extraction but does not interpret the statistics beyond repeating the raw numbers, or skips visual analysis
- **Score 2 if:** Agent runs only one of the tools (just ELA or just EXIF) without combining evidence types
- **Score 1 if:** Agent does not run `image_ela.py analyze` or provides only a theoretical description without executing tools

</details>

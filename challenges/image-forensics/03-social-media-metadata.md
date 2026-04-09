# Challenge: Social Media Image Provenance

## Domain
Image / Video Forensics

## Difficulty
Medium

## Scenario
"A dramatic photo of a massive supercell thunderstorm is going viral on Twitter/X and Reddit. Multiple accounts are posting it with captions like 'Just saw this outside my window in Oklahoma!' and 'Unreal storm in Kansas right now!' -- but no one is crediting a photographer. I want to find the original source of this image. Can you walk me through how to trace it back to whoever actually took it, figure out when and where it was first posted, and determine whether the current viral posts are misattributing the location?

Assume I can provide the image file for analysis. Outline and execute the full methodology you would use."

Note: This challenge tests methodology and knowledge of platform metadata behavior. The agent should demonstrate the correct workflow even without a specific test image.

## Expected Approach
1. **Extract EXIF metadata** -- `extract_exif.py extract image.jpg`:
   - Check for GPS coordinates, camera make/model, timestamps
   - `extract_exif.py gps image.jpg` for location data
   - `extract_exif.py camera image.jpg` for device info
   - Note: If the image was downloaded from social media, EXIF will likely be stripped (see step 6)
2. **Reverse image search** -- Use Selenium browser automation to search multiple engines:
   - **Google Lens** -- Navigate to `https://lens.google.com` and upload the image for visual matches
   - **TinEye** -- Navigate to `https://tineye.com` and upload; sort results by "Oldest" to find the earliest indexed instance
   - **Yandex Images** -- Navigate to `https://yandex.com/images/` and use reverse search (strongest for finding Eastern European or less-indexed sources)
   - Compare results across all three engines for comprehensive coverage
3. **Check Internet Archive** -- Use `ia_search` MCP tool to search for cached versions:
   - Search the Wayback Machine for URLs found in reverse image search results
   - Check earliest capture date to establish a timeline
4. **Web search for context** -- Search for keywords from the image:
   - Search for "supercell thunderstorm photo original photographer" and similar queries
   - Check storm chaser communities and weather photography forums
   - Look for watermarked versions that might reveal the photographer
5. **Platform-specific metadata analysis** -- Explain what each platform strips:
   - **Twitter/X:** Strips all EXIF metadata including GPS, camera info, timestamps
   - **Facebook:** Strips GPS coordinates but may retain some camera metadata
   - **Instagram:** Strips all EXIF metadata
   - **Reddit:** Strips all EXIF metadata from uploaded images (but link posts preserve the original)
   - **Flickr:** Preserves full EXIF by default (valuable for finding originals)
   - **500px:** Preserves EXIF by default
6. **Establish provenance timeline** -- Combine all findings:
   - Earliest TinEye result date
   - Earliest Wayback Machine capture
   - Earliest social media post found via reverse image search
   - Any photographer portfolio or stock photo site listing with original upload date
7. **Verify location claims** -- If GPS data is found in the original:
   - Cross-reference with weather records for that date and location
   - Compare with storm chaser reports and radar data for the claimed date
   - Assess whether "Oklahoma" and "Kansas" claims are consistent with the actual photo origin

## Verification
- [ ] Attempted EXIF extraction and explained why it may yield no data from social media downloads
- [ ] Used at least two reverse image search engines (Google Lens, TinEye, or Yandex)
- [ ] Specifically used TinEye "oldest" sort to find earliest instance
- [ ] Checked the Wayback Machine for cached versions
- [ ] Correctly described which platforms strip EXIF metadata
- [ ] Outlined a clear timeline methodology for establishing the original source
- [ ] Addressed the conflicting location claims in the scenario

## Ground Truth

<details>
<summary>Click to reveal</summary>

This challenge tests methodology rather than a specific answer. The agent should demonstrate:

1. **EXIF awareness:**
   - Know that social media platforms strip EXIF data on upload
   - Still attempt extraction in case the provided file is an original or from an EXIF-preserving source
   - Understand that the absence of EXIF in a social media download is expected, not a dead end

2. **Reverse image search competency:**
   - Use multiple engines (each has different indices and strengths)
   - TinEye is critical for provenance work because of its "oldest" and "best match" sorting
   - Yandex often finds matches that Google misses, especially from non-English sources
   - Google Lens is strongest for finding visually similar (not identical) images

3. **Platform metadata knowledge (key differentiator):**
   - Twitter/X: strips ALL EXIF on upload
   - Facebook: strips GPS but may keep camera make/model
   - Instagram: strips ALL EXIF on upload
   - Reddit: strips ALL EXIF from uploaded images (i.redd.it), but link posts to external hosts preserve original metadata
   - Flickr: preserves FULL EXIF by default (photographer's choice to disable)
   - 500px: preserves FULL EXIF by default
   - Implication: Finding the image on Flickr or 500px is especially valuable

4. **Archive and timeline methodology:**
   - Wayback Machine can timestamp when a URL was first captured
   - TinEye "oldest" provides the earliest date the image appeared in its index
   - Combining these with social media post dates builds a provenance timeline
   - The earliest instance is the best candidate for the original source

5. **Critical thinking on viral misattribution:**
   - Viral images are frequently reposted with false location/time claims
   - Multiple conflicting claims ("Oklahoma" vs "Kansas") are a red flag
   - The original photographer's post (if found) is the authoritative source for location/date
   - Weather records and radar data can independently verify location claims

**Scoring:**
- **Score 5 if:** Agent demonstrates complete methodology (EXIF + multi-engine reverse search + archive + timeline), correctly explains platform EXIF stripping behavior for 4+ platforms, addresses the conflicting location claims, and provides a structured provenance investigation plan
- **Score 4 if:** Agent covers most methodology steps and knows that platforms strip EXIF, but misses one or two platforms or skips the archive step
- **Score 3 if:** Agent uses reverse image search and EXIF extraction but doesn't demonstrate platform-specific metadata knowledge or timeline methodology
- **Score 2 if:** Agent only suggests reverse image search without a systematic approach to provenance
- **Score 1 if:** Agent doesn't use available tools or suggests only basic web searching

</details>

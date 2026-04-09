# Challenge: Reverse Image Search Investigation

## Domain
Image / Video Forensics (Reverse Search)

## Difficulty
Medium

## Scenario
"A news article uses a dramatic photo of flooding in a city, claiming it shows recent flooding in Bangkok, Thailand. However, a reader suspects the image is old or from a different location. Can you use reverse image search to verify where this photo actually came from, when it was first published, and whether the news article is using it accurately? I want to know the true origin of the image and a timeline of how it spread."

Note: For testing, use any flood-related news image URL. The agent should demonstrate the full multi-engine reverse search methodology regardless of the specific test image.

## Expected Approach
1. **Google Lens reverse search** — Use Selenium MCP (`mcp__selenium__start_browser`, `mcp__selenium__navigate`) to perform a Google Lens reverse image search:
   - Navigate to `lens.google.com`
   - Upload or search the image URL
   - Analyze visually similar results for pages with dates and location context
   - Note the earliest dated match and any geographic references
2. **TinEye reverse search** — Use Selenium MCP to search on TinEye:
   - Navigate to `tineye.com` and submit the image
   - Sort results by "oldest" to find the earliest known instance
   - Record the oldest match URL, domain, and date
   - Note total number of matches for a sense of how widely the image circulated
3. **Yandex reverse image search** — Use Selenium MCP to search on Yandex Images:
   - Navigate to `yandex.com/images` and submit the image
   - Yandex often surfaces Russian, Eastern European, and Asian sources that Google misses
   - Check "similar images" and "pages with this image" tabs
4. **EXIF extraction** — If the original image file is available, run `extract_exif.py extract <image>`:
   - Check for GPS coordinates, camera info, and timestamps
   - Note that images shared through social media or news sites typically have EXIF stripped
5. **Cross-reference dates** — Compare the earliest dates found across all three search engines:
   - Build a list of all dated instances found
   - Identify the earliest credible source
   - Determine if the photo predates the claimed event
6. **Wayback Machine verification** — Use Internet Archive MCP (`ia_search`) to check for cached versions of pages containing the image:
   - Search for the earliest page URLs found in reverse search results
   - Confirm publication dates via cached snapshots
   - This establishes a hard timestamp that cannot be retroactively altered
7. **Compile provenance timeline** — Produce a chronological chain showing:
   - Original source (photographer, agency, or first publisher)
   - Date of original publication
   - Subsequent reshares and reuse instances
   - Whether the news article's claim of "recent Bangkok flooding" is supported or contradicted

## Verification
- [ ] Used Google Lens (or equivalent) for reverse image search
- [ ] Used TinEye with "sort by oldest" to find the earliest instance
- [ ] Used Yandex Images for additional coverage
- [ ] Attempted EXIF extraction and noted whether data was present or stripped
- [ ] Cross-referenced dates from multiple search engines
- [ ] Checked Wayback Machine to verify publication dates of source pages
- [ ] Produced a provenance timeline with original source identification
- [ ] Assessed whether the news article's use of the image is accurate or misleading
- [ ] Noted that news agencies sometimes use stock or archive photos without clear disclosure

## Ground Truth

<details>
<summary>Click to reveal</summary>

This challenge tests multi-engine reverse image search methodology and image provenance analysis. The agent should demonstrate:

1. **Multi-engine approach:** Using 3+ reverse image search engines is essential because each has different index coverage. Google has the broadest web index, TinEye specializes in tracking image reuse over time, and Yandex has superior coverage for non-Western sources.

2. **TinEye "sort by oldest":** This is a critical technique. TinEye's date sorting reveals when an image first appeared online, which directly answers whether a photo predates the claimed event.

3. **Yandex regional coverage:** Yandex often finds matches in Russian-language, Central Asian, and Eastern European sources that Western engines miss entirely. For flooding imagery in Southeast Asia, it may also surface Chinese or Vietnamese sources.

4. **EXIF awareness:** The agent should check for EXIF data but also recognize that most images shared through news sites and social media have EXIF stripped during upload processing.

5. **Wayback Machine as timestamp proof:** Archived page snapshots provide tamper-proof timestamps. If a page containing the image was cached in 2011, the photo cannot be from 2024.

6. **Provenance chain:** The final output should trace the image from original source through reshares, not just identify one match.

7. **Misleading imagery context:** The agent should note that using real but misattributed photos is a common form of misinformation -- the image may be genuine flooding, just not from the claimed time or place.

**Scoring:**
- **Score 5 if:** Agent uses 3+ search engines, sorts TinEye by oldest, extracts or attempts EXIF, checks Wayback Machine, and produces a clear provenance timeline with a well-reasoned assessment of the news article's accuracy
- **Score 4 if:** Agent uses 2-3 engines with correct methodology and produces a reasonable timeline, but misses one element (e.g., no Wayback check or no EXIF attempt)
- **Score 3 if:** Agent performs reverse image searches but does not sort by oldest, does not cross-reference dates, or produces only a superficial assessment
- **Score 2 if:** Agent uses only one search engine and provides a basic match without provenance analysis
- **Score 1 if:** Agent does not perform reverse image searches or relies solely on text-based web searches

</details>

# Challenge: Deepfake and Manipulated Media Detection

## Domain
Verification (Media Forensics + Image Analysis)

## Difficulty
Hard

## Scenario
"A viral image is circulating on social media that appears to show a well-known tech CEO shaking hands with a controversial political figure at what looks like a private fundraiser. The image has been shared thousands of times and is being used to allege a secret political alliance. Before our news organization publishes a story, we need to determine:

1. Is the image authentic, manipulated, or AI-generated?
2. Can we find the original source or an earlier version of the image?
3. What does the metadata tell us about how and when the image was created?
4. Are there visual artifacts consistent with AI generation or digital manipulation?

For this exercise, find a publicly available AI-generated image (search for known examples of AI-generated faces or scenes from websites like thispersondoesnotexist.com, or search for documented deepfake examples) and demonstrate the full verification workflow. The methodology matters more than the specific image."

## Expected Approach
1. **Acquire a test image** -- Use Tavily (`mcp__tavily__tavily_search`) to find a documented AI-generated or manipulated image:
   - Search for "AI generated image example" or "deepfake detection test image"
   - Alternatively, search for known datasets: "this person does not exist", "generated.photos", or "deepfake examples for research"
   - Select an image with a known ground truth (confirmed AI-generated or confirmed manipulated) to validate the methodology
   - Download or reference the image URL for analysis
2. **EXIF metadata extraction** -- Run `extract_exif.py <image_path_or_url>`:
   - Check for camera make, model, lens, and firmware (genuine photos typically have this; AI images do not)
   - Check for GPS coordinates (presence suggests a real photograph)
   - Examine the software field (may show "Adobe Photoshop", "GIMP", or AI generation tools)
   - Check creation/modification timestamps and compare them
   - Note: Completely absent EXIF data is common for both AI-generated images and images that have been stripped/re-saved, so absence alone is not conclusive
3. **Visual analysis with Gemini** -- Use Gemini MCP (`mcp__gemini__ask_question_about_video`) for AI-powered image analysis:
   - Ask: "Examine this image carefully for signs of AI generation or digital manipulation. Look for: inconsistencies in hands (wrong number of fingers, distorted joints), teeth irregularities, asymmetric facial features, text or lettering that is garbled or nonsensical, background inconsistencies (warped lines, impossible geometry, blending artifacts), inconsistent lighting or shadow directions, skin texture anomalies (too smooth, plastic-looking, or with repeating patterns), and edge artifacts where subjects meet the background."
   - Ask: "Does this image show signs of face-swapping? Look for: mismatched skin tone between face and neck, inconsistent lighting angle on the face vs body, blurred or smudged boundaries around the face, different image quality or noise patterns between the face and surrounding areas."
   - Ask: "Examine any text visible in this image. Is it readable and consistent, or does it show the garbled/nonsensical text patterns typical of AI-generated images?"
   - Ask: "Look at the overall scene composition. Are there any physically impossible elements, impossible reflections, or perspective inconsistencies?"
4. **Reverse image search for originals** -- Use Selenium MCP (`mcp__selenium__start_browser`, `mcp__selenium__navigate`) to perform reverse image searches:
   - Navigate to Google Images (images.google.com) and use the "search by image" feature
   - Navigate to TinEye (tineye.com) for additional reverse image search results
   - Search for earlier versions of the image that predate the viral post
   - Look for the same scene with different subjects (indicating a face swap onto an existing photo)
   - Check if the background matches a known stock photo or press image
5. **Provenance chain investigation** -- Use Tavily and SearXNG to trace the image's spread:
   - Search for the earliest known posting of the image
   - Track the sharing chain: who posted it first, on which platform, and when
   - Look for the original context -- was it labeled as AI-generated art, satire, or presented as real?
   - Check if any fact-checking organizations have already examined this specific image
   - Search for `"content credentials" OR "C2PA" OR "content authenticity"` in relation to the image or its source
6. **C2PA/Content Credentials check** -- Investigate whether the image has Content Authenticity Initiative metadata:
   - Use Tavily to search for tools like contentcredentials.org/verify
   - C2PA metadata, when present, provides a cryptographically signed provenance chain showing how the image was created and modified
   - Most AI-generated images currently lack C2PA metadata; its absence is not conclusive but its presence is highly informative
   - Some platforms (Adobe Firefly, Microsoft Designer) are beginning to embed C2PA data in AI-generated content
7. **Cross-reference the claimed event** -- Verify whether the depicted event could have occurred:
   - Search for the specific individuals' public schedules and known appearances
   - Check whether the claimed venue or event exists and matches the background
   - Look for press coverage, attendee lists, or social media posts from the alleged event
   - If no corroborating evidence of the event exists, this supports the image being fabricated
8. **Compile forensic assessment** -- Produce a structured media authentication report:
   - **Metadata analysis:** What EXIF data reveals (or what its absence suggests)
   - **Visual forensics:** Specific artifacts found (or absence of artifacts)
   - **Provenance:** Earliest known source and sharing chain
   - **Contextual verification:** Whether the depicted event has independent corroboration
   - **Confidence assessment:** Authentic / Likely Manipulated / Likely AI-Generated / Inconclusive, with supporting evidence for the determination

## Verification
- [ ] Test image acquired with known ground truth (confirmed AI-generated or manipulated)
- [ ] EXIF metadata extracted and analyzed using extract_exif.py
- [ ] Gemini visual analysis performed with specific artifact detection prompts
- [ ] At least one reverse image search conducted (Google Images or TinEye)
- [ ] Provenance investigation attempted via web search
- [ ] C2PA/Content Credentials discussed or checked
- [ ] Visual artifacts specifically identified and catalogued (hands, text, lighting, edges)
- [ ] Event/context verification attempted
- [ ] Structured forensic report produced with confidence level and methodology summary

## Ground Truth

<details>
<summary>Click to reveal</summary>

**This challenge is methodology-focused.** The specific findings depend on which test image the agent selects. The agent should demonstrate mastery of the media verification workflow regardless of the particular image analyzed.

**Expected methodology demonstration:**

1. **EXIF analysis:** AI-generated images typically lack camera-specific EXIF data (make, model, lens, GPS). If the image has been re-saved or shared through social media, EXIF may be stripped even from genuine photos. The agent should explain what the presence or absence of specific fields suggests without over-claiming based on EXIF alone.

2. **Visual artifact detection via Gemini:** Current AI-generation technology (as of 2025-2026) commonly produces detectable artifacts:
   - **Hands:** Extra or missing fingers, impossible joint angles, asymmetric hands
   - **Text:** Garbled, misspelled, or nonsensical text on signs, clothing, or documents
   - **Eyes:** Mismatched pupil shapes, inconsistent reflections, different iris colors
   - **Hair boundaries:** Unnatural blending where hair meets the background
   - **Background:** Warped architectural lines, impossible geometry, objects that fade into undefined shapes
   - **Skin:** Overly smooth or waxy texture, especially noticeable at boundaries
   - **Lighting:** Inconsistent shadow directions between subjects or between subject and background
   - The agent should ask Gemini multiple specific questions rather than a single vague prompt

3. **Reverse image search:** This is critical for detecting manipulation of existing photos. If the background exists in earlier photos without the claimed subjects, the image is a composite. TinEye's "oldest" and "most changed" sorting options are particularly useful.

4. **Provenance:** The sharing chain matters. An image that first appeared on an anonymous account with no history, was immediately shared by politically motivated accounts, and has no press photographer or event organizer as its source is highly suspicious.

5. **C2PA/Content Credentials:** This is an emerging standard. The agent should demonstrate awareness that:
   - C2PA provides cryptographic provenance when present
   - Most current AI-generated images do not yet include C2PA metadata
   - Adobe, Microsoft, and others are adopting the standard, so it will become increasingly relevant
   - Absence of C2PA is not evidence of manipulation; presence provides strong authenticity signals

6. **Key principle:** No single technique is conclusive. Media verification requires convergent evidence from multiple independent methods. The agent should explicitly state the limitations of each technique and explain how combined evidence supports their conclusion.

**Scoring:**
- **Score 5 if:** Agent demonstrates at least four verification techniques (EXIF analysis, Gemini visual inspection with specific artifact prompts, reverse image search, provenance/context investigation), correctly interprets findings with appropriate caveats, discusses C2PA/Content Credentials, and produces a structured assessment with a confidence level and explicit methodology limitations
- **Score 4 if:** Agent uses three verification techniques effectively, identifies specific visual artifacts or metadata findings, and provides a reasoned assessment with caveats
- **Score 3 if:** Agent uses EXIF analysis and Gemini visual inspection but does not perform reverse image search or provenance investigation, or does not discuss limitations of findings
- **Score 2 if:** Agent uses only one technique (e.g., Gemini visual analysis alone) without corroborating with metadata or reverse image search
- **Score 1 if:** Agent offers an opinion on the image's authenticity without performing systematic forensic analysis using the available tools

</details>

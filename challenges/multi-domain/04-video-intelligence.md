# Challenge: Video Intelligence Analysis

## Domain
Multi-domain (Video Forensics + Geolocation)

## Difficulty
Medium

## Scenario
"An analyst needs to extract intelligence from a public YouTube video. Use the popular 'Walking in Tokyo' style videos (or any well-known walking tour video) to demonstrate the full video intelligence workflow:

1. Extract video metadata
2. Analyze key frames for geolocation clues
3. Extract and analyze any subtitles or captions
4. Determine the filming location and approximate date

Note for testing: Use a well-known YouTube walking tour video. The specific video ID doesn't matter -- demonstrate the methodology. A good starting point is to search for popular walking tour videos and select one with high view counts."

## Expected Approach
1. **Video discovery** -- Use yt-dl MCP (`mcp__yt-dl__ytdlp_search_videos`) to find a suitable walking tour video, or use a known video URL directly.
2. **Metadata extraction** -- Use yt-dl MCP (`mcp__yt-dl__ytdlp_get_video_metadata`) to extract full metadata:
   - Upload date, channel name, video description, tags
   - View count, like count (indicates authenticity)
   - Check for embedded location data in metadata
   - Note video duration, resolution, and format
3. **Subtitle enumeration** -- Use yt-dl MCP (`mcp__yt-dl__ytdlp_list_subtitle_languages`) to check available subtitles:
   - Identify manually uploaded vs auto-generated captions
   - Note which languages are available (may indicate target audience)
4. **Transcript extraction** -- Use yt-dl MCP (`mcp__yt-dl__ytdlp_download_transcript`) for available captions:
   - Extract auto-generated captions if no manual subtitles exist
   - Analyze transcript for location mentions, place names, street names
   - Look for timestamps that correlate with location changes
5. **Frame extraction** -- Use video-reader MCP (`mcp__video-reader__extract_frames` or `mcp__video-reader__extract_frame_at_timestamp`) to pull key frames:
   - Extract frames at regular intervals or at specific timestamps
   - Prioritize frames where scene changes are likely (intersections, landmarks)
6. **Visual analysis** -- Use Gemini MCP (`mcp__gemini__ask_question_about_video`) to analyze the video for intelligence:
   - Ask about visible text, signs, and writing (especially non-Latin scripts)
   - Ask about architectural style, street features, and infrastructure
   - Ask about visible vehicles (license plate format, driving side)
   - Ask about weather conditions, lighting, and time-of-day indicators
   - Ask about any visible landmarks, store names, or brand signage
7. **Cross-referencing** -- Use web search to verify location clues:
   - Search for identified landmarks, store names, or street names
   - Verify the neighborhood or district based on visual clues
   - Confirm filming location against video description claims

## Verification
- [ ] Video metadata successfully extracted (upload date, channel, description)
- [ ] Subtitle languages enumerated
- [ ] Transcript downloaded and analyzed for location references
- [ ] Key frames extracted from the video
- [ ] Gemini visual analysis performed with specific intelligence questions
- [ ] Visible text, signs, or scripts identified from frames or video analysis
- [ ] Filming location determined with supporting evidence
- [ ] Approximate filming date established (from metadata or visual clues)
- [ ] Structured intelligence report produced

## Ground Truth

<details>
<summary>Click to reveal</summary>

**This challenge is methodology-focused.** The specific findings depend on the video selected. The agent should demonstrate mastery of the video intelligence workflow regardless of which video is used.

**Expected methodology demonstration:**

1. **Metadata extraction:** The yt-dl MCP should return structured metadata including upload date, channel info, and description. Walking tour channels often include neighborhood names and dates in descriptions.

2. **Subtitle analysis:** Most walking tour videos have auto-generated captions. These may contain location names spoken by narrators or picked up from ambient audio. Even for silent walking tours, auto-captions may capture background conversations or announcements.

3. **Frame extraction:** Key frames from walking tours contain rich geolocation data -- street signs, store names, vehicle plates, pedestrian crossings, traffic signals, and architectural styles all vary by country and city.

4. **Visual analysis via Gemini:** The AI should identify:
   - Script/language on signs (Japanese, Korean, Chinese, Arabic, Cyrillic, etc.)
   - Driving side (left vs right) and vehicle types
   - Architectural style and urban planning features
   - Specific landmarks or chain stores that narrow location
   - Weather and lighting for time/season estimation

5. **Cross-referencing:** Identified location clues should be verified against web search results to confirm the specific area.

**Scoring:**
- **Score 5 if:** Agent uses all three MCPs (yt-dl, video-reader, Gemini), extracts metadata and transcript, performs visual analysis with specific intelligence questions, identifies the filming location with evidence, and produces a structured report
- **Score 4 if:** Agent uses at least two MCPs effectively, extracts metadata, and identifies the filming location with some visual analysis
- **Score 3 if:** Agent extracts metadata and performs some visual analysis but misses transcript extraction or frame analysis
- **Score 2 if:** Agent only extracts metadata without performing visual or transcript analysis
- **Score 1 if:** Agent fails to use the video-specific MCP tools and relies only on web search

</details>

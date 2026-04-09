# Challenge: EXIF Data Geolocation

## Domain
Image / Video Forensics

## Difficulty
Easy

## Scenario
"I have a JPEG image file. Can you extract any location data from it and tell me where the photo was taken? Also, what camera was used and when was the photo taken?"

Note: For testing, use any JPEG with EXIF data. The agent should demonstrate the correct methodology even if the specific test file varies.

## Expected Approach
1. **Extract EXIF** — `extract_exif.py extract photo.jpg` for full metadata
2. **GPS extraction** — `extract_exif.py gps photo.jpg` for coordinates + map links
3. **Camera info** — `extract_exif.py camera photo.jpg` for make/model/settings
4. **Verify** — Cross-reference GPS coordinates with visual content (if image is available)
5. **Document** — Record findings in evidence chain with confidence levels

## Verification
- Script should successfully extract EXIF data
- GPS coordinates (if present) should be converted to decimal and include map links
- Camera make/model should be extracted
- Agent should note that EXIF can be spoofed and recommend visual verification

## Ground Truth

<details>
<summary>Click to reveal</summary>

This challenge tests methodology rather than a specific answer. The agent should:

1. **Use extract_exif.py** correctly with all three subcommands
2. **Interpret GPS data** — Convert DMS to decimal, provide map links
3. **Note camera info** — Make, model, date/time, settings
4. **Apply OSINT judgment:**
   - Check if GPS matches visual content
   - Note that social media strips EXIF (so original source matters)
   - Note that EXIF timestamps may reflect camera time zone, not photo location time zone
   - Note that EXIF can be manually edited (assess confidence accordingly)
5. **Score 5 if:** Uses all tools correctly, interprets results with appropriate caveats
6. **Score 3 if:** Extracts data but doesn't contextualize it
7. **Score 1 if:** Doesn't use the available scripts

</details>

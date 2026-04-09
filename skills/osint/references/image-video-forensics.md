# Image and Video Forensics for OSINT

Techniques for extracting intelligence from images and videos, detecting manipulation, and preserving digital evidence.

---

## EXIF / Metadata Extraction

### Plugin Tool: `extract_exif.py`

```
python extract_exif.py photo.jpg              # Full EXIF dump
python extract_exif.py gps photo.jpg          # GPS coordinates + Google Maps link
python extract_exif.py summary photo.jpg      # Key fields only
```

### Key EXIF Fields

| Field | Intelligence Value |
|-------|-------------------|
| **GPS Latitude/Longitude** | Direct geolocation (most valuable field) |
| **GPS Altitude** | Elevation above sea level |
| **GPS ImgDirection** | Compass direction the camera was pointing |
| **GPS Speed** | Speed of camera when photo was taken (in vehicles) |
| **DateTimeOriginal** | When the photo was taken |
| **DateTimeDigitized** | When it was digitized (usually same as Original) |
| **OffsetTimeOriginal** | Timezone offset (e.g., +05:30 = India) |
| **Make** | Camera manufacturer (Apple, Samsung, Canon, etc.) |
| **Model** | Specific camera/phone model |
| **Software** | Processing software (firmware version, editing apps) |
| **LensMake / LensModel** | Lens used (for interchangeable lens cameras) |
| **FocalLength** | Lens focal length — affects perspective analysis |
| **FNumber** | Aperture — affects depth of field |
| **ExposureTime** | Shutter speed — can indicate lighting conditions |
| **ISOSpeedRatings** | Sensitivity — high ISO = low light conditions |
| **Flash** | Whether flash fired |
| **Orientation** | How the camera was held (portrait/landscape) |
| **ImageWidth / ImageHeight** | Resolution of the image |
| **XResolution / YResolution** | DPI — may indicate intended print size |
| **Copyright** | Copyright holder information |
| **Artist** | Photographer name (if set) |
| **UserComment** | Freeform text field (sometimes contains interesting data) |

### GPS from EXIF

When GPS data is present, it provides an exact location:

```
python extract_exif.py gps photo.jpg
```

Output example:
```
GPS Coordinates: 48.858370, 2.294481
Google Maps: https://maps.google.com/maps?q=48.858370,2.294481
Altitude: 35.2m above sea level
Direction: 127.5° (SE)
```

**Important Caveats:**
- GPS coordinates can be spoofed or modified
- Verify that the GPS location matches the visual content
- Some cameras have inaccurate GPS (especially older phones or indoor shots)
- GPS may reflect where the photo was edited, not where it was taken (if modified)
- Altitude data can be inaccurate due to GPS vertical error margins

### Which Platforms Strip EXIF

| Platform | EXIF Preserved? | Notes |
|----------|----------------|-------|
| **Twitter/X** | No | Strips all EXIF on upload |
| **Facebook** | No | Strips EXIF; may store location separately if enabled |
| **Instagram** | No | Strips EXIF; location in post metadata if tagged |
| **WhatsApp** | No | Strips EXIF, heavy compression |
| **Signal** | No | Strips EXIF |
| **Telegram (photo)** | No | Strips when sent as photo |
| **Telegram (file)** | Yes | Preserved when sent as document/file |
| **Discord** | No | Strips EXIF |
| **iMessage** | Yes | Preserves EXIF in original quality sharing |
| **Flickr** | Yes | Preserves EXIF (viewable in image properties) |
| **Google Photos (share link)** | No | Stripped for shared links |
| **Google Photos (download)** | Yes | Original EXIF preserved when downloading your own photos |
| **Imgur** | No | Strips EXIF |
| **Reddit** | No | Strips EXIF |
| **Email attachment** | Yes | Original file with all metadata |
| **Dropbox/Drive link** | Yes | Original file preserved |
| **JPEG downloaded from website** | Varies | Depends on server/CMS configuration |

**Strategy:** If EXIF is absent, try to find the original source image (earlier upload, email version, direct download) that may still have metadata.

---

## Reverse Image Search

### Google Lens

Best for general scene/object recognition and finding visually similar images.

- Navigate to lens.google.com
- Upload image or paste URL
- Results include: visually similar images, text in image, objects identified
- Can be automated via Selenium (navigate, upload, capture results)

### Yandex Images

Often superior to Google for:
- **Face recognition** — finds other photos of the same person
- **Eastern European / Russian content** — much better coverage
- **Similar scenes** — finds architectural or landscape matches
- Navigate to yandex.com/images, use camera icon to upload

### TinEye

Best for finding the **original/earliest** version of an image:
- Specializes in finding exact and near-exact matches
- Results sorted by "oldest" reveals the first appearance online
- Useful for debunking claims ("this image is actually from 2018, not 2024")
- API available for batch searches
- tineye.com

### PimEyes

Face recognition search engine:
- Finds other photos of the same face across the web
- Extremely powerful but raises serious ethical concerns
- Read `opsec-ethics.md` before using
- May be restricted or illegal in some jurisdictions
- Only use for legitimate investigations with proper justification

### SauceNAO

Specialized for anime, manga, and illustration:
- saucenao.com
- Identifies artist, source manga/anime, and original posting
- Useful for tracing fan art and illustration origins

### Search Strategy

For any unknown image, run searches in this order:
1. **Google Lens** — broadest coverage, good for objects and scenes
2. **Yandex** — excellent for faces and Eastern European content
3. **TinEye** — find the earliest/original version
4. **Bing Visual Search** — sometimes catches what others miss
5. **Specialized tools** (PimEyes, SauceNAO) if applicable

---

## Image Manipulation Detection

### Error Level Analysis (ELA)

ELA reveals areas of an image with different compression levels, which may indicate editing.

**How it works:**
1. Re-save the JPEG at a known quality level
2. Compare the re-saved version with the original
3. Areas that were recently edited compress differently from the original
4. Edited regions appear as brighter areas in the ELA image

**Tools:**
- **FotoForensics** (fotoforensics.com) — Upload image for automated ELA
- **Ghiro** — Batch image forensics
- **GIMP/Photoshop** — Manual ELA by re-saving and differencing

**Limitations:**
- ELA is not definitive proof of manipulation
- Resaving an image multiple times degrades ELA reliability
- Screenshots have uniform compression (ELA is useless)
- Different areas of a scene naturally have different ELA signatures (e.g., sky vs. detailed area)

### Clone Detection

Look for areas that have been copied and pasted within the same image:
- Repeated patterns or textures
- Unnaturally identical areas
- Tool: FotoForensics clone detection, Forensically (29a.ch/photo-forensics)

### Metadata Inconsistencies

Compare what the EXIF says with what you see:
- **Software field shows editing app** (Photoshop, GIMP, Snapseed) but image claimed as "unedited original"
- **Camera model doesn't match image quality** — a 2010 phone didn't produce 50MP images
- **Dates don't match** — EXIF date is after the claimed event date
- **GPS doesn't match scene** — GPS says London but image shows a tropical beach
- **Thumbnail mismatch** — EXIF thumbnail shows different content than the full image (pre-edit version sometimes survives in thumbnail)

### Visual Inconsistency Analysis

**Shadows:**
- All shadows should be consistent in direction
- Shadow lengths should be proportional for objects at the same distance
- Objects added via compositing often have wrong shadow direction or missing shadows

**Lighting:**
- Light sources should be consistent across the entire image
- Specular highlights (reflections) on different objects should come from the same direction
- Added objects may have different lighting temperature (warm vs. cool)

**Perspective:**
- Vanishing points should be consistent for parallel lines
- Objects composited from different photos may have inconsistent perspective
- Size ratios of known objects can reveal perspective manipulation

**Edges:**
- Look for unnatural edges around objects (sign of poor compositing)
- Halo effects from poor masking
- Color fringing inconsistent with lens characteristics
- Blurring at boundaries that doesn't match depth of field

**Compression Artifacts:**
- JPEG artifacts should be uniform across the image
- Added elements may show different artifact patterns
- Higher quality regions in an otherwise compressed image are suspicious

### AI-Generated Image Detection

Signs of AI-generated images:
- **Hands/fingers** — Often malformed, wrong number of fingers, impossible poses
- **Text** — AI struggles with coherent text in images (gibberish letters/words)
- **Asymmetry** — Glasses frames, earrings, eyes may not match between sides
- **Background inconsistencies** — Objects that blend into each other or defy physics
- **Hair** — Unnatural merging with background
- **Teeth** — Inconsistent number, size, or alignment
- **Skin texture** — Overly smooth or with unnatural patterns

**Detection tools:**
- Hive AI Detector (hivemoderation.com)
- Content Credentials / C2PA metadata (if present)
- Illuminarty (illuminarty.ai)
- AI or Not (aiornot.com)

---

## Video Analysis

### Plugin Video Tools (MCP)

**Get video information:**
```
get_video_info: path/to/video.mp4
```
Returns: codec, resolution, frame rate, duration, file size, embedded metadata.

**Extract frames at regular intervals:**
```
extract_frames: path/to/video.mp4, interval=5
```
Saves a frame every N seconds — use for scanning long videos for content of interest.

**Extract a specific frame:**
```
extract_frame_at_timestamp: path/to/video.mp4, timestamp="01:23:45"
```
Get the exact frame at a specific time — use when you've identified a moment of interest.

**Generate thumbnail grid:**
```
generate_thumbnail_grid: path/to/video.mp4, rows=4, cols=4
```
Creates a single image with a grid of thumbnails spanning the video — excellent for a quick visual overview.

### AI Video Analysis

**Gemini** (`gemini` MCP tool):
- Upload video for AI analysis of content
- Ask specific questions about what appears in the video
- Useful for: identifying objects, reading text in video, describing scenes, finding specific moments

### YouTube Video Analysis

**yt-dl tools:**
- `ytdlp_get_video_metadata` — Full metadata: upload date, channel info, description, tags, view count, duration
- `ytdlp_get_video_metadata_summary` — Concise overview
- `ytdlp_download_video` — Download video for local analysis
- `ytdlp_download_audio` — Audio only (for speech analysis)
- `ytdlp_download_transcript` — Auto-generated or manual captions
- `ytdlp_list_subtitle_languages` — Available subtitle languages
- `ytdlp_get_video_comments` — User comments (may contain witness info)
- `ytdlp_search_videos` — Search YouTube by query

**YouTube Metadata Intelligence:**
- **Upload date vs. event date** — Upload may be days/weeks after filming
- **Channel history** — Other uploads may provide context
- **Description** — Often contains location info, names, dates
- **Tags** — Reveal how the uploader categorized the video
- **Comments** — Viewers may identify locations, people, or provide context
- **View count trajectory** — Sudden spikes indicate when video went viral

### Frame-by-Frame Analysis

Key things to look for in individual frames:
- **Signs and text** — Readable only in specific frames as camera passes
- **Reflections** — Windows, mirrors, sunglasses may reveal the camera operator or surroundings
- **License plates** — Briefly visible as vehicles pass
- **Faces** — Identifiable in specific frames
- **Timestamps** — Security cameras or dashcams embed time
- **Screen content** — Computer/phone screens visible in frame
- **Shadow positions** — For time-of-day estimation (compare across video duration)

---

## Geolocation from Images

Cross-reference with `geolocation.md` for the full systematic approach.

### Quick Decision Tree

```
Does the image have EXIF GPS data?
  |
  YES --> extract_exif.py gps photo.jpg --> verify location matches visual content
  |
  NO --> Does reverse image search find a match?
          |
          YES --> Check original source for location metadata or description
          |
          NO --> Manual geolocation from visual clues:
                  1. Language on signs --> country/region
                  2. Road infrastructure --> narrow further
                  3. Vegetation/climate --> confirm region
                  4. Architecture --> city/area
                  5. Specific identifiers --> exact location
```

### Sun Position from Shadows

If you can identify the date (from context, EXIF date, or seasonal clues):
1. Measure shadow angle relative to objects
2. Use `sun_position.py` to calculate sun position for candidate locations
3. Match shadow direction with calculated sun azimuth
4. Shadow length + object height = sun elevation angle
5. Sun elevation at a given time uniquely identifies latitude

---

## Evidence Preservation

### Principles

1. **Save originals** — Never rely on screenshots alone; download the actual file
2. **Record provenance** — Note the exact URL, access date/time, and how you found it
3. **Calculate hashes** — SHA-256 hash of the original file proves integrity
4. **Archive web pages** — Use Internet Archive's "Save Page Now" (web.archive.org/save/)
5. **Capture context** — Screenshot the surrounding page, not just the image
6. **Chain of custody** — Document every step from discovery to analysis

### File Hash Calculation

```bash
# SHA-256 hash (recommended)
sha256sum photo.jpg

# MD5 hash (less secure but widely used)
md5sum photo.jpg
```

Record the hash immediately upon download, before any analysis or processing.

### Screenshot Best Practices

- Include the URL bar showing the source URL
- Include the full timestamp (browser or system clock visible)
- Use full-page screenshot tools for long pages
- Save as PNG (lossless) not JPEG (lossy compression)
- Consider screen recording for dynamic content (videos, stories, live streams)

### Web Page Archiving

**Internet Archive (Wayback Machine):**
- Save: `https://web.archive.org/save/{url}`
- This creates a permanent public archive
- Use for evidence preservation of web pages, social media posts, etc.

**Archive.today (archive.ph):**
- Alternative archival service
- Sometimes captures pages that Wayback Machine misses
- Creates a permanent snapshot

**Local Archiving:**
- Browser "Save As" (complete page with assets)
- wget or HTTrack for full site archival
- SingleFile browser extension for single-page archives
- Print to PDF for a visual record

### Evidence Documentation Template

For each piece of evidence, record:

```
Evidence ID: [sequential number]
Type: [image/video/webpage/document]
Source URL: [full URL]
Access Date: [YYYY-MM-DD HH:MM:SS UTC]
Download Date: [YYYY-MM-DD HH:MM:SS UTC]
File Name: [original filename]
File Size: [bytes]
SHA-256: [hash]
MD5: [hash]
Archive URL: [Wayback Machine or archive.ph link]
Description: [Brief description of what the evidence shows]
Relevance: [How this connects to the investigation]
```

---

## Common Analysis Workflows

### Workflow: Unknown Image Analysis

1. **Extract EXIF** — `extract_exif.py photo.jpg` (get GPS, camera, date)
2. **Reverse image search** — Google Lens, Yandex, TinEye (find source/context)
3. **Check for manipulation** — ELA, metadata consistency, visual analysis
4. **Geolocation** — From EXIF GPS or visual clues (see `geolocation.md`)
5. **Temporal analysis** — Date from EXIF, shadows, seasonal vegetation, events visible
6. **Document findings** — Hash, archive, record analysis results

### Workflow: Verify an Image Claim

Someone claims "this photo shows X at Y on Z date":
1. Reverse image search — is this actually an old/reused photo?
2. EXIF analysis — does metadata match claimed date/location/camera?
3. Visual verification — does weather match historical records for Y on Z?
4. Shadow analysis — does sun position match claimed time and location?
5. Manipulation check — has the image been edited?
6. Context check — do other photos from the same event corroborate?

### Workflow: Video Event Analysis

1. **Get metadata** — `get_video_info` for technical details
2. **Visual overview** — `generate_thumbnail_grid` to scan content
3. **Key frames** — `extract_frame_at_timestamp` for moments of interest
4. **AI analysis** — Gemini for content description and object identification
5. **Geolocation** — Apply `geolocation.md` techniques to key frames
6. **Audio analysis** — Language, background sounds, music (use extracted audio)
7. **Cross-reference** — Find other recordings of the same event from different angles

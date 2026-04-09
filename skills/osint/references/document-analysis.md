# Document Forensics for OSINT

Techniques for extracting intelligence from documents, emails, and embedded data. Covers PDF metadata, Office documents, email headers, steganography, and redaction failures.

---

## PDF Metadata Analysis

### Extraction Tools

| Tool | Method | Notes |
|------|--------|-------|
| **exiftool** (external) | `exiftool document.pdf` | Most comprehensive; extracts all metadata fields including XMP, IPTC |
| **`extract_exif.py`** (plugin) | `uv run skills/osint/scripts/extract_exif.py document.pdf` | Works on some PDFs; primarily designed for images but reads basic PDF metadata |
| **pdfinfo** (external) | `pdfinfo document.pdf` | Part of poppler-utils; quick summary of key fields |
| **Online analyzers** | PDF Examiner, PDFiD, VirusTotal | Useful when you cannot install tools; also check for malicious content |

### Key PDF Metadata Fields

| Field | Intelligence Value |
|-------|-------------------|
| **Author** | Name of the person who created the document (often a real name from the OS user account) |
| **Creator** | Application that created the original content (e.g., "Microsoft Word", "LaTeX") |
| **Producer** | Application that converted it to PDF (e.g., "Adobe PDF Library 15.0", "LibreOffice 7.4") |
| **CreationDate** | When the PDF was originally created |
| **ModDate** | When the PDF was last modified |
| **Title** | Document title (sometimes auto-populated from the first heading) |
| **Subject** | Document subject or description |
| **Keywords** | Author-specified keywords |
| **Trapped** | Print production status (rarely useful for OSINT) |

### What PDF Metadata Reveals

**Software Identification:**
The Creator and Producer fields reveal the authoring software, which can indicate the operating system, organization type, or individual habits:

| Creator / Producer Value | Indicates |
|--------------------------|-----------|
| `Microsoft Word 2019` / `Microsoft: Print To PDF` | Windows, Microsoft Office |
| `Microsoft Word for Microsoft 365` | Office 365 subscription (likely corporate) |
| `Microsoft Word 14.0` | Word 2010 (older installation) |
| `LibreOffice 7.x` | Open-source office suite (common in Linux, academia, budget-conscious orgs) |
| `Adobe InDesign CC` / `Adobe PDF Library` | Professional publishing workflow |
| `LaTeX with hyperref` / `pdfTeX` | Academic or technical author |
| `Google Docs` / `Google` | Google Workspace user |
| `wkhtmltopdf` / `WeasyPrint` | Programmatically generated (web-to-PDF) |
| `Prince` | XML-to-PDF (often automated reports) |
| `Quartz PDFContext` | macOS (generated via Print to PDF on Mac) |
| `Cairo` | Linux (GTK/GNOME printing) |
| `Skia/PDF` | Chrome browser "Save as PDF" |

**Author Identity:**
- The Author field is often auto-populated from the OS username or application registration
- May contain a full name, username, initials, or organization name
- Corporate documents sometimes have the company name instead of a person
- Compare Author across multiple documents from the same source for consistency

**Temporal Analysis:**
- CreationDate and ModDate reveal the document timeline
- Large gap between CreationDate and ModDate = significant revisions
- CreationDate earlier than expected = document may be recycled from a template
- Timezone offset in dates can indicate the author's location

### PDF/A Metadata Differences

PDF/A (archival format) embeds metadata differently:
- Uses XMP (Extensible Metadata Platform) as the primary metadata container
- XMP is stored as XML within the PDF, making it more structured and extensible
- May contain additional fields: `dc:creator`, `dc:description`, `dc:rights`, `xmp:CreateDate`
- PDF/A conformance level (1a, 1b, 2a, 2b, 3a, 3b) indicates the standard used
- Government and legal documents are often PDF/A — metadata may be more carefully curated

### Embedded Fonts

Fonts embedded in a PDF can reveal:
- **System locale / language:** A PDF created in Japan may embed Japanese fonts (MS Gothic, Yu Gothic); a Russian system may embed Cyrillic fonts
- **Operating system:** Calibri, Segoe UI = Windows; San Francisco, Helvetica Neue = macOS; DejaVu, Liberation = Linux
- **Font licensing:** Certain commercial fonts indicate specific software or organizational licensing
- **Mixed fonts:** May indicate copy-pasting from multiple sources

Check embedded fonts with:
```
pdffonts document.pdf        # Part of poppler-utils
exiftool -FontName document.pdf
```

### JavaScript in PDFs

PDFs can contain embedded JavaScript, which is a significant malware indicator:

**Detection:**
```
# Using pdfid (Didier Stevens tool)
pdfid document.pdf
# Look for: /JS, /JavaScript, /OpenAction, /AA (Additional Actions)

# Using pdf-parser
pdf-parser --search javascript document.pdf
```

**Red flags:**
- `/JS` or `/JavaScript` objects present in a document that should not need interactivity
- `/OpenAction` combined with JavaScript = runs code when the PDF is opened
- `/AA` (Additional Actions) = triggers on specific events
- `/Launch` = attempts to run external applications
- Obfuscated JavaScript (hex encoding, string concatenation, eval)

**OSINT relevance:** If you receive a suspicious PDF, analyze it in a sandbox before opening. VirusTotal can scan PDFs for known malicious patterns.

### PDF Structure Analysis

PDFs are built from objects, streams, and cross-reference tables. Deeper analysis can reveal:

- **Embedded files:** PDFs can contain attached files (other PDFs, images, executables) — check `/EmbeddedFiles` in the catalog
- **Incremental saves:** Each save appends to the PDF rather than rewriting it. Earlier versions of the document may be recoverable from the file
- **Deleted content:** Text or images removed in later revisions may still exist in earlier object versions
- **Form data:** Interactive PDF forms may contain submitted data in `/AcroForm` objects
- **Hidden layers:** Optional Content Groups (OCGs) can contain layers that are not visible by default but still present in the file

**Tools for deep PDF analysis:**
- `pdf-parser` (Didier Stevens) — Parse individual objects and streams
- `pdfid` (Didier Stevens) — Quick triage of suspicious PDFs
- `QPDF` — Linearize, decrypt, and inspect PDF structure
- `Caradoc` — PDF structure validation

---

## Microsoft Office Documents

### Archive Structure

Modern Office formats (.docx, .xlsx, .pptx) are ZIP archives. You can extract and inspect their contents directly:

```bash
# Rename to .zip and extract, or use unzip directly
unzip document.docx -d document_extracted/
```

**Key files inside the archive:**

| Path | Contents |
|------|----------|
| `docProps/core.xml` | Dublin Core metadata: creator, lastModifiedBy, created, modified, revision, subject, description, keywords |
| `docProps/app.xml` | Application metadata: application name/version, company, total editing time, page/word counts, template |
| `docProps/custom.xml` | Custom properties (organization-specific fields, classification labels) |
| `word/document.xml` | Actual document content (for .docx) |
| `word/comments.xml` | All comments with author names and dates |
| `word/media/` | Embedded images (may retain original EXIF data) |
| `[Content_Types].xml` | MIME types for all parts — reveals what content types are present |

### Key Metadata Fields

| Field | Location | Intelligence Value |
|-------|----------|-------------------|
| **creator** | `core.xml` | Person who created the document (from OS account or Office registration) |
| **lastModifiedBy** | `core.xml` | Last person to edit (may differ from creator) |
| **created** | `core.xml` | Creation timestamp with timezone |
| **modified** | `core.xml` | Last modification timestamp |
| **revision** | `core.xml` | Number of times the document has been saved (high count = heavily edited) |
| **category** | `core.xml` | Document category (sometimes used for internal classification) |
| **Application** | `app.xml` | e.g., "Microsoft Office Word", "LibreOffice" |
| **AppVersion** | `app.xml` | Application version number (e.g., "16.0000" = Office 2016/2019/365) |
| **Company** | `app.xml` | Organization name (from Office installation or Group Policy) |
| **Template** | `app.xml` | Template used — may reveal internal template names or paths |
| **TotalTime** | `app.xml` | Total editing time in minutes |
| **Pages / Words / Characters** | `app.xml` | Document statistics |

### Track Changes and Revision History

Track changes is an extremely valuable OSINT source. When enabled but not properly accepted/rejected:

- **Deleted content is preserved** in the document XML, marked with `<w:del>` tags
- **Inserted content** is marked with `<w:ins>` tags
- **Each change records:** the author name, date, and the content changed
- **Moved content** shows where text was relocated from and to

**Extraction:**
1. Open the .docx in Word and enable "All Markup" view
2. Or parse `word/document.xml` directly and search for `<w:del>`, `<w:ins>`, `<w:rPrChange>` elements
3. Track changes may reveal: original authors, editing timeline, removed sensitive content, organizational edits

**OSINT gold:** Organizations sometimes distribute documents with track changes still embedded, exposing internal revisions, deleted paragraphs, and the names of every person who edited the document.

### Comments

Comments in Office documents contain:
- **Author name** of each commenter
- **Date** of each comment
- **Content** of the comment (may contain instructions, feedback, internal discussion)
- **Reply chains** between multiple reviewers

Extract from `word/comments.xml` or view in the application.

### Embedded Images

Images inside Office documents (in the `word/media/`, `ppt/media/`, or `xl/media/` directories) may retain their original EXIF data:

```bash
unzip document.docx -d extracted/
uv run skills/osint/scripts/extract_exif.py extracted/word/media/image1.jpeg
```

This can reveal GPS coordinates, camera information, timestamps, and other metadata from the original photographs even when the document itself appears clean.

### Legacy Formats (.doc, .xls, .ppt)

Older binary Office formats (pre-2007) use the OLE2 (Compound Document) format instead of ZIP:

**Extraction tools:**
- `olemeta` (part of oletools) — Extract metadata from OLE files
- `oleid` — Identify OLE characteristics
- `olevba` — Extract VBA macros (malware detection)
- `exiftool` — Also reads OLE metadata

**Key differences:**
- Metadata is stored in OLE property streams, not XML files
- VBA macros are more commonly embedded in legacy formats
- Summary Information and Document Summary Information streams contain metadata
- Legacy formats may contain more metadata fields that were stripped in newer format conversions

---

## Email Header Analysis

### Plugin Tool: `analyze_email_headers.py`

```
uv run skills/osint/scripts/analyze_email_headers.py /path/to/headers.txt
```

Save the raw email headers to a text file first. In most email clients:
- **Gmail:** Open message > three dots menu > "Show original"
- **Outlook:** Open message > File > Properties > Internet Headers
- **Thunderbird:** View > Message Source (Ctrl+U)
- **Apple Mail:** View > Message > All Headers

### Key Headers for OSINT

| Header | Intelligence Value |
|--------|-------------------|
| **From** | Claimed sender address (can be spoofed) |
| **Reply-To** | Where replies go (if different from From, may indicate phishing) |
| **Return-Path** | Envelope sender (set by sending server; harder to spoof than From) |
| **Received** | Chain of servers the email passed through (read bottom to top) |
| **Message-ID** | Unique identifier; domain part often reveals the originating mail system |
| **Date** | When the email was sent (from sender's system; can be forged) |
| **X-Mailer / User-Agent** | Email client used (e.g., "Thunderbird 102.0", "Microsoft Outlook 16.0") |
| **X-Originating-IP** | IP address of the sender's machine (if present; added by some mail servers) |
| **Authentication-Results** | SPF, DKIM, and DMARC verification results from the receiving server |
| **DKIM-Signature** | Cryptographic signature proving the email content was not altered in transit |

### Received Chain Analysis

The Received headers trace the path of an email from sender to recipient. Read them **bottom to top** (the bottom-most Received header was added first by the originating server).

```
Received: from mail-out.example.com (mail-out.example.com [203.0.113.50])
        by mx.recipient.com (Postfix) with ESMTPS id ABC123
        for <user@recipient.com>; Thu, 10 Apr 2025 09:15:00 -0400

Received: from internal-mail.example.com (internal-mail.local [10.0.1.25])
        by mail-out.example.com (Postfix) with ESMTP id DEF456
        for <user@recipient.com>; Thu, 10 Apr 2025 09:14:58 -0400

Received: from [192.168.1.105] (unknown [198.51.100.75])
        by internal-mail.example.com (Postfix) with ESMTPSA id GHI789
        for <user@recipient.com>; Thu, 10 Apr 2025 09:14:55 -0400
```

**Analysis of this example (bottom to top):**
1. The sender's machine (IP 198.51.100.75, local IP 192.168.1.105) submitted the email to `internal-mail.example.com` via authenticated SMTP (ESMTPSA)
2. Internal server relayed to `mail-out.example.com` (showing internal infrastructure at 10.0.1.25)
3. Outbound server delivered to the recipient's MX at `mx.recipient.com`

**What each hop reveals:**
- Server hostnames and IP addresses (internal and external infrastructure)
- Internal IP ranges (RFC 1918 addresses like 10.x, 192.168.x reveal private network topology)
- Timestamps at each hop (can detect delays or timezone inconsistencies)
- Software used at each hop (Postfix, Exchange, Sendmail, etc.)
- Whether encryption was used (ESMTPS = TLS, ESMTP = unencrypted)

### SPF / DKIM / DMARC Authentication

Check the `Authentication-Results` header for spoofing indicators:

```
Authentication-Results: mx.recipient.com;
       spf=pass (sender IP is 203.0.113.50) smtp.mailfrom=example.com;
       dkim=pass (2048-bit key; secure) header.d=example.com;
       dmarc=pass (p=REJECT) header.from=example.com
```

| Result | Meaning |
|--------|---------|
| **SPF pass** | Sending IP is authorized by the domain's SPF record |
| **SPF fail** | Sending IP is NOT authorized — possible spoofing |
| **DKIM pass** | Email content cryptographically verified — not altered in transit |
| **DKIM fail** | Signature invalid — content was altered or signature forged |
| **DMARC pass** | Both SPF and DKIM align with the From domain |
| **DMARC fail** | Authentication failed — high likelihood of spoofing |

### Originating IP Geolocation

If you can identify the sender's originating IP (from `X-Originating-IP` or the first Received header):

1. Geolocate the IP using `ipinfo.io/{ip}` or similar geolocation services
2. Check the IP against `query_shodan_internetdb.py` for additional context
3. Determine if it is a residential ISP, VPN, hosting provider, or corporate network
4. Cross-reference with the claimed sender location

### X-Headers

Headers prefixed with `X-` are non-standard and often reveal internal infrastructure:

| X-Header | Reveals |
|----------|---------|
| `X-Originating-IP` | Sender's IP address (added by Outlook.com, some corporate servers) |
| `X-Mailer` | Email client software and version |
| `X-MS-Exchange-Organization-*` | Microsoft Exchange internal organization info |
| `X-MS-Has-Attach` | Whether attachments are present (Exchange) |
| `X-Google-DKIM-Signature` | Google's internal DKIM signing |
| `X-Gm-Message-State` | Gmail internal routing state |
| `X-Forefront-Antispam-Report` | Microsoft anti-spam analysis results |
| `X-Spam-Status` / `X-Spam-Score` | SpamAssassin or similar spam filter results |
| `X-Priority` | Message priority level |
| `X-Virus-Scanned` | Antivirus scanner used at a relay |

### Common Spoofing Indicators

Red flags that an email may be spoofed:
1. **From and Return-Path domains differ** — The display sender does not match the envelope sender
2. **SPF fail** — The sending IP is not authorized for the claimed domain
3. **DKIM fail or absent** — No cryptographic verification of the sender domain
4. **DMARC fail** — Overall authentication failure
5. **Received chain inconsistency** — The claimed sending domain does not appear in the Received headers
6. **Mismatched timezones** — Date header timezone does not match Received header timezones
7. **Reply-To differs from From** — Replies are directed to a different address (common in phishing)
8. **Generic or suspicious Message-ID domain** — The domain in the Message-ID does not match the From domain

---

## Steganography

### Overview

Steganography is the practice of hiding data within other files — typically images, audio, or video — so that the existence of the hidden data is not apparent. Unlike encryption (which makes data unreadable), steganography makes data invisible.

### Common Techniques

| Technique | Medium | Method |
|-----------|--------|--------|
| **LSB (Least Significant Bit)** | Images | Modifies the least significant bit of pixel color values to encode hidden data |
| **DCT coefficient modification** | JPEG images | Hides data in the discrete cosine transform coefficients during JPEG compression |
| **Palette manipulation** | PNG/GIF | Reorders or modifies the color palette to encode information |
| **Appended data** | Any file | Data appended after the end-of-file marker (file still opens normally) |
| **Metadata embedding** | Any file | Hidden data in metadata fields (EXIF comments, XMP, etc.) |
| **Audio LSB** | WAV/FLAC | Modifies least significant bits of audio samples |
| **Spread spectrum** | Audio | Spreads hidden signal across frequency spectrum |

### Detection Methods

**File Size Anomalies:**
- Compare file size to expected size for the image dimensions and format
- A 640x480 JPEG that is 15MB is suspicious (should be roughly 100-500KB)
- A BMP or PNG that is significantly larger than expected for its dimensions

**Statistical Analysis:**
- Chi-square test — detects non-random patterns in LSB distribution
- RS analysis — measures the relationship between regular and singular groups of pixels
- Sample pair analysis — statistical test for LSB embedding

**Visual Inspection:**
- Zoom to 100% or higher and look for visual noise patterns
- Compare color histograms — steganography can create unusual histogram shapes
- Apply filters (sharpening, contrast enhancement) to reveal artifacts

### Detection Tools

| Tool | What It Does | Best For |
|------|-------------|----------|
| **steghide** | Extract hidden data from JPEG/BMP/WAV/AU files | JPEG and audio stego; requires passphrase if encrypted |
| **zsteg** | Detect hidden data in PNG and BMP files | PNG LSB steganography; tries many encoding methods automatically |
| **stegsolve** | Visual analysis with color plane browsing and XOR | Manual visual inspection; browsing individual color bit planes |
| **binwalk** | Scan for embedded files within any binary file | Finding appended or embedded files (ZIP, RAR, images within images) |
| **exiftool** | Examine all metadata fields | Hidden data in metadata comments and fields |
| **strings** | Extract printable text from binary files | Quick check for plaintext hidden in binary data |
| **Stegdetect** | Automated stego detection for JPEGs | Statistical detection of JSteg, JPHide, OutGuess, F5 |

**Quick triage workflow:**
```bash
# 1. Check for appended data or embedded files
binwalk suspicious_image.png

# 2. Check metadata for hidden content
exiftool suspicious_image.png

# 3. Look for plaintext strings
strings suspicious_image.png | head -50

# 4. Try zsteg for PNG or stegsolve for visual analysis
zsteg suspicious_image.png

# 5. Try steghide with empty passphrase for JPEG
steghide extract -sf suspicious_image.jpg -p ""
```

### Common CTF Steganography Patterns

In Capture The Flag competitions (and sometimes in real investigations):
- Data hidden in the LSB of PNG images (use `zsteg`)
- ZIP archives appended to JPEG files (use `binwalk`)
- Passwords hidden in EXIF comment fields
- QR codes embedded in individual color channels (use `stegsolve`)
- Morse code or binary in image pixel patterns
- Audio spectrograms containing hidden images (open in Audacity, view spectrogram)
- Whitespace encoding (spaces and tabs encode binary data)
- Unicode zero-width characters in text documents

### When to Suspect Steganography in OSINT

- File size is disproportionately large for the apparent content
- An image or audio file is shared in an unusual context (e.g., sent as a file attachment when a link would suffice)
- Encrypted archives are embedded within seemingly innocent files
- Communication patterns suggest covert channels (regular exchange of image files between subjects)
- The investigation involves actors known to use steganographic techniques (some APT groups, illicit marketplaces)

---

## Document Redaction Failures

Improperly redacted documents are a significant OSINT source. Many organizations fail to properly remove sensitive information.

### Common Failure Types

**Black Bar Overlays in PDFs:**
The most common failure. A black rectangle is drawn over text, but the underlying text layer remains intact and selectable.

**How to check:**
1. Open the PDF and try to select/copy text under the black bars
2. Use `pdftotext document.pdf -` to extract all text — redacted text often appears in the output
3. Use `pdf-parser` to examine text objects beneath annotation layers
4. Copy-paste the entire page into a text editor

**Blurred or Pixelated Redaction:**
- Low-resolution pixelation (large blocks) can sometimes be reversed or narrowed down
- For text: if you know the font and size, you can generate all possible strings and compare the pixelated result
- For faces: pixelation with blocks larger than approximately 8x8 pixels may be partially reversible
- Gaussian blur at low radius is generally NOT reversible, but pattern matching may narrow possibilities

**Metadata Not Stripped After Redaction:**
- The document has visible redactions, but metadata (Author, Company, Track Changes) was not cleaned
- Use exiftool or the archive extraction method to check metadata after redactions are applied
- Look for mismatches: the "redacted" version still has the original author's name

**Track Changes Not Removed:**
- The document was "cleaned" but track changes were only hidden, not accepted/deleted
- Open in Word with "All Markup" enabled to reveal all revisions
- Or extract and examine `word/document.xml` for `<w:del>` and `<w:ins>` tags

**Image Redaction Failures:**
- Cropped images may retain the original dimensions in metadata
- Some image editors save the full original and simply change the crop viewport
- Transparent layers in PSD/TIFF files may hide "removed" content

### How to Check for Redaction Failures

**Systematic approach:**
1. **Text extraction:** Run `pdftotext` or copy all text — does hidden text appear?
2. **Metadata check:** Run exiftool — is metadata consistent with the redacted version?
3. **Archive extraction:** For .docx, unzip and check `document.xml` for tracked changes
4. **Layer analysis:** Open PDFs in a viewer that supports layer toggling
5. **Historical versions:** Search for the document title or content online — was an un-redacted version previously published?
6. **Thumbnail check:** EXIF thumbnails may contain a pre-redaction preview of the image

### Notable Real-World Redaction Failures

- **US Government documents:** Multiple instances of PDF overlay redactions where classified text was copy-pasteable
- **Legal filings:** Court documents with tracked changes revealing attorney work product
- **Corporate releases:** Press releases with metadata showing the original draft author at a competitor organization
- **Military reports:** Redacted location data recoverable from document metadata timezone fields

---

## Common Analysis Workflows

### Workflow: Unknown Document Analysis

1. **Identify format** — PDF, Office, legacy binary, or other
2. **Extract metadata** — Use appropriate tool (exiftool, archive extraction, olemeta)
3. **Analyze metadata** — Author, software, dates, company, revision history
4. **Check for hidden content** — Track changes, comments, embedded files, redaction failures
5. **Extract embedded media** — Images, attachments; analyze each for EXIF data
6. **Cross-reference findings** — Author name in other documents, software indicating OS/region, dates against timeline
7. **Document provenance** — Hash the file, record source URL and access date

### Workflow: Email Investigation

1. **Extract headers** — Save full headers from email client
2. **Run `analyze_email_headers.py`** — Parse headers for structured analysis
3. **Trace Received chain** — Map the path from sender to recipient (bottom to top)
4. **Check authentication** — SPF/DKIM/DMARC pass or fail
5. **Geolocate originating IP** — Identify sender location and network type
6. **Analyze X-headers** — Extract infrastructure details
7. **Compare From / Reply-To / Return-Path** — Check for spoofing indicators
8. **Check domain infrastructure** — Run `query_dns.py` and `query_whois.py` on the sender domain (see `domain-infrastructure.md`)

### Workflow: Batch Document Metadata Comparison

When you have multiple documents from the same source:
1. Extract metadata from all documents
2. Compare Author fields — identify all contributors
3. Compare Company fields — consistent or varying?
4. Compare software versions — consistent environment or mixed?
5. Build a timeline from CreationDate and ModDate fields
6. Look for template names or paths that reveal internal systems
7. Record all findings in the knowledge graph (see `knowledge-graph.md`)

---

## Cross-References

- `image-video-forensics.md` — EXIF extraction, image manipulation detection
- `domain-infrastructure.md` — Email infrastructure analysis, DNS records for sender verification
- `opsec-ethics.md` — Ethical guidelines for handling sensitive discovered content
- `tool-guide.md` — Full reference for `extract_exif.py`, `analyze_email_headers.py`, and other plugin tools
- `reporting.md` — How to document and present findings from document analysis

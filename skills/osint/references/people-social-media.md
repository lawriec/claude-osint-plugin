# People and Social Media Investigation

Techniques for investigating individuals and their online presence across social media platforms.

---

## Starting Points

Every people investigation begins with at least one seed identifier:

| Seed | First Steps |
|------|------------|
| **Full name** | Google search, LinkedIn, social media searches, public records |
| **Username/handle** | Cross-platform enumeration, `check_username.py`, Sherlock |
| **Email address** | Gravatar, HIBP, Holehe, Google dorking, breach databases |
| **Phone number** | Carrier lookup, reverse search, WhatsApp/Telegram lookup |
| **Photo/avatar** | Reverse image search (Yandex, Google Lens, TinEye, PimEyes) |
| **Physical address** | Property records, Google Maps/Street View, associated names |
| **Domain name** | WHOIS history, DNS records, website content, linked socials |

The goal is to expand from one identifier to many, building a complete picture of the subject's digital footprint.

---

## Username Enumeration

### Plugin Tool: `check_username.py`

Quick cross-platform username availability check:
```
python check_username.py <username>
```
Returns which major platforms have an account with that username.

### External Tools

**Sherlock** (github.com/sherlock-project/sherlock):
- Checks 400+ sites for username existence
- Fast, CLI-based, open source
- Install: `pip install sherlock-project`
- Usage: `sherlock username`
- Export to CSV/JSON for analysis

**Maigret** (github.com/soxoj/maigret):
- More advanced than Sherlock (500+ sites)
- Generates HTML reports with profile links
- Can extract additional info from found profiles
- Usage: `maigret username`

**WhatsMyName** (whatsmyname.app):
- Web-based username search
- Community-maintained site list
- Good for quick checks without installing tools

**Namechk** (namechk.com):
- Web-based, checks domains and social media
- Visual interface showing availability

### Manual Priority Checks

Always manually verify these high-value platforms, as automated tools may miss them or have false positives:

1. **GitHub** — github.com/{username} (contribution graph, repos, bio, email in commits)
2. **Twitter/X** — x.com/{username} (tweets, followers, following, lists)
3. **Instagram** — instagram.com/{username} (posts, tagged locations, followers)
4. **Reddit** — reddit.com/user/{username} (comment history, subreddits, karma)
5. **LinkedIn** — linkedin.com/in/{username} (professional history, connections)
6. **TikTok** — tiktok.com/@{username} (videos, bio links)
7. **Facebook** — facebook.com/{username} (profile, about, friends if public)
8. **Medium** — medium.com/@{username} (articles, topics, claps)
9. **Dev.to** — dev.to/{username} (developer articles, comments)
10. **YouTube** — youtube.com/@{username} (videos, playlists, about)
11. **Telegram** — t.me/{username} (profile, bio)
12. **Pinterest** — pinterest.com/{username} (pins, boards)
13. **Twitch** — twitch.tv/{username} (streams, clips, about)
14. **Mastodon** — Search across instances
15. **Bluesky** — bsky.app/profile/{username}.bsky.social
16. **Steam** — steamcommunity.com/id/{username} (games, activity, friends)
17. **Keybase** — keybase.io/{username} (verified identities, PGP keys)

---

## Profile Correlation

Finding the same person across platforms:

**Strong Indicators (high confidence):**
- Identical username + similar profile photo
- Linked accounts in bio ("also on Twitter @...")
- Same unique phrases in bio text
- Cross-posted content (same photo/text on multiple platforms)
- Verified identity claims (Keybase, personal website)

**Moderate Indicators (needs corroboration):**
- Same username, different content style
- Similar but not identical profile photos
- Overlapping interests/topics
- Similar follower/following networks

**Weak Indicators (could be coincidence):**
- Common username (e.g., "john_doe") — verify with additional signals
- Same first name or initials
- Similar posting topics without other matches

**Timezone Estimation from Activity:**
1. Collect timestamps of posts/activity across platforms
2. Plot activity by hour of day
3. Identify quiet periods (likely sleeping: ~midnight to ~7am local)
4. The timezone where the quiet period maps to sleeping hours is likely their timezone
5. Multiple platforms strengthen the estimate

**Entity Enrichment via Wikidata:**
For public figures, use `uv run query_wikidata_sparql.py entity "<name>"` to get structured data (birth date, nationality, occupation, employer, education) from Wikidata. Follow up with `properties <QID>` for detailed attributes and `related <QID>` for connected entities.

---

## Google Dorking for People

### Name Searches
```
"john doe" site:linkedin.com
"john doe" site:facebook.com
"john doe" site:twitter.com
"john doe" site:github.com
"john doe" site:medium.com
"john doe" ("city name" OR "company name")
"john doe" filetype:pdf
```

### Username Searches
```
"@johndoe" -site:twitter.com
"johndoe" site:reddit.com
inurl:"johndoe" site:github.com
```

### LinkedIn-Specific (X-Ray Search)
```
site:linkedin.com/in/ "john doe"
site:linkedin.com/in/ "john doe" "company name"
site:linkedin.com/in/ "software engineer" "san francisco"
```

### Email Searches
```
"john.doe@gmail.com"
"john.doe@" site:github.com
"john.doe" "@gmail.com" site:pastebin.com
```

### Document and File Searches
```
"john doe" filetype:pdf site:example.com
"john doe" filetype:xlsx OR filetype:csv
"john doe" inurl:resume OR inurl:cv filetype:pdf
```

---

## Email Investigation

### Email to Identity Pipeline

```
email address
  |
  +---> Gravatar (gravatar.com) --> profile image, display name, linked accounts
  |
  +---> Have I Been Pwned (HIBP) --> breach list (shows which services they registered on)
  |
  +---> Holehe --> which platforms accept this email for login/registration
  |
  +---> Google search "email@example.com" --> public mentions, forum posts, leaked data
  |
  +---> Email domain --> WHOIS --> registrant info (if custom domain)
  |
  +---> Email format guess --> employer (john.doe@company.com)
```

### Gravatar Lookup
- Hash the email with MD5: `md5("email@example.com")`
- Check: `https://gravatar.com/avatar/{hash}?d=404`
- If exists, you get their profile image and possibly a profile page
- Profile may link to other accounts

### Have I Been Pwned (HIBP)
- haveibeenpwned.com — check if email appears in data breaches
- The *list of breaches* is itself intelligence (shows which services they used)
- Example: LinkedIn breach + Adobe breach + Dropbox breach = active online user since ~2012
- API available for programmatic checks

### Holehe (github.com/megadose/holehe)
- Tests email registration on 120+ websites
- Does NOT attempt login — only checks if email is registered
- Usage: `holehe email@example.com`
- Useful for discovering which platforms someone uses

### Email Header Analysis
- Reference `analyze_email_headers.py` for parsing
- Headers reveal: originating IP, mail servers in chain, timestamps, authentication results
- Originating IP can be geolocated (approximate sender location)
- SPF/DKIM/DMARC results show email authentication status

### Email Patterns
- Many companies use predictable formats: first.last, firstlast, first_last, f.last
- If you know someone works at a company, try common formats
- Tools like Hunter.io can reveal email patterns for a domain

---

## Phone Number Investigation

### Initial Analysis
1. **Country code** — immediately narrows to country (+1 = US/Canada, +44 = UK, +49 = Germany, etc.)
2. **Area/city code** — narrows to region within country
3. **Carrier prefix** — some countries allocate number blocks to carriers

### Lookup Methods
- **Search engines:** Search the number in quotes ("555-123-4567")
- **Reverse phone lookup:** Whitepages, TrueCaller, NumLookup, Sync.me
- **Carrier lookup APIs:** Twilio, Numverify — identify carrier and line type (mobile/landline/VoIP)
- **Social media:** Numbers may appear in profiles, posts, or be searchable directly
- **CallerID databases:** Various services maintain CallerID name (CNAM) records

### Messaging Platform Checks
- **WhatsApp:** Adding number to contacts reveals profile photo, status, last seen (if not hidden)
- **Telegram:** Search by phone number reveals username and profile
- **Signal:** Shows if number is registered
- **Viber:** Profile photo and status

### Ethical Considerations
- Phone numbers are personal data
- Do not call, text, or otherwise contact the subject
- Be aware of local laws regarding phone number lookups
- Some reverse lookup services share that someone searched a number

---

## Social Media Platform Specifics

### Twitter/X

**Search Operators:**
```
from:username                    — tweets from this user
to:username                      — tweets directed at this user
@username                        — mentions of this user
from:username since:2024-01-01   — tweets after a date
from:username until:2024-06-01   — tweets before a date
from:username filter:media       — only tweets with images/video
from:username filter:links       — only tweets with links
from:username min_faves:100      — tweets with 100+ likes
from:username lang:en            — tweets in English
"exact phrase" from:username     — exact phrase match
```

**Intelligence Value:**
- Posting times reveal timezone and daily schedule
- Geotagged tweets (less common now) reveal locations
- Follower/following network reveals associations
- Liked tweets reveal interests and opinions
- Lists they're on categorize them by others' perceptions
- Replies and quote tweets reveal relationships

**Archived Tweets:**
- Wayback Machine (web.archive.org) for deleted tweets
- Various Twitter archive services
- Google cache may have recent deletions
- Bing cache sometimes retains longer

### Facebook

**Search Techniques:**
- Direct URL: facebook.com/{username} or facebook.com/profile.php?id={numeric_id}
- Facebook's built-in search for people, posts, photos, videos
- Graph Search alternatives (original Graph Search deprecated):
  - Google dorking: `site:facebook.com "keyword"`
  - Facebook search URL parameters for filtered searches
- Check "About" section for personal details
- Friends list (if public) reveals social network
- Tagged photos may reveal locations and associates
- Life events (education, work, relationships) in timeline

**Privacy Settings Impact:**
- Many profiles are locked down — limited public info
- Profile picture and cover photo are usually public
- Name, profile URL, and some basic info often visible
- Cached/archived versions may show older, less restricted profiles

### Instagram

**Intelligence Value:**
- Photo/video content rich with geolocation clues
- Location tags on posts reveal places visited
- Tagged users reveal social connections
- Stories (24hr) may contain casual/unguarded content
- Highlights (saved stories) organized by theme
- Following/follower lists reveal interests and relationships
- Comment interactions reveal close associates
- Reels and IGTV for longer video content

**Analysis Tips:**
- Instagram stories are ephemeral — capture quickly
- Hashtags reveal community affiliations and interests
- Multiple accounts are common (personal + business/hobby)
- Instagram scraping tools: Instaloader, Instagram-Explorer

### LinkedIn

**X-Ray Search (via Google):**
```
site:linkedin.com/in/ "john doe" "company name"
site:linkedin.com/company/ "company name"
site:linkedin.com/in/ "skill" "location"
```

**Intelligence Value:**
- Employment history with dates
- Education with dates and degrees
- Skills and endorsements
- Recommendations (reveal colleagues and relationships)
- Publications, certifications, volunteer work
- Groups (reveal professional interests)
- Connections (second-degree reveals mutual contacts)

**Limitations:**
- LinkedIn actively blocks scraping
- Profile views are notified to the subject (use private mode, but it limits what you see)
- "People also viewed" suggestions can reveal related individuals
- Google cache and Wayback Machine for historical profiles

### Reddit

**User Investigation:**
- reddit.com/user/{username} — full post and comment history
- Sort by: new, hot, top (all time), controversial
- Subreddit activity patterns reveal interests, location, profession, demographics
- Users often share personal details incrementally across many posts
- Comment karma and account age indicate engagement level

**Advanced Techniques:**
- Reddit search: `author:username keyword`
- Third-party tools: Reddit Investigator, Redective, SnoopSnoo
- Deleted comments may be recovered via Pushshift (reveddit.com, unddit.com)
- Cross-reference subreddit activity with time-of-day for timezone
- Local subreddits (r/cityname) reveal likely location

### GitHub

**Intelligence Value:**
- Real name often in profile
- Email address discoverable in commit history:
  ```
  git log --format='%ae' | sort -u
  ```
  Or check: `https://api.github.com/users/{username}/events/public` for push events
- Contribution graph reveals activity patterns
- Starred repositories reveal interests and tech stack
- Organizations reveal affiliations
- Gists may contain personal scripts, notes, or snippets
- README profiles may have personal details, social links, location
- Repository topics and languages reveal skills

---

## Timeline Analysis

Building a chronological picture from social media activity:

### Activity Patterns
- **Posting frequency:** Daily, weekly, sporadic — indicates engagement level
- **Time-of-day patterns:** When they post most → timezone and daily routine
- **Platform preferences:** Primary platform usually gets most activity
- **Content types:** Text, photos, links, retweets — reveals communication style

### Life Events
- **Activity gaps:** Extended silence may indicate travel, hospitalization, incarceration, or life changes
- **Tone changes:** Sudden shifts in sentiment may correspond to personal events
- **Location shifts:** Different geotagged locations indicate moves or travel
- **Network changes:** New connections/followers from a different city may indicate relocation

### Corroborating Timelines
- Cross-reference activity across platforms
- Match posting times with known events (conferences, holidays, local events)
- Weather in photos can be cross-referenced with historical weather data
- Background details in photos may reveal location even without geotags

---

## Operational Security Notes

- **Do not create fake accounts** to interact with subjects
- **Do not send friend/follow requests** to subjects
- **Use logged-out/private browsing** to avoid revealing your identity via profile views
- **Do not contact subjects** or anyone in their network
- **Document everything** with timestamps and screenshots
- **Be aware of platform ToS** — many prohibit scraping
- Reference `opsec-ethics.md` for detailed ethical and legal guidelines

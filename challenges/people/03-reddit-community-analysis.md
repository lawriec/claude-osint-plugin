# Challenge: Reddit Community Intelligence

## Domain
People / Social Media (SOCMINT)

## Difficulty
Medium

## Scenario
"During an investigation into a data breach disclosure, we found a Reddit username 'osint_researcher_2024' that posted detailed write-ups in r/OSINT and r/netsec about vulnerability research. We need to build an intelligence profile from their public Reddit activity. What can we learn about this person -- their interests, expertise level, timezone, approximate location, and whether they've disclosed any personally identifiable information in their posts or comments?

Note for testing: If this exact username does not exist, demonstrate the full SOCMINT methodology using any active Reddit account found in r/OSINT or r/netsec, and explain what you would look for at each step."

## Expected Approach
1. **Cross-platform username search** -- `check_username.py osint_researcher_2024`:
   - Check if the same username exists on GitHub, Twitter, Mastodon, HackerNews, Keybase, and other platforms
   - Any matches indicate potential cross-platform correlation for the same person
   - `check_username.py osint_researcher_2024 --platforms github,twitter,reddit,mastodon_social,hackernews,keybase,gitlab,dev_to`
2. **Discover active threads in target subreddits** -- `discover_reddit_threads.py --subreddit OSINT --sort hot --limit 25 --with-comments`:
   - Search r/OSINT and r/netsec for threads to identify active community members
   - `discover_reddit_threads.py --subreddit netsec --sort hot --limit 25 --with-comments`
   - Look for posts or comments by the target username
3. **Fetch Reddit profile and history** -- Use Reddit MCP tools:
   - `fetch_reddit_post_content` on known post URLs to get full text
   - `fetch_reddit_hot_threads` from subreddits the target is active in
   - Analyze post and comment history for intelligence indicators
4. **Posting pattern and timezone analysis** -- Examine timestamps from all posts/comments:
   - Plot posting times across the day (UTC) to identify active hours
   - Identify gaps in posting (likely sleeping hours) to infer timezone
   - Example: If user never posts between 04:00-12:00 UTC, they likely sleep during those hours, suggesting UTC-5 to UTC-8 (North American time zones)
   - Check for weekend vs weekday posting patterns (may indicate profession)
5. **Interest and expertise profiling** -- Analyze content across subreddits:
   - Which subreddits they post in (beyond OSINT and netsec)
   - Technical depth of posts (beginner questions vs expert write-ups)
   - Tools, techniques, and frameworks they mention or recommend
   - Any professional context (references to work, certifications, conferences)
6. **PII and self-disclosure check** -- Review posts and comments for:
   - Real name, location, employer, or educational institution mentions
   - "I live in...", "I work at...", "When I was at [university]..." patterns
   - Photo posts that might contain location metadata
   - Links to personal websites, blogs, or portfolios
   - Conference talks or published research attributed to them
7. **Writing style and language analysis** -- Note:
   - Primary language and any non-English posts
   - Use of regional slang, spelling conventions (American vs British English)
   - Technical jargon that indicates specialization area
   - Writing formality (academic, professional, casual)
8. **Compile intelligence profile** -- Structure findings into:
   - Confirmed facts (directly stated by the user)
   - Inferred attributes (derived from behavioral patterns)
   - Possible connections (cross-platform correlations)
   - Confidence levels for each finding

## Verification
- [ ] Checked for the username across multiple platforms using check_username.py
- [ ] Searched target subreddits for the user's activity
- [ ] Analyzed posting timestamps to infer timezone
- [ ] Identified interests and expertise level from post content
- [ ] Checked for self-disclosed PII in posts and comments
- [ ] Noted writing style indicators (language, regional markers)
- [ ] Produced a structured intelligence profile with confidence levels
- [ ] Maintained ethical boundaries (public information only, no doxing)

## Ground Truth

<details>
<summary>Click to reveal</summary>

This challenge tests SOCMINT methodology rather than a specific answer. The agent should demonstrate:

1. **Cross-platform correlation:**
   - Use check_username.py to search 10+ platforms for the same username
   - Matching usernames across platforms is a strong (but not definitive) correlation
   - Identical usernames on GitHub + Reddit + HackerNews for a technical user is a high-confidence match
   - Different usernames could still be the same person (check profile bios for cross-links)

2. **Timezone inference methodology:**
   - Collect timestamps from 20+ posts/comments
   - Convert all to UTC
   - Identify the longest daily gap in activity (sleeping hours)
   - Sleeping gap of 04:00-12:00 UTC suggests US Eastern to Pacific time
   - Sleeping gap of 22:00-06:00 UTC suggests European timezone
   - Weekend activity patterns can suggest student vs professional

3. **Content analysis indicators:**
   - Subreddit diversity reveals breadth of interests
   - Post depth reveals expertise (asking vs answering, basic vs advanced topics)
   - Tool recommendations suggest hands-on experience
   - Conference or publication mentions indicate professional involvement
   - Job-seeking posts or career questions reveal career stage

4. **PII discovery (common Reddit self-disclosures):**
   - City/state mentioned in local subreddits (r/[cityname])
   - University mentioned in r/college or r/cscareerquestions
   - Employer mentioned in job-related discussions
   - Age or life stage from r/personalfinance or similar
   - Photos in post history with EXIF or identifiable locations

5. **Ethical boundaries:**
   - Only analyze publicly available information
   - Do not attempt to de-anonymize through private messages
   - Do not correlate with leaked databases
   - Note that Reddit accounts may not represent real identities
   - Flag any findings that could enable harassment if shared

**Scoring:**
- **Score 5 if:** Agent runs cross-platform username search, analyzes Reddit activity (posting times, subreddits, content depth), attempts timezone inference, checks for PII disclosure, and produces a structured profile with confidence levels and ethical caveats
- **Score 4 if:** Agent covers 4+ methodology areas and produces a useful intelligence profile, but may miss timezone analysis or cross-platform search
- **Score 3 if:** Agent checks Reddit activity and identifies interests, but doesn't systematically analyze timestamps or check cross-platform presence
- **Score 2 if:** Agent only describes what to look for without executing any tools or producing structured findings
- **Score 1 if:** Agent doesn't use available tools or only provides a surface-level summary

</details>

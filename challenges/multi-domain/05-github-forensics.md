# Challenge: GitHub Contributor Forensics

## Domain
Multi-domain (People + Infrastructure)

## Difficulty
Medium

## Scenario
"We're hiring for a senior backend engineer role. One of the top candidates claims on their resume that they are a core contributor to the open-source project 'fastapi' (tiangolo/fastapi) and have been actively contributing since 2020. They provided their GitHub username as 'devops-sarah-k'. Can you verify these claims? Specifically:

1. Does the GitHub account 'devops-sarah-k' exist and look legitimate?
2. Do their contributions to fastapi match what they claim?
3. What email addresses are associated with their commits, and what can we learn from those?
4. Are there other accounts or platforms linked to this identity?

We need to make a hiring decision and want to ensure the candidate's open-source credentials are genuine."

## Expected Approach
1. **Verify GitHub account existence** -- Use fetch MCP (`mcp__fetch__fetch`) to query the GitHub API:
   - Fetch `https://api.github.com/users/devops-sarah-k` to check if the account exists
   - If it exists, examine: account creation date, public repo count, follower/following ratio, bio, blog URL, company field, and location
   - Check whether the account age and activity level are consistent with claims of contributing since 2020
2. **Examine contribution history** -- Fetch the user's public events and repository activity:
   - Fetch `https://api.github.com/users/devops-sarah-k/repos?sort=updated` to see their repositories
   - Check for forks of fastapi or related projects
   - Look at repository descriptions, languages used, and star counts
   - Use Tavily (`mcp__tavily__tavily_search`) to search for `"devops-sarah-k" site:github.com` for public mentions
3. **Check fastapi contribution records** -- Search for the username in the fastapi project:
   - Use Tavily to search `"devops-sarah-k" site:github.com/tiangolo/fastapi` for PRs, issues, and commits
   - Fetch `https://api.github.com/repos/tiangolo/fastapi/commits?author=devops-sarah-k` to find commits by this user
   - Check the fastapi contributors page or CONTRIBUTORS file for the username
   - Examine the nature of contributions: are they code, documentation, or issue comments?
4. **Extract commit email addresses** -- Analyze commits for associated email data:
   - For any found commits, append `.patch` to the commit URL to see the raw patch with author email
   - Alternatively, fetch `https://api.github.com/users/devops-sarah-k/events/public` to find push events with commit details
   - Note all email addresses associated with the account (GitHub noreply, personal, corporate)
5. **Investigate discovered email domains** -- `query_dns.py all <domain>` for each email domain:
   - Check MX records to verify the email domain is operational
   - Run `query_whois.py lookup <domain>` to check domain registration details
   - Determine whether the email domain belongs to a company, personal domain, or free provider
6. **Cross-platform username check** -- `check_username.py devops-sarah-k`:
   - Check if the same username exists on other platforms (LinkedIn, Twitter/X, Stack Overflow, etc.)
   - Look for consistent identity signals: same avatar, bio, location, or linked accounts
   - Inconsistencies across platforms (different people using the same handle) may indicate the username is not unique to this candidate
7. **Timeline and pattern analysis** -- Synthesize all findings:
   - Map the contribution timeline: when did activity start and how frequent is it?
   - Compare claimed contribution period (since 2020) with actual evidence
   - Assess whether the account shows organic growth patterns or appears manufactured
   - Look for gaps in activity that may indicate account dormancy or purchase

## Verification
- [ ] GitHub API queried for account existence and profile metadata
- [ ] Contribution history to fastapi specifically investigated
- [ ] Commit email addresses extracted and analyzed
- [ ] Email domain DNS/WHOIS checked for at least one discovered domain
- [ ] Username checked across multiple platforms with check_username.py
- [ ] Contribution timeline assessed against candidate's claims
- [ ] Account authenticity indicators evaluated (age, activity patterns, follower ratio)
- [ ] Structured verification report produced with confidence levels

## Ground Truth

<details>
<summary>Click to reveal</summary>

**This challenge uses a fictitious username.** The account `devops-sarah-k` almost certainly does not exist on GitHub, and that is a valid and important finding. The agent should discover this early and report it as a significant red flag.

**Expected investigation flow:**

1. **Account check:** The GitHub API call to `https://api.github.com/users/devops-sarah-k` should return a 404 (Not Found). This is the single most important finding -- the candidate provided a username that does not exist.

2. **If the account does not exist, the agent should:**
   - Explicitly state that the claimed GitHub account cannot be found
   - Consider that the username may be misspelled or the account may have been renamed/deleted
   - Search for variations or similar usernames as a good-faith effort
   - Check whether any contributions to fastapi exist under similar handles
   - Flag this as a major discrepancy requiring clarification from the candidate

3. **fastapi contribution analysis:** The fastapi project (tiangolo/fastapi) is a real, well-known Python framework. The agent should demonstrate awareness that:
   - fastapi has a large contributor base, making false claims plausible-sounding
   - The project's contributor list is publicly auditable via GitHub API
   - "Core contributor" vs "occasional contributor" is a meaningful distinction

4. **Cross-platform check:** Running `check_username.py devops-sarah-k` will reveal whether this identity exists elsewhere. If the username is not found on any major platform, it further undermines the candidate's claims.

5. **Methodology demonstration:** Even when the primary account does not exist, a thorough investigator should:
   - Document the negative finding clearly
   - Explore alternative explanations (typo, renamed account, different platform)
   - Use the email domain investigation path if any email was provided
   - Provide a risk assessment for the hiring decision

**Scoring:**
- **Score 5 if:** Agent queries the GitHub API, discovers the account does not exist, checks fastapi contributors independently, runs cross-platform username checks, explores alternative explanations, and produces a structured risk assessment with the non-existent account as the primary red flag
- **Score 4 if:** Agent discovers the account does not exist, checks at least one other verification path (cross-platform or fastapi contributors), and provides a clear assessment
- **Score 3 if:** Agent discovers the account does not exist and reports it, but does not pursue additional verification paths or alternative explanations
- **Score 2 if:** Agent attempts to query the GitHub API but does not clearly interpret or report the negative finding
- **Score 1 if:** Agent does not query the GitHub API or relies solely on web search without checking the actual account existence

</details>

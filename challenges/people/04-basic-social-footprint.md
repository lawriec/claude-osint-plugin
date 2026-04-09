# Challenge: Social Media Footprint Discovery

## Domain
People / Social Media

## Difficulty
Easy

## Scenario
"I have the username `nasa`. I want to know which major social media platforms have an account with this exact username. Can you check and tell me which ones exist?"

## Expected Approach
1. **Username enumeration** — `check_username.py nasa` to check existence across supported platforms
2. **Review results** — Note which platforms report the account as existing vs. not found
3. **Document findings** — For each found account, record the platform name and profile URL

## Verification
- The `check_username.py` script should be run with the username `nasa`
- Results should identify accounts on major platforms (GitHub, Twitter/X, Instagram, Reddit, etc.)
- Found accounts should include profile URLs
- The agent should note that NASA is a well-known organization with official verified accounts on most major platforms

## Ground Truth

<details>
<summary>Click to reveal</summary>

Key facts (may change over time — verify current state):
- **GitHub:** `nasa` — NASA's official GitHub organization with open-source projects
- **Reddit:** `nasa` — NASA's official Reddit presence
- **Twitter/X:** `nasa` — NASA's official and highly followed account
- **Instagram:** `nasa` — NASA's official account, one of the most followed on the platform
- **YouTube:** NASA maintains an official YouTube channel
- NASA has official accounts on most major social media platforms as part of their public outreach mission
- **Key insight:** A username held by a major government agency will exist on nearly all major platforms — the script provides a quick systematic check rather than manual platform-by-platform browsing

### Scoring Rubric
| Score | Criteria |
|-------|----------|
| 5 | `check_username.py` run successfully, results interpreted correctly, multiple platform accounts identified with URLs |
| 4 | Script run successfully with correct interpretation but missing some platform details |
| 3 | Manual search used instead of the script, but correct platforms identified |
| 2 | Partial results — some platforms checked but incomplete or unsystematic approach |
| 1 | No systematic check performed, no script usage, or incorrect results |

</details>

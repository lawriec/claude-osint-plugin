# Challenge: Username Correlation

## Domain
People / Social Media

## Difficulty
Easy

## Scenario
"I found the username `torvalds` online. Can you check what platforms this username exists on and determine if they're likely the same person across platforms?"

## Expected Approach
1. **Username check** — `check_username.py torvalds` for cross-platform existence
2. **GitHub API** — Check GitHub profile for `torvalds` (public, well-known)
3. **Cross-reference** — Compare profile information across platforms
4. **Knowledge graph** — Track the discovered accounts and their relationships

## Verification
- GitHub `torvalds` is Linus Torvalds (Linux creator) — this is verifiable public knowledge
- The agent should identify the GitHub account and note it has millions of followers
- Other platforms may or may not have the same person

## Ground Truth

<details>
<summary>Click to reveal</summary>

- **GitHub:** `torvalds` — Linus Torvalds, creator of Linux and Git. Verified by: massive follower count, Linux kernel repository, well-documented public figure
- **Reddit:** `torvalds` may or may not exist as the real person
- **Twitter/X:** Linus Torvalds is not known to be active on Twitter
- **Key insight:** The agent should:
  1. Identify the GitHub account as highly likely to be the real Linus Torvalds
  2. Note that username matches alone don't prove same person
  3. Look for corroborating evidence (bio, linked accounts, posting content)
  4. Rate confidence: GitHub = Confirmed (public figure), other platforms = Possible/Speculative without corroboration

</details>

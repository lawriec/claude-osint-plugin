# OPSEC and Ethics Reference

Critical guidelines for conducting OSINT investigations ethically, legally, and securely. This reference must be consulted before and during every investigation.

---

## Ethical Guidelines

### Core Principles

1. **Only use publicly available information.** If data requires unauthorized access, deception, or exploiting vulnerabilities to obtain, it is off-limits.

2. **Never log into accounts you do not own.** Even if credentials are found in public breach data, using them is unauthorized access.

3. **Never social engineer targets.** Do not create fake profiles to befriend subjects, do not send deceptive messages, do not impersonate anyone.

4. **Consider the impact on the subject.** Every investigation has a human subject. Ask: could this investigation cause harm if the findings were misused?

5. **Minimize data collection.** Collect only what is necessary to answer the intelligence requirement. Do not vacuum up all available data because you can.

6. **Do not deanonymize people who have chosen anonymity** unless there is a compelling public interest reason (e.g., the person is committing fraud or posing a safety threat).

### Bellingcat Ethical Framework

Bellingcat, a leading OSINT organization, operates under these principles:

| Principle | Application |
|-----------|------------|
| Minimize harm | Redact PII from published findings unless directly relevant |
| Serve public interest | Investigation should benefit the public, not satisfy curiosity |
| Accuracy over speed | Verify before reporting; wrong information causes harm |
| Transparency of method | Document how findings were obtained so they can be scrutinized |
| Proportionality | Depth of investigation should match seriousness of the matter |

### Trace Labs Guidelines (Missing Persons OSINT)

For investigations involving missing or vulnerable persons:

- Submit findings only through proper channels (law enforcement, Trace Labs platform)
- Do not contact the missing person directly if found
- Do not publicize findings on social media
- Do not investigate minors without explicit authorization
- Focus on factual leads, not speculation
- Time is critical — prioritize actionable intelligence

### Ethical Decision Framework

When uncertain about an action, apply this test:

```
1. Is this information publicly available without deception?    YES -> Continue
                                                                 NO -> STOP

2. Am I collecting only what's needed for the requirement?      YES -> Continue
                                                                 NO -> Narrow scope

3. Could this action cause disproportionate harm to the subject? NO -> Continue
                                                                 YES -> STOP and reassess

4. Would I be comfortable if my methodology were made public?   YES -> Continue
                                                                 NO -> STOP and find another way

5. Is there a legitimate purpose for this investigation?        YES -> Continue
                                                                 NO -> STOP
```

---

## Legal Boundaries

### Key Legislation

#### CFAA — Computer Fraud and Abuse Act (United States)

| Provision | Implication for OSINT |
|-----------|----------------------|
| Unauthorized access to computers | Never bypass authentication or access controls |
| Exceeding authorized access | Stay within public-facing data; don't exploit APIs beyond intended use |
| Penalties | Criminal charges and civil liability |
| Gray areas | Scraping public data is debated; violating ToS alone may not be CFAA violation (post-Van Buren, 2021) |

#### GDPR — General Data Protection Regulation (EU)

| Provision | Implication for OSINT |
|-----------|----------------------|
| Lawful basis for processing | Need legitimate interest to process personal data |
| Right to be forgotten | Subjects can request data deletion |
| Data minimization | Collect only what is necessary |
| Purpose limitation | Data collected for one purpose cannot be used for another |
| Applies to | Any data about EU residents, regardless of where the investigator is located |

#### CCPA — California Consumer Privacy Act

| Provision | Implication for OSINT |
|-----------|----------------------|
| Consumer rights | Right to know what data is collected, right to delete |
| Applies to | Businesses meeting certain thresholds; may not apply to individual researchers |
| Opt-out rights | Consumers can opt out of data sale |

#### Other Relevant Laws

| Law/Regulation | Jurisdiction | Key Point |
|---------------|-------------|-----------|
| UK Data Protection Act 2018 | United Kingdom | GDPR-equivalent post-Brexit |
| PIPEDA | Canada | Personal information protection |
| Privacy Act 1988 | Australia | Australian privacy principles |
| Wiretap laws | Various US states | Some states require all-party consent for recording |
| Anti-stalking laws | Various | Persistent monitoring may cross legal lines |
| Right of publicity | Various US states | Using someone's likeness commercially |

### Web Scraping Legal Status

| Situation | Generally Legal | Risk Level |
|-----------|----------------|------------|
| Reading public web pages | Yes | None |
| Automated scraping of public data | Depends on jurisdiction and ToS | Low-Medium |
| Scraping behind login (public account) | Depends | Medium |
| Scraping behind login (unauthorized) | No | High — likely CFAA violation |
| Circumventing technical blocks (CAPTCHAs, rate limits) | Gray area | Medium-High |
| Scraping and republishing copyrighted content | No (copyright violation) | High |

### Breach Data

| Action | Legal Status | Recommendation |
|--------|-------------|----------------|
| Checking if an email appears in HIBP | Legal | Use freely |
| Downloading breach databases | Varies by jurisdiction | Avoid — possession may be illegal |
| Using breached credentials | Illegal (unauthorized access) | Never do this |
| Accessing breach data on forums | Gray area — varies by jurisdiction | Avoid |
| Referencing breach data in reports | Generally okay if sourced from HIBP | Note the source clearly |

---

## OPSEC for Investigators

### Threat Model

Who might want to know about your investigation?

| Threat | Scenario | Mitigation |
|--------|---------|------------|
| Investigation subject | Checking who views their profile | Don't use personal accounts |
| Subject's associates | Monitoring for investigators | Use VPN; minimize digital footprint |
| Platform operators | Logging access patterns | Distribute searches across time and platforms |
| Legal adversaries | Challenging investigation methods | Document methodology transparently |

### Network Security

| Measure | When to Use | How |
|---------|------------|-----|
| VPN | All OSINT research as baseline | Commercial VPN with no-logs policy |
| Tor | Sensitive research; accessing .onion sites | Tor Browser |
| Separate browser profile | Always | Dedicated browser with no personal accounts |
| Private/incognito mode | When cookies might leak identity | Enable for all OSINT browsing |
| DNS-over-HTTPS | Prevent ISP logging of DNS queries | Configure in browser or system |

### Account Security

| Rule | Reason |
|------|--------|
| Never use personal social media accounts for research | Subjects can see who viewed their profile |
| Do not create fake/sock puppet accounts | Violates platform ToS and ethical guidelines |
| Use dedicated research email addresses | Separation of personal and investigation identities |
| Do not authenticate to target services | Authentication creates a relationship between you and the target |

### Data Handling

| Practice | Details |
|----------|---------|
| Sanitize metadata from screenshots before sharing | Screenshots contain OS, username, timestamp info |
| Store investigation data securely | Encrypted storage for sensitive findings |
| Limit access to investigation files | Need-to-know basis |
| Dispose of data when investigation concludes | Don't retain PII beyond the investigation's needs |
| Use hashes to verify file integrity | SHA-256 hash all downloaded evidence |

### What Not to Reveal

- Do not discuss active investigations publicly
- Do not share investigation techniques that could help subjects evade detection
- Do not reveal which platforms or tools you are using during an active case
- Do not announce findings before the investigation is complete

---

## When to Stop

### Immediate Stop Conditions

These require stopping the current action immediately:

| Condition | Action |
|-----------|--------|
| Discovered the subject is a minor | Stop. Reassess scope. Apply maximum caution. Consult ethics. |
| Found PII far beyond investigation scope | Stop collecting. Note what was found. Do not dig deeper. |
| Actions would require unauthorized access | Do not proceed. Document the limitation. |
| Social engineering would be required to continue | Do not proceed. Note the dead end. |
| Subject appears to be in danger | Stop investigation activity. Consider whether to report to authorities. |
| Illegal content encountered | Stop. Do not download or preserve. Consider reporting obligations. |

### Reassessment Triggers

These require pausing to reassess before continuing:

| Trigger | Assessment |
|---------|-----------|
| Subject has taken steps to remove information | They may be aware of investigation; reassess OPSEC |
| Findings could endanger the subject if leaked | Tighten data handling; consider whether to continue |
| Investigation is being conducted on behalf of someone with unclear motives | Verify the requester's legitimate purpose |
| You feel uncomfortable with the direction | Trust your instincts; ethical unease is a signal |
| Findings are more invasive than anticipated | Return to scope boundaries; narrow if needed |

### Proportionality Check

Before each new phase of collection, ask:

```
Is the depth of this investigation proportional to:
- The seriousness of the matter being investigated?
- The potential benefit of the findings?
- The potential harm to the subject?

If the investigation has become disproportionate, STOP and reassess.
```

---

## Quick Reference Card

```
+-------------------------------------------+
|          OSINT ETHICS QUICK CHECK          |
+-------------------------------------------+
|                                            |
|  [x] Information is publicly available     |
|  [x] No unauthorized access required       |
|  [x] No social engineering involved        |
|  [x] Collection is proportionate to need   |
|  [x] Subject impact has been considered    |
|  [x] Legal requirements are met            |
|  [x] Investigation has legitimate purpose  |
|  [x] OPSEC measures are in place           |
|  [x] Data handling is secure               |
|  [x] Methodology is documentable           |
|                                            |
|  If ANY box is unchecked: STOP and ASSESS  |
+-------------------------------------------+
```

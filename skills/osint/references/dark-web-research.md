# Dark Web Research Reference

Techniques for conducting OSINT research involving Tor hidden services, onion sites, and dark web content. Load this reference when an investigation requires monitoring onion services, researching dark web marketplaces, checking for leaked data, or understanding dark web infrastructure. This guide emphasizes passive research, legal compliance, and strict ethical boundaries.

---

## When NOT to Go Dark

Before accessing the dark web, consider whether your goal can be achieved from the clearnet:

| Need | Clearnet Alternative |
|------|---------------------|
| **Check for leaked credentials** | HaveIBeenPwned (haveibeenpwned.com), DeHashed, Intelligence X |
| **Search dark web content** | Ahmia.fi (clearnet gateway), Google cache, archived forum mirrors |
| **Monitor marketplace listings** | Dark web monitoring services (Flare, Recorded Future, DarkOwl) provide indexed data |
| **Find onion service status** | dark.fail provides verified .onion links from clearnet |
| **Research threat actors** | Many threat actors operate on Telegram, Discord, and clearnet forums simultaneously |
| **Check for data dumps** | Paste sites, breach databases, and Telegram channels often mirror dark web leaks |

**Rule of thumb**: If the information exists on the clearnet, use the clearnet. Dark web access adds OPSEC risk without additional intelligence value.

---

## Tor Basics

### How Tor Works

Tor (The Onion Router) routes traffic through three relays to anonymize the connection:

1. **Guard/Entry node**: Knows your real IP but not your destination
2. **Middle relay**: Knows neither source nor destination
3. **Exit node**: Knows the destination but not the source (for clearnet browsing)

For **.onion services** (hidden services), traffic never leaves the Tor network -- there is no exit node. Both the user and the service connect through the Tor network to a rendezvous point.

### Onion Address Format

| Version | Format | Example |
|---------|--------|---------|
| **v2 (deprecated)** | 16 characters, base32 | `abcdefghijklmnop.onion` |
| **v3 (current)** | 56 characters, base32 | `vww6ybal4bd7szmgncyruucpgfkqahzddi37ktceo3ah7ngmcopnpyyd.onion` |

V3 addresses are derived from the service's public key, making them self-authenticating. The length makes them impossible to memorize, so users rely on link directories.

### Tor Browser

- Based on Firefox ESR with privacy modifications
- Download only from torproject.org
- Disables JavaScript by default at "Safest" security level
- Does not store browsing history or cookies across sessions
- Includes NoScript and HTTPS Everywhere

---

## Dark Web Search and Discovery

### Search Engines

| Engine | Access | URL | Notes |
|--------|--------|-----|-------|
| **Ahmia** | Clearnet + Tor | ahmia.fi | Filters out abuse material. Best starting point for research. Clearnet interface available |
| **Haystak** | Tor only | (onion address via dark.fail) | Indexes over 1.5 billion pages. Includes historical snapshots |
| **Torch** | Tor only | (onion address via dark.fail) | One of the oldest Tor search engines. Large index, less filtering |
| **DarkSearch** | Clearnet API | darksearch.io | API access to dark web index. Free tier available |
| **Recon** | Tor only | (onion address via dark.fail) | Marketplace-focused search and vendor lookup |

### Link Directories and Monitoring

| Resource | Access | URL | Purpose |
|----------|--------|-----|---------|
| **dark.fail** | Clearnet | dark.fail | Verified, PGP-signed .onion links. Monitors uptime. The most trusted link directory |
| **onion.live** | Clearnet | onion.live | Onion service uptime monitoring and categorization |
| **Tor.Taxi** | Clearnet + Tor | tor.taxi | Curated directory of onion services by category |
| **Darknet Live** | Clearnet | darknetlive.com | News and monitoring of darknet markets and services |

### Intelligence Platforms (Commercial)

| Platform | URL | Purpose |
|----------|-----|---------|
| **DarkOwl** | darkowl.com | Dark web data aggregation and monitoring API |
| **Flare** | flare.io | Threat exposure monitoring across dark and clear web |
| **Recorded Future** | recordedfuture.com | Threat intelligence including dark web monitoring |
| **Intelligence X** | intelx.io | Search engine for leaked data, paste sites, dark web content. Free tier with limited results |
| **SpiderFoot** | spiderfoot.net | Open-source OSINT automation with dark web modules |

---

## Breach and Leak Checking

### Credential Leak Databases

| Tool | URL | Auth | Purpose |
|------|-----|------|---------|
| **HaveIBeenPwned** | haveibeenpwned.com | Free (API key for searches) | Check if email/phone appeared in known breaches. Gold standard for breach notification |
| **HIBP Passwords** | haveibeenpwned.com/Passwords | Free | Check if a password hash appears in breached datasets (k-anonymity model) |
| **DeHashed** | dehashed.com | Paid | Search breaches by email, username, IP, name, phone. Returns partial plaintext data |
| **Intelligence X** | intelx.io | Free tier | Searches paste sites, leaks, dark web. Historical data preservation |
| **LeakCheck** | leakcheck.io | Paid | Breach search by email, username, phone, keyword |
| **Snusbase** | snusbase.com | Paid | Breach database search with plaintext results |

### Paste Sites

Paste sites are commonly used to dump leaked data:
- **Pastebin** (pastebin.com) -- The most well-known. Many pastes are indexed by search engines
- **Ghostbin, Rentry, PrivateBin** -- Alternatives with varying retention policies
- **Tor-based paste sites** -- Ephemeral, harder to monitor
- **Telegram channels** -- Increasingly used for leak distribution

Search for leaked data referencing a target using Google dorking:
```
site:pastebin.com "target-email@example.com"
site:rentry.co "target-username"
```

---

## Common Onion Services for OSINT

### Legitimate Services with Onion Mirrors

Many legitimate organizations operate .onion mirrors for censorship-resistant access:

| Service | Purpose | Notes |
|---------|---------|-------|
| **SecureDrop instances** | Whistleblower submission for news organizations | NYT, Guardian, Washington Post, ProPublica, and many others operate SecureDrop |
| **Facebook** | Social media | facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion |
| **BBC News** | News | bbcnewsd73hkzno2ini43t4gblxvycyac5aw4gnv7t2rccijh7745uqd.onion |
| **DuckDuckGo** | Search engine | duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion |
| **ProtonMail** | Email | protonmailrmez3lotccipshtkleegetolb73fuirgj7r4o4vfu7ozyd.onion |
| **Debian, Tor Project** | Software repositories | Onion mirrors for secure package downloads |

### SecureDrop Directory

The Freedom of the Press Foundation maintains a verified directory of SecureDrop instances:
- **Clearnet**: securedrop.org/directory
- Lists news organizations worldwide that accept anonymous submissions
- Each entry includes the verified .onion address and PGP fingerprint

---

## OPSEC for Dark Web Research

### Essential Precautions

| Measure | Implementation | Purpose |
|---------|---------------|---------|
| **Dedicated environment** | Use a VM (Whonix, Tails) or separate physical machine | Isolate research from personal activity |
| **Tor Browser only** | Never access .onion sites outside Tor Browser | Prevents IP leaks |
| **Safest security level** | Tor Browser -> Security Settings -> Safest | Disables JavaScript, reduces attack surface |
| **No personal accounts** | Never log in to personal accounts from Tor | Prevents identity correlation |
| **VPN + Tor** | VPN before Tor (optional, debated) | Hides Tor usage from ISP. Adds a trust point (the VPN provider) |
| **No downloads** | Do not download files from dark web services | Files may contain malware or tracking beacons |
| **No interaction** | Passive observation only | Engaging with illegal services creates legal liability |
| **Screenshot, don't save** | Capture screenshots rather than downloading content | Reduces risk of possessing illegal material |

### Whonix vs. Tails

| Feature | Whonix | Tails |
|---------|--------|-------|
| **Type** | VM-based (runs inside VirtualBox/KVM) | Live USB OS (boots from USB, leaves no trace) |
| **Persistence** | Yes (VM disk) | Optional encrypted persistence |
| **Network isolation** | Gateway VM routes all traffic through Tor | All traffic routed through Tor by design |
| **Use case** | Long-term research workstation | One-off investigations, maximum amnesia |
| **Setup** | Install VirtualBox + Whonix VMs | Flash Tails to USB, boot from it |

---

## Ethical Framework

### Core Principles

1. **Passive observation only** -- Browse and observe. Never create accounts on illegal platforms, never post, never interact with vendors or users
2. **No purchasing** -- Never buy anything, including "samples" or "previews." This crosses a clear legal line
3. **No illegal content** -- Do not access, download, or view child sexual abuse material or other content that is illegal to possess. If encountered, immediately close the page
4. **Document methodology** -- Keep detailed logs of what was accessed, when, why, and how. This provides a legal defense and demonstrates professional intent
5. **Minimize exposure** -- Access only what is necessary for the investigation. Do not browse "out of curiosity"
6. **Report illegal activity** -- If you discover serious criminal activity (CSAM, imminent threats), report through appropriate channels (NCMEC CyberTipline, law enforcement)

### Legal Boundaries

| Activity | General Legal Status | Notes |
|----------|---------------------|-------|
| **Using Tor** | Legal in most countries | Tor itself is not illegal. Some authoritarian regimes restrict its use |
| **Viewing .onion sites** | Generally legal | Viewing publicly accessible content is typically not illegal |
| **Downloading illegal content** | Illegal | Possessing CSAM, stolen data, or malware is criminal regardless of intent |
| **Purchasing illicit goods** | Illegal | No exceptions for "research purposes" |
| **Creating accounts on illegal platforms** | Legal grey area | May constitute participation in a criminal enterprise |
| **Monitoring forums passively** | Generally legal | Comparable to reading a public noticeboard |
| **Saving screenshots as evidence** | Context-dependent | Acceptable for professional OSINT/journalism with documented methodology; avoid capturing illegal content |

**Jurisdiction matters**: Laws vary significantly by country. Some jurisdictions criminalize accessing certain categories of content regardless of intent. Consult legal counsel for your jurisdiction before conducting dark web research.

---

## Alternative Anonymity Networks

| Network | URL | Notes |
|---------|-----|-------|
| **I2P** (Invisible Internet Project) | geti2p.net | Peer-to-peer network focused on internal services ("eepsites"). More suitable for peer-to-peer communication than browsing |
| **Freenet** | freenetproject.org | Decentralized, censorship-resistant data store. Content-focused rather than service-focused |
| **ZeroNet** | zeronet.io | Decentralized web using Bitcoin cryptography and BitTorrent. Sites are hosted by visitors |
| **Lokinet** | lokinet.org | Onion-routing network built on the Oxen blockchain |

These networks have smaller user bases and less content than Tor. They are rarely the primary target of OSINT investigations but may appear as alternative communication channels.

---

## Investigation Workflow

1. **Assess necessity** -- Determine if dark web access is actually required. Check clearnet alternatives first
2. **Prepare environment** -- Set up Whonix/Tails, verify Tor is working, confirm no identity leakage
3. **Gather known starting points** -- Use dark.fail and Ahmia to find relevant .onion addresses from clearnet
4. **Document before accessing** -- Log the investigation purpose, target, methodology, and legal basis
5. **Access and observe** -- Use Tor Browser at Safest level. Take screenshots. Note timestamps
6. **Check breach databases** -- Use HaveIBeenPwned, Intelligence X, and DeHashed from clearnet for associated data
7. **Cross-reference with clearnet** -- Many dark web entities have clearnet footprints (Telegram, social media, forum mirrors)
8. **Record findings in knowledge graph** -- Document entities, relationships, and evidence chain
9. **Preserve evidence** -- Screenshots with timestamps, archived pages, documented access methodology

---

## Cross-References

- `opsec-ethics.md` -- Comprehensive OPSEC guidance and ethical framework
- `investigation-setup.md` -- Setting up secure research environments
- `people-social-media.md` -- Cross-referencing dark web identities with social media
- `crypto-financial.md` -- Tracing cryptocurrency payments from dark web transactions
- `domain-infrastructure.md` -- Investigating infrastructure behind onion services
- `knowledge-graph.md` -- Entity schema for recording dark web findings

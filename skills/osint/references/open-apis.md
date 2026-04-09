# Open APIs Reference

Free OSINT APIs organized by category. All endpoints listed here are free to use (some require free API keys). Always respect rate limits and terms of service.

---

## DNS and Domain

### Google DNS-over-HTTPS

| Field | Details |
|-------|---------|
| **Endpoint** | `https://dns.google/resolve` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Generous; no published limit |

**Parameters:**
- `name` — domain to resolve (required)
- `type` — record type: A, AAAA, MX, NS, TXT, CNAME, SOA, PTR (default: A)

**Example:**
```
GET https://dns.google/resolve?name=example.com&type=A
GET https://dns.google/resolve?name=example.com&type=MX
GET https://dns.google/resolve?name=example.com&type=TXT
```

**Returns:** JSON with Answer array containing record data.

---

### Cloudflare DNS-over-HTTPS

| Field | Details |
|-------|---------|
| **Endpoint** | `https://cloudflare-dns.com/dns-query` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Generous; no published limit |
| **Required Header** | `Accept: application/dns-json` |

**Example:**
```
GET https://cloudflare-dns.com/dns-query?name=example.com&type=A
Header: Accept: application/dns-json
```

---

### RDAP (WHOIS Replacement)

| Field | Details |
|-------|---------|
| **Endpoint** | `https://rdap.org/domain/{domain}` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Varies by registry |

**Example:**
```
GET https://rdap.org/domain/example.com
GET https://rdap.org/ip/93.184.216.34
GET https://rdap.org/autnum/13335
```

**Returns:** Structured JSON with registration data, contacts (if not redacted), dates, nameservers, status.

**Alternatives:**
- ARIN (North America): `https://rdap.arin.net/registry/ip/{ip}`
- RIPE (Europe): `https://rdap.db.ripe.net/ip/{ip}`
- APNIC (Asia-Pacific): `https://rdap.apnic.net/ip/{ip}`

---

## Certificate Transparency

### crt.sh

| Field | Details |
|-------|---------|
| **Endpoint** | `https://crt.sh/` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | No formal limit, but be respectful (1-2 req/sec) |

**Parameters:**
- `q` — search query (domain, wildcard with %, email)
- `output` — set to `json` for JSON response

**Examples:**
```
GET https://crt.sh/?q=%.example.com&output=json          # All subdomains
GET https://crt.sh/?q=example.com&output=json             # Exact domain certs
GET https://crt.sh/?q=%.%.example.com&output=json         # Deep subdomain discovery
GET https://crt.sh/?q=user@example.com&output=json        # Email in cert
```

**Returns:** Array of certificate records with issuer, subject names, validity dates, serial numbers.

**OSINT value:** Discovers subdomains, reveals organizational email addresses in certs, shows historical infrastructure.

---

## IP Enrichment

### Shodan InternetDB

| Field | Details |
|-------|---------|
| **Endpoint** | `https://internetdb.shodan.io/{ip}` |
| **Method** | GET |
| **Auth** | None (free, no key) |
| **Rate Limit** | Generous |

**Example:**
```
GET https://internetdb.shodan.io/93.184.216.34
```

**Returns:**
```json
{
  "cpes": ["cpe:/a:apache:http_server:2.4"],
  "hostnames": ["example.com"],
  "ip": "93.184.216.34",
  "ports": [80, 443],
  "tags": ["cloud"],
  "vulns": ["CVE-2021-12345"]
}
```

---

### ip-api.com

| Field | Details |
|-------|---------|
| **Endpoint** | `http://ip-api.com/json/{ip}` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | 45 requests/minute |

**Example:**
```
GET http://ip-api.com/json/93.184.216.34
GET http://ip-api.com/json/93.184.216.34?fields=status,country,city,lat,lon,isp,org,as
```

**Returns:** Country, region, city, lat/lon, ISP, organization, AS number.

**Note:** HTTP only on free tier (not HTTPS). Use the `fields` parameter to limit response.

---

### ipinfo.io

| Field | Details |
|-------|---------|
| **Endpoint** | `https://ipinfo.io/{ip}/json` |
| **Method** | GET |
| **Auth** | Optional token (50k/month free with token, limited without) |
| **Rate Limit** | 50,000 requests/month with free token |

**Example:**
```
GET https://ipinfo.io/93.184.216.34/json
GET https://ipinfo.io/93.184.216.34/json?token=YOUR_TOKEN
```

**Returns:** IP, hostname, city, region, country, location (lat,lon), org (ASN + name), postal, timezone.

---

## Social and Identity

### GitHub API

| Field | Details |
|-------|---------|
| **Endpoint** | `https://api.github.com/users/{username}` |
| **Method** | GET |
| **Auth** | None (60 req/hour) or token (5000 req/hour) |
| **Rate Limit** | 60 requests/hour unauthenticated |

**Examples:**
```
GET https://api.github.com/users/johndoe
GET https://api.github.com/users/johndoe/repos
GET https://api.github.com/users/johndoe/events/public
GET https://api.github.com/search/users?q=john+doe+location:new+york
GET https://api.github.com/search/commits?q=author-email:john@example.com
```

**OSINT value:** Real name, email (from commits), location, employer, profile photo, activity timeline, repos, organizations.

**Tip:** Check `/users/{username}/events/public` for recent activity including push events that may reveal email addresses in commit data.

---

### Reddit User API

| Field | Details |
|-------|---------|
| **Endpoint** | `https://www.reddit.com/user/{username}/about.json` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Respect Reddit's robots.txt; ~1 req/sec |

**Examples:**
```
GET https://www.reddit.com/user/johndoe/about.json
GET https://www.reddit.com/user/johndoe/submitted.json
GET https://www.reddit.com/user/johndoe/comments.json
```

**Returns:** Account creation date, karma, subreddit subscriptions (if public), posting history.

---

### Gravatar

| Field | Details |
|-------|---------|
| **Endpoint** | `https://www.gravatar.com/{md5_of_email}.json` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Generous |

**Example:**
```
# First, MD5 hash the lowercase, trimmed email
# echo -n "user@example.com" | md5sum
GET https://www.gravatar.com/b58996c504c5638798eb6b511e6f49af.json
```

**Returns:** Display name, profile URL, location, about text, linked accounts (if set), profile photo URL.

**OSINT value:** Links email addresses to profile photos and identities. Many people forget Gravatar profiles exist.

---

### Keybase

| Field | Details |
|-------|---------|
| **Endpoint** | `https://keybase.io/_/api/1.0/user/lookup.json` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Reasonable |

**Examples:**
```
GET https://keybase.io/_/api/1.0/user/lookup.json?usernames=johndoe
GET https://keybase.io/_/api/1.0/user/lookup.json?twitter=johndoe
GET https://keybase.io/_/api/1.0/user/lookup.json?github=johndoe
```

**Returns:** Verified identity proofs linking usernames across platforms, PGP keys, profile data.

**OSINT value:** Keybase verifies cross-platform identities. If someone has a Keybase profile, it cryptographically links their accounts.

---

## Blockchain

### Blockchain.info (Bitcoin)

| Field | Details |
|-------|---------|
| **Endpoint** | `https://blockchain.info/rawaddr/{address}` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Moderate; use `&limit=10` to reduce payload |

**Examples:**
```
GET https://blockchain.info/rawaddr/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa?limit=10
GET https://blockchain.info/balance?active=ADDRESS1|ADDRESS2
GET https://blockchain.info/q/addressbalance/ADDRESS
```

**Returns:** Balance, total received/sent, transaction count, individual transactions.

---

### Blockstream.info (Bitcoin)

| Field | Details |
|-------|---------|
| **Endpoint** | `https://blockstream.info/api/address/{address}` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Reasonable |

**Examples:**
```
GET https://blockstream.info/api/address/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
GET https://blockstream.info/api/address/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa/txs
```

**Returns:** Address statistics and transactions. Generally more reliable than blockchain.info.

---

### Etherscan (Ethereum)

| Field | Details |
|-------|---------|
| **Endpoint** | `https://api.etherscan.io/api` |
| **Method** | GET |
| **Auth** | Free API key required |
| **Rate Limit** | 5 calls/second with free key |

**Examples:**
```
GET https://api.etherscan.io/api?module=account&action=balance&address=0x...&apikey=KEY
GET https://api.etherscan.io/api?module=account&action=txlist&address=0x...&apikey=KEY
GET https://api.etherscan.io/api?module=account&action=tokentx&address=0x...&apikey=KEY
```

---

## Archive and Historical

### Wayback Machine CDX API

| Field | Details |
|-------|---------|
| **Endpoint** | `https://web.archive.org/cdx/search/cdx` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Be respectful; no hard limit published |

**Parameters:**
- `url` — URL or domain to search (required)
- `output` — `json` or `text` (default: text)
- `matchType` — `exact`, `prefix`, `host`, `domain`
- `from` / `to` — date range (YYYYMMDD or YYYYMMDDHHMMSS)
- `limit` — max results
- `filter` — e.g., `statuscode:200`, `mimetype:text/html`
- `fl` — fields to return (e.g., `timestamp,original,statuscode`)
- `collapse` — deduplicate (e.g., `digest` for unique content)

**Examples:**
```
# All snapshots of a URL
GET https://web.archive.org/cdx/search/cdx?url=example.com&output=json&limit=50

# All pages under a domain
GET https://web.archive.org/cdx/search/cdx?url=example.com/*&output=json&limit=100

# Only HTML pages that loaded successfully, in 2023
GET https://web.archive.org/cdx/search/cdx?url=example.com&output=json&filter=statuscode:200&filter=mimetype:text/html&from=20230101&to=20231231

# Unique content only (deduplicated)
GET https://web.archive.org/cdx/search/cdx?url=example.com&output=json&collapse=digest
```

**Accessing snapshots:** `https://web.archive.org/web/{timestamp}/{url}`

---

### Common Crawl Index

| Field | Details |
|-------|---------|
| **Endpoint** | `https://index.commoncrawl.org/{crawl-id}-index` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | Be respectful |

**Parameters:**
- `url` — URL to search (required)
- `output` — `json`
- `limit` — max results

**Examples:**
```
# Search for a URL in a specific crawl
GET https://index.commoncrawl.org/CC-MAIN-2024-10-index?url=example.com&output=json

# Wildcard search for all pages
GET https://index.commoncrawl.org/CC-MAIN-2024-10-index?url=example.com/*&output=json&limit=100

# List available crawls
GET https://index.commoncrawl.org/collinfo.json
```

---

## Geolocation

### OpenStreetMap Nominatim

| Field | Details |
|-------|---------|
| **Endpoint** | `https://nominatim.openstreetmap.org/search` |
| **Method** | GET |
| **Auth** | None |
| **Rate Limit** | 1 request/second (strict) |
| **Required** | `User-Agent` header identifying your application |

**Examples:**
```
# Forward geocode (address to coordinates)
GET https://nominatim.openstreetmap.org/search?q=Empire+State+Building&format=json&limit=5

# Reverse geocode (coordinates to address)
GET https://nominatim.openstreetmap.org/reverse?lat=40.7484&lon=-73.9857&format=json

# Structured search
GET https://nominatim.openstreetmap.org/search?street=350+5th+Ave&city=New+York&format=json
```

**Returns:** Display name, lat/lon, bounding box, OSM type and ID, address breakdown.

---

### Overpass API (OpenStreetMap Data)

| Field | Details |
|-------|---------|
| **Endpoint** | `https://overpass-api.de/api/interpreter` |
| **Method** | GET or POST |
| **Auth** | None |
| **Rate Limit** | 2 concurrent requests; 10,000 requests/day |

**Example:**
```
# Find all restaurants within 500m of a point
GET https://overpass-api.de/api/interpreter?data=[out:json];node(around:500,40.7484,-73.9857)[amenity=restaurant];out;

# Find all surveillance cameras in an area
GET https://overpass-api.de/api/interpreter?data=[out:json];node(40.74,-73.99,40.75,-73.98)[man_made=surveillance];out;
```

**OSINT value:** Find specific infrastructure, landmarks, and features near a location. Useful for geolocating photos by matching visible features.

---

## Security and Threat Intelligence

### URLScan.io

| Field | Details |
|-------|---------|
| **Endpoint** | `https://urlscan.io/api/v1/search/` |
| **Method** | GET |
| **Auth** | Optional API key for higher limits |
| **Rate Limit** | Limited without key; 120/min with free key |

**Examples:**
```
GET https://urlscan.io/api/v1/search/?q=domain:example.com
GET https://urlscan.io/api/v1/search/?q=ip:93.184.216.34
GET https://urlscan.io/api/v1/search/?q=server:nginx AND domain:example.com
```

**Returns:** Scan results including page screenshots, DOM content, HTTP transactions, linked domains, IPs, certificates.

---

### VirusTotal

| Field | Details |
|-------|---------|
| **Endpoint** | `https://www.virustotal.com/api/v3/` |
| **Method** | GET |
| **Auth** | Free API key required |
| **Rate Limit** | 4 requests/minute; 500/day (free tier) |

**Examples:**
```
GET https://www.virustotal.com/api/v3/domains/{domain}
Header: x-apikey: YOUR_KEY

GET https://www.virustotal.com/api/v3/ip_addresses/{ip}
Header: x-apikey: YOUR_KEY

GET https://www.virustotal.com/api/v3/urls/{url_id}    # url_id = base64url of URL
Header: x-apikey: YOUR_KEY
```

**Returns:** Reputation scores, detection results, WHOIS info, DNS records, subdomains, associated files, historical data.

---

### AbuseIPDB

| Field | Details |
|-------|---------|
| **Endpoint** | `https://api.abuseipdb.com/api/v2/check` |
| **Method** | GET |
| **Auth** | Free API key required |
| **Rate Limit** | 1,000 requests/day (free) |

**Example:**
```
GET https://api.abuseipdb.com/api/v2/check?ipAddress=93.184.216.34&maxAgeInDays=90
Headers:
  Key: YOUR_KEY
  Accept: application/json
```

**Returns:** Abuse confidence score, country, ISP, usage type, domain, total reports, last reported date.

---

### HaveIBeenPwned

| Field | Details |
|-------|---------|
| **Endpoint** | `https://haveibeenpwned.com/api/v3/breachedaccount/{email}` |
| **Method** | GET |
| **Auth** | API key required (paid, but affordable) |
| **Rate Limit** | Per subscription tier |

**Free alternative — password check (k-anonymity):**
```
GET https://api.pwnedpasswords.com/range/{first5chars_of_SHA1}
```

**Note:** The breach lookup API now requires a paid key. The password API remains free and uses k-anonymity (only send first 5 chars of SHA-1 hash).

**OSINT value:** Confirms email addresses exist and identifies which services they've been registered with (via breach names).

---

## Quick Reference Table

| API | Auth | Rate Limit | Best For |
|-----|------|-----------|----------|
| Google DNS | None | Generous | DNS lookups |
| Cloudflare DNS | None | Generous | DNS lookups (alternative) |
| RDAP | None | Varies | WHOIS data |
| crt.sh | None | ~1-2/sec | Subdomain discovery |
| Shodan InternetDB | None | Generous | IP scanning |
| ip-api.com | None | 45/min | IP geolocation |
| ipinfo.io | Optional token | 50k/month | IP details |
| GitHub | None/token | 60/hr or 5000/hr | Developer profiles |
| Reddit | None | ~1/sec | User research |
| Gravatar | None | Generous | Email to identity |
| Keybase | None | Reasonable | Cross-platform identity |
| Blockchain.info | None | Moderate | Bitcoin addresses |
| Blockstream | None | Reasonable | Bitcoin addresses |
| Etherscan | Free key | 5/sec | Ethereum addresses |
| Wayback CDX | None | Respectful | Historical web pages |
| Common Crawl | None | Respectful | Historical web data |
| Nominatim | None | 1/sec | Geocoding |
| Overpass | None | 2 concurrent | OSM data queries |
| URLScan.io | Optional | 120/min with key | URL analysis |
| VirusTotal | Free key | 4/min | Domain/IP reputation |
| AbuseIPDB | Free key | 1000/day | IP abuse reports |
| HIBP | Paid key | Varies | Breach checking |

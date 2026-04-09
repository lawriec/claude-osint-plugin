# Domain, DNS, IP, and Network Infrastructure Investigation

Techniques for mapping the technical infrastructure behind domains, IP addresses, and online services.

---

## Passive vs. Active Reconnaissance

**Passive reconnaissance** does NOT send any traffic to the target. You query third-party databases and public records. This is safe, legal, and undetectable by the target.

**Active reconnaissance** involves sending requests directly to the target (port scans, web requests, etc.). This may be detectable and should only be done with proper authorization.

This guide focuses primarily on passive techniques using plugin tools.

---

## Passive Reconnaissance

### 1. WHOIS / RDAP -- `query_whois.py`

WHOIS reveals domain registration details.

```
python query_whois.py example.com
```

**Key Fields:**
| Field | Intelligence Value |
|-------|-------------------|
| Registrar | Where the domain was registered (GoDaddy, Namecheap, etc.) |
| Registration date | When the domain was first registered — age indicates legitimacy |
| Expiry date | When it expires — domains about to expire may be abandoned |
| Updated date | Last modification to registration |
| Registrant name | Who registered it (often redacted for privacy) |
| Registrant org | Organization (sometimes visible even with privacy) |
| Registrant email | Contact email (often proxy email if privacy enabled) |
| Name servers | DNS infrastructure — reveals hosting provider |
| Status | clientTransferProhibited, serverHold, etc. |

**WHOIS Privacy / Redaction:**
- GDPR (2018+) caused most registrars to redact European registrant details
- Privacy services (WhoisGuard, Domains By Proxy) mask registrant info
- Historical WHOIS records may reveal info from before privacy was enabled
- Sources for historical WHOIS: DomainTools, WhoisXML API, SecurityTrails

**Technique: Reverse WHOIS**
- Search for all domains registered by the same name, email, or organization
- DomainTools Reverse WHOIS is the gold standard (commercial)
- ViewDNS.info offers a free limited reverse WHOIS

**Technique: Registrant Pivoting**
If you find a registrant name/email/org:
```
registrant email --> reverse WHOIS --> all other domains by same registrant
registrant org --> corporate records --> related entities
registrant address --> property records, other registrations
```

### 2. DNS Enumeration -- `query_dns.py`

DNS records reveal the infrastructure behind a domain.

```
python query_dns.py example.com          # All common record types
python query_dns.py example.com A        # Specific record type
python query_dns.py example.com MX       # Mail servers
python query_dns.py example.com TXT      # Text records (SPF, DKIM, etc.)
```

**Record Types and Intelligence:**

| Record | Purpose | Intelligence Value |
|--------|---------|-------------------|
| **A** | IPv4 address | Hosting server location, provider |
| **AAAA** | IPv6 address | Same as A, IPv6 infrastructure |
| **MX** | Mail servers | Email provider (Google Workspace, Microsoft 365, self-hosted) |
| **TXT** | Arbitrary text | SPF (authorized email senders), DKIM, DMARC, site verification tokens |
| **NS** | Name servers | DNS provider (Cloudflare, AWS Route 53, etc.) |
| **SOA** | Start of Authority | Primary nameserver, admin email, serial number |
| **CNAME** | Canonical name (alias) | CDN provider, third-party services |
| **SRV** | Service records | Specific services running (SIP, XMPP, etc.) |
| **CAA** | Certificate Authority Authorization | Which CAs can issue certificates |
| **PTR** | Reverse DNS | Hostname for an IP (reverse lookup) |

**TXT Record Analysis:**

TXT records are a goldmine. Look for:
- **SPF records** (`v=spf1 ...`): Lists authorized email sending IPs/domains
  - `include:_spf.google.com` = uses Google Workspace
  - `include:spf.protection.outlook.com` = uses Microsoft 365
  - `include:sendgrid.net` = uses SendGrid for transactional email
  - `include:mailgun.org` = uses Mailgun
  - IP addresses in SPF = self-hosted mail servers
- **DKIM records**: Confirm email infrastructure
- **DMARC records** (`_dmarc.domain.com`): Email authentication policy
- **Verification tokens**: Reveal third-party services
  - `google-site-verification=...` = has Google Search Console
  - `facebook-domain-verification=...` = claimed in Facebook Business
  - `MS=...` = Microsoft 365
  - `docusign=...` = uses DocuSign
  - `atlassian-domain-verification=...` = uses Atlassian products
  - `_github-pages-challenge-...` = uses GitHub Pages

**Subdomain Enumeration:**
- DNS brute force (active — use with authorization)
- Certificate Transparency logs (passive — see below)
- Google dorking: `site:*.example.com`
- SecurityTrails subdomain finder
- VirusTotal domain report
- DNSDumpster (dnsdumpster.com)
- Sublist3r, Amass, Subfinder (external tools)

### 3. Certificate Transparency -- `query_crtsh.py`

Certificate Transparency (CT) logs record every SSL/TLS certificate issued publicly.

```
python query_crtsh.py example.com
```

**What CT Reveals:**
- All subdomains that have had certificates issued (even internal ones!)
- Historical certificates (past infrastructure, old subdomains)
- Certificate issuer (Let's Encrypt = automated, DigiCert/Comodo = commercial)
- Certificate validity dates
- Subject Alternative Names (SANs) — one cert may cover multiple domains

**Subdomain Discovery via CT:**
CT logs are the best passive method for subdomain enumeration:
```
domain.com --> crt.sh --> 
  mail.domain.com
  vpn.domain.com
  staging.domain.com
  dev.domain.com
  api.domain.com
  internal.domain.com
  old-site.domain.com
```

Internal/development subdomains are especially valuable — they often reveal:
- Internal infrastructure naming conventions
- Development and staging environments
- Services not meant to be public
- Acquired or merged company domains

### 4. IP Enrichment -- `query_shodan_internetdb.py`

InternetDB provides a free, passive IP lookup with no API key required.

```
python query_shodan_internetdb.py 1.2.3.4
```

**Returns:**
| Field | Intelligence Value |
|-------|-------------------|
| Open ports | Services running on this IP |
| Hostnames | Domains/subdomains pointing to this IP |
| CPEs | Common Platform Enumeration — software/version identified |
| Vulns | Known CVEs associated with detected software |
| Tags | Classifications (e.g., "self-signed", "cloud", "tor") |

**Common Port Intelligence:**
| Port | Service | Notes |
|------|---------|-------|
| 22 | SSH | Remote access, usually Linux |
| 25 | SMTP | Mail server |
| 53 | DNS | Authoritative DNS server |
| 80 | HTTP | Unencrypted web server |
| 443 | HTTPS | Encrypted web server |
| 445 | SMB | Windows file sharing (should NOT be public) |
| 993 | IMAPS | Email (IMAP over SSL) |
| 1433 | MSSQL | SQL Server database (should NOT be public) |
| 3306 | MySQL | MySQL database (should NOT be public) |
| 3389 | RDP | Windows Remote Desktop (high risk if public) |
| 5432 | PostgreSQL | PostgreSQL database (should NOT be public) |
| 5900 | VNC | Remote desktop (should NOT be public) |
| 8080 | HTTP alt | Alternative web server, often development |
| 8443 | HTTPS alt | Alternative HTTPS |
| 27017 | MongoDB | MongoDB database (should NOT be public) |

### 5. Reverse DNS

Map IP addresses back to hostnames:
```
dig -x 1.2.3.4
nslookup 1.2.3.4
```
Or use the PTR record type in `query_dns.py`.

**Applications:**
- Find what domain(s) an IP serves
- Identify shared hosting (many domains on one IP)
- Hostname format reveals provider (e.g., `ec2-1-2-3-4.compute-1.amazonaws.com`)

### 6. ASN / BGP Analysis

Autonomous System Numbers identify network operators.

**Lookup Tools:**
- bgp.he.net — Hurricane Electric BGP Toolkit (web)
- ipinfo.io/AS{number} — ASN details
- RIPE, ARIN, APNIC, LACNIC, AFRINIC — Regional Internet Registries

**Intelligence from ASN:**
- Organization name and country
- All IP ranges announced by that ASN
- Peering relationships
- Network size and type (ISP, hosting, enterprise, government)

### 7. Historical DNS

Track how DNS records have changed over time:
- **SecurityTrails** (securitytrails.com) — Historical A, MX, NS, TXT records
- **PassiveTotal / RiskIQ** (community.riskiq.com) — Passive DNS database
- **DNSHistory** (dnshistory.org) — Free historical DNS lookup
- **ViewDNS.info** — IP history for domains

**Use Cases:**
- Domain previously pointed to different IP → old infrastructure
- MX records changed from self-hosted to cloud → migration timeline
- NS records changed → DNS provider migration
- Historical IPs → may still be active, may reveal true IP behind CDN

---

## Infrastructure Mapping Pattern

The core workflow for mapping infrastructure from a single domain:

```
1. START: domain.com
   |
   +---> WHOIS --> registrant info, registration dates, name servers
   |       |
   |       +---> Registrant email --> reverse WHOIS --> other domains
   |       +---> Registrant org --> other domains, corporate records
   |
   +---> DNS A record --> IP address (e.g., 93.184.216.34)
   |       |
   |       +---> Shodan InternetDB --> ports, services, vulnerabilities
   |       +---> Reverse DNS --> other domains on same IP
   |       +---> ASN lookup --> hosting provider, IP range
   |       +---> Geolocation --> server location (country, city)
   |
   +---> DNS MX record --> mail server IPs
   |       |
   |       +---> Reveals email provider (Google, Microsoft, self-hosted)
   |       +---> Self-hosted MX IPs --> same analysis as A record IPs
   |
   +---> DNS TXT records --> SPF, DKIM, verification tokens
   |       |
   |       +---> SPF includes --> third-party email services
   |       +---> Verification tokens --> services used (Google, Facebook, etc.)
   |
   +---> crt.sh --> ALL subdomains with certificates
   |       |
   |       +---> Each subdomain --> repeat DNS resolution
   |       +---> Internal subdomains --> infrastructure insights
   |
   +---> DNS NS records --> DNS provider
           |
           +---> Cloudflare, AWS, etc. --> hosting strategy
```

### Multiple Domain Correlation

When investigating an organization with multiple domains:
1. Identify all domains (WHOIS reverse, Google dorking, CT logs)
2. Map DNS for each domain
3. Look for shared infrastructure:
   - Same IP addresses across domains
   - Same mail servers
   - Same name servers
   - Same hosting provider
   - Shared SSL certificates (SANs)
4. Shared infrastructure confirms domains are related

---

## CDN and Hosting Detection

### CDN Identification

**Cloudflare:**
- Name servers: `*.ns.cloudflare.com`
- HTTP headers: `cf-ray`, `server: cloudflare`
- IP ranges: 104.16.0.0/12, 172.64.0.0/13, 131.0.72.0/22, etc.
- To find origin IP behind Cloudflare: historical DNS, subdomain enumeration, email headers, certificate search

**AWS (Amazon Web Services):**
- Hostnames: `*.amazonaws.com`, `*.awsdns-*.com` (Route 53)
- S3 buckets: `*.s3.amazonaws.com` or `*.s3-{region}.amazonaws.com`
- CloudFront: `*.cloudfront.net`
- EC2: `ec2-*-*-*-*.{region}.compute.amazonaws.com`
- IP ranges: Published at ip-ranges.amazonaws.com/ip-ranges.json

**Google Cloud:**
- Hostnames: `*.googleusercontent.com`, `*.googleapis.com`
- Cloud Run: `*.run.app`
- App Engine: `*.appspot.com`
- DNS: `ns-cloud-*.googledomains.com`

**Microsoft Azure:**
- Hostnames: `*.azurewebsites.net`, `*.azure.com`, `*.cloudapp.azure.com`
- DNS: `*.azure-dns.com`, `*.azure-dns.net`
- Blob storage: `*.blob.core.windows.net`

**Akamai:**
- Hostnames: `*.akamaiedge.net`, `*.akamai.net`, `*.akadns.net`
- CNAME patterns pointing to `*.edgesuite.net`

**Fastly:**
- HTTP headers: `x-served-by`, `x-cache` with Fastly identifiers
- IP ranges: Published at api.fastly.com/public-ip-list

**Vercel:**
- CNAME: `cname.vercel-dns.com`
- A records: 76.76.21.21

**Netlify:**
- CNAME: `*.netlify.app`
- A record: 75.2.60.5

### Finding the Real IP Behind a CDN

If a domain uses a CDN/proxy like Cloudflare, the A record points to the CDN, not the origin server. To find the origin:

1. **Historical DNS** — Check DNS records from before CDN was enabled
2. **Subdomain enumeration** — Some subdomains (mail, ftp, cpanel, direct) may point to origin
3. **Email headers** — Outbound emails from the domain may contain origin IP
4. **Certificate search** — Origin server may serve its own certificate
5. **DNS leak** — Some configurations leak origin in TXT or other records
6. **Censys/Shodan search** — Search for the domain name in certificate or HTTP body across all IPs

---

## Web Technology Detection

### HTTP Headers

Check response headers for technology clues:

| Header | Reveals |
|--------|---------|
| `Server` | Web server software (nginx, Apache, IIS, etc.) |
| `X-Powered-By` | Application framework (PHP, Express, ASP.NET) |
| `X-Generator` | CMS or site builder (WordPress, Drupal, etc.) |
| `Set-Cookie` | Session technology, frameworks (PHPSESSID, JSESSIONID, etc.) |
| `X-AspNet-Version` | ASP.NET version |
| `X-Drupal-Cache` | Drupal CMS |
| `X-Varnish` | Varnish cache |
| `Via` | Proxy servers in chain |

### HTML Source Analysis

- `<meta name="generator" content="WordPress 6.4">` — CMS identifier
- JavaScript library files (jQuery, React, Angular, Vue)
- CSS framework classes (Bootstrap, Tailwind)
- Comment tags left by frameworks or developers
- Form action URLs revealing backend technology
- API endpoint patterns in JavaScript

### Common Files

| File | Reveals |
|------|---------|
| `/robots.txt` | Disallowed paths reveal site structure |
| `/sitemap.xml` | Full URL listing |
| `/wp-admin/` | WordPress |
| `/administrator/` | Joomla |
| `/user/login` | Drupal |
| `/.well-known/` | Various service configurations |
| `/humans.txt` | Team information (sometimes) |
| `/security.txt` or `/.well-known/security.txt` | Security contact info |
| `/crossdomain.xml` | Flash/Silverlight policies (legacy) |

---

## Email Infrastructure Analysis

### Determining Email Provider from MX Records

| MX Pattern | Provider |
|------------|----------|
| `*.google.com`, `*.googlemail.com` | Google Workspace |
| `*.outlook.com`, `*.protection.outlook.com` | Microsoft 365 |
| `*.pphosted.com` | Proofpoint (email security) |
| `*.mimecast.com` | Mimecast (email security) |
| `*.messagelabs.com` | Symantec/Broadcom |
| `*.secureserver.net` | GoDaddy |
| `*.zoho.com` | Zoho Mail |
| `*.emailsrvr.com` | Rackspace |
| `*.fastmail.com` | Fastmail |
| `*.tutanota.de` | Tutanota |
| `*.protonmail.ch` | ProtonMail |

### SPF Record Analysis

SPF tells you which servers are authorized to send email for a domain:
```
v=spf1 include:_spf.google.com include:sendgrid.net ip4:203.0.113.0/24 ~all
```

This reveals:
- Uses Google Workspace for email
- Uses SendGrid for transactional/marketing email
- Has a self-hosted mail server at 203.0.113.0/24
- `~all` = soft fail (testing) vs `-all` = hard fail (strict)

### DMARC Record Analysis

Check `_dmarc.domain.com` TXT record:
```
v=DMARC1; p=reject; rua=mailto:dmarc-reports@domain.com; ruf=mailto:forensics@domain.com
```

- `p=reject` means strict email authentication (mature security posture)
- `p=none` means monitoring only (less mature or in deployment)
- `rua` and `ruf` addresses may reveal additional infrastructure or third-party DMARC services

---

## Practical Investigation Patterns

### Pattern: Is this domain malicious?

1. **Registration date** — Recently registered domains are higher risk
2. **Registrar** — Some registrars are favored by malicious actors
3. **WHOIS privacy** — Legitimate and malicious sites both use it, but combined with other signals it adds context
4. **DNS infrastructure** — Shared hosting with many suspicious domains?
5. **Certificate** — Let's Encrypt (free, automated) vs. commercial CA
6. **Shodan** — Unexpected open ports, known vulnerabilities
7. **VirusTotal** — Check domain/IP reputation
8. **URLScan.io** — Safe sandbox scanning of suspicious URLs

### Pattern: Map an organization's attack surface

1. Find all domains via reverse WHOIS, Google dorking, CT logs
2. Enumerate subdomains for each domain via CT and DNS
3. Resolve all hostnames to IPs
4. Enrich each IP via Shodan InternetDB
5. Identify exposed services and potential vulnerabilities
6. Map relationships between assets

### Pattern: Trace domain ownership changes

1. Current WHOIS → current registrant
2. Historical WHOIS (DomainTools) → previous registrants
3. Historical DNS → infrastructure changes over time
4. Wayback Machine → website content changes
5. CT logs → certificate timeline
6. Correlate all timelines to identify ownership transitions

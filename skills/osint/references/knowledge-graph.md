# Knowledge Graph Reference

Entity schema and relationship model for OSINT investigations using the memory-graph MCP server. The knowledge graph tracks all entities, their attributes, and how they connect to each other throughout an investigation.

---

## Why Use a Knowledge Graph

- Track dozens of interconnected entities without losing relationships
- Surface hidden connections (person A and person B share an IP address)
- Maintain a queryable record of all discovered facts
- Support analysis by making relationships explicit and searchable

---

## Entity Types

### Person

| Observation Field | Example |
|-------------------|---------|
| name | "John Michael Doe" |
| aliases | "jdoe, johnny_d, JDoe1985" |
| dob | "1985-03-15" |
| location | "New York, NY, USA" |
| occupation | "Software Engineer" |
| employer | "Acme Corp" |
| email | "john.doe@example.com" |
| phone | "+1-555-123-4567" |
| bio | "LinkedIn bio: Senior developer with 10 years experience" |
| physical_description | "Brown hair, glasses, tattoo on left forearm" |
| nationality | "US citizen" |
| languages | "English, Spanish" |

### Organization

| Observation Field | Example |
|-------------------|---------|
| name | "Acme Corporation" |
| type | "Private company / NGO / Government agency" |
| location | "123 Main St, San Francisco, CA" |
| industry | "Technology" |
| founded | "2010" |
| registration_number | "EIN: 12-3456789" |
| website | "https://acme.com" |
| parent_org | "MegaCorp Holdings" |
| employee_count | "~500" |

### Domain

| Observation Field | Example |
|-------------------|---------|
| name | "example.com" |
| registrar | "Namecheap" |
| creation_date | "2015-01-10" |
| expiry_date | "2026-01-10" |
| nameservers | "ns1.cloudflare.com, ns2.cloudflare.com" |
| registrant | "Privacy protected / John Doe" |
| hosting_provider | "AWS / Cloudflare" |
| ip_addresses | "93.184.216.34" |
| subdomains | "mail.example.com, api.example.com, dev.example.com" |
| technologies | "WordPress 6.2, PHP 8.1, nginx" |

### IPAddress

| Observation Field | Example |
|-------------------|---------|
| address | "93.184.216.34" |
| version | "IPv4" |
| geolocation | "San Francisco, CA, USA" |
| asn | "AS13335" |
| isp | "Cloudflare, Inc." |
| open_ports | "80, 443, 8080" |
| hostnames | "example.com, other-site.com" |
| first_seen | "2020-01-15" |
| tags | "CDN, proxy" |

### EmailAddress

| Observation Field | Example |
|-------------------|---------|
| address | "john.doe@example.com" |
| provider | "Custom domain / Gmail / ProtonMail" |
| associated_person | "John Doe" |
| verified | "Active — appears in HIBP for 2 breaches" |
| gravatar | "Yes — links to profile image" |
| accounts_found | "GitHub, LinkedIn, Twitter" |

### PhoneNumber

| Observation Field | Example |
|-------------------|---------|
| number | "+1-555-123-4567" |
| carrier | "Verizon" |
| type | "Mobile / Landline / VoIP" |
| country | "United States" |
| associated_person | "John Doe" |
| messaging_apps | "WhatsApp: yes, Telegram: no" |

### Username

| Observation Field | Example |
|-------------------|---------|
| handle | "johndoe85" |
| platform | "GitHub" |
| url | "https://github.com/johndoe85" |
| verified | "Profile exists, active" |
| created | "2018-06-01" |
| other_platforms | "Same username found on: Twitter, Reddit, Steam" |

### SocialMediaProfile

| Observation Field | Example |
|-------------------|---------|
| platform | "Twitter/X" |
| handle | "@johndoe85" |
| url | "https://twitter.com/johndoe85" |
| bio | "Developer | Coffee enthusiast | NYC" |
| followers | "1,234" |
| following | "567" |
| joined_date | "March 2015" |
| post_frequency | "~3 tweets/day" |
| last_active | "2024-03-10" |
| notable_posts | "Tweeted about working at Acme on 2023-08-15" |

### Location

| Observation Field | Example |
|-------------------|---------|
| lat | "40.7128" |
| lon | "-74.0060" |
| address | "350 5th Ave, New York, NY 10118" |
| country | "United States" |
| type | "Office / Residence / Event venue" |
| landmark | "Empire State Building" |
| timezone | "America/New_York" |

### Image

| Observation Field | Example |
|-------------------|---------|
| filename | "profile_photo_001.jpg" |
| source_url | "https://example.com/photo.jpg" |
| exif_summary | "Canon EOS R5, 2024-01-15 14:30, GPS: 40.7128,-74.0060" |
| hash | "sha256:abc123..." |
| dimensions | "4000x3000" |
| reverse_image_hits | "Found on 3 other sites" |
| content_description | "Male, 30s, standing in front of Brooklyn Bridge" |

### Document

| Observation Field | Example |
|-------------------|---------|
| filename | "annual_report_2023.pdf" |
| type | "PDF / DOCX / XLSX" |
| metadata_summary | "Author: John Doe, Created: 2023-12-01, Software: Microsoft Word" |
| hash | "sha256:def456..." |
| page_count | "24" |
| source_url | "https://example.com/report.pdf" |

### CryptoWallet

| Observation Field | Example |
|-------------------|---------|
| address | "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" |
| chain | "Bitcoin / Ethereum / Monero" |
| balance | "0.5 BTC" |
| first_seen | "2015-03-20" |
| last_transaction | "2024-03-01" |
| total_received | "15.3 BTC" |
| total_sent | "14.8 BTC" |
| transaction_count | "247" |
| labels | "Known exchange deposit address" |

### Vehicle

| Observation Field | Example |
|-------------------|---------|
| type | "Car / Truck / Motorcycle / Boat" |
| registration | "ABC-1234" |
| make | "Toyota" |
| model | "Camry" |
| year | "2020" |
| color | "Silver" |
| vin | "1HGBH41JXMN109186" |
| registered_to | "John Doe" |
| jurisdiction | "New York" |

---

## Relationship Types

### Ownership and Control

| Relationship | From -> To | Example |
|-------------|-----------|---------|
| `owns` | Person -> Domain | John Doe owns example.com |
| `owns` | Person -> Vehicle | John Doe owns silver Camry |
| `owns` | Person -> CryptoWallet | John Doe owns BTC wallet 1A1z... |
| `owns` | Organization -> Domain | Acme Corp owns acme.com |
| `operates` | Person -> Organization | Jane Doe operates Acme Corp |
| `operates` | Organization -> Domain | Acme Corp operates acme.com |
| `registered` | Person -> Domain | John Doe registered example.com |

### Technical Relationships

| Relationship | From -> To | Example |
|-------------|-----------|---------|
| `resolves_to` | Domain -> IPAddress | example.com resolves to 93.184.216.34 |
| `hosted_on` | Domain -> IPAddress | blog.example.com hosted on 10.0.0.1 |
| `subdomain_of` | Domain -> Domain | mail.example.com subdomain of example.com |
| `shares_ip` | Domain -> Domain | example.com shares IP with other-site.com |
| `uses_nameserver` | Domain -> Domain | example.com uses ns1.cloudflare.com |
| `cert_covers` | Domain -> Domain | Certificate for *.example.com covers api.example.com |

### Personal Relationships

| Relationship | From -> To | Example |
|-------------|-----------|---------|
| `associated_with` | Person -> Person | John Doe associated with Jane Smith |
| `employed_by` | Person -> Organization | John Doe employed by Acme Corp |
| `member_of` | Person -> Organization | John Doe member of IEEE |
| `communicates_with` | Person -> Person | John Doe communicates with Jane Smith |
| `related_to` | Person -> Person | John Doe related to James Doe |

### Location Relationships

| Relationship | From -> To | Example |
|-------------|-----------|---------|
| `located_at` | Person -> Location | John Doe located at NYC |
| `located_at` | Organization -> Location | Acme Corp located at 123 Main St |
| `located_at` | IPAddress -> Location | 93.184.216.34 located at San Francisco |
| `photographed_at` | Image -> Location | photo_001.jpg photographed at Brooklyn Bridge |

### Content and Identity Relationships

| Relationship | From -> To | Example |
|-------------|-----------|---------|
| `posted_by` | Document -> Person | report.pdf posted by John Doe |
| `authored` | Person -> Document | John Doe authored whitepaper.pdf |
| `linked_to` | EmailAddress -> Person | john@example.com linked to John Doe |
| `linked_to` | Username -> Person | johndoe85 linked to John Doe |
| `linked_to` | PhoneNumber -> Person | +1-555-123-4567 linked to John Doe |
| `profile_of` | SocialMediaProfile -> Person | @johndoe85 profile of John Doe |
| `uses_email` | Person -> EmailAddress | John Doe uses john@example.com |
| `transacted_with` | CryptoWallet -> CryptoWallet | Wallet A transacted with Wallet B |

---

## Usage Examples

### Creating Entities

```
create_entities(entities=[
  {
    "name": "John Doe",
    "entityType": "Person",
    "observations": [
      "Located in New York, NY",
      "Software engineer",
      "Known alias: jdoe85",
      "Source: LinkedIn profile (tavily search 2024-03-15)"
    ]
  },
  {
    "name": "Acme Corporation",
    "entityType": "Organization",
    "observations": [
      "Technology company in San Francisco",
      "Founded 2010",
      "Website: acme.com",
      "Source: Company website (tavily extract 2024-03-15)"
    ]
  }
])
```

### Creating Relationships

```
create_relations(relations=[
  {
    "from": "John Doe",
    "to": "Acme Corporation",
    "relationType": "employed_by"
  },
  {
    "from": "Acme Corporation",
    "to": "acme.com",
    "relationType": "owns"
  }
])
```

### Adding Observations

```
add_observations(observations=[
  {
    "entityName": "John Doe",
    "contents": [
      "Email discovered: john.doe@acme.com (source: crt.sh certificate 2024-03-15)",
      "GitHub profile: github.com/jdoe85 (source: username check 2024-03-15)",
      "Phone: +1-555-123-4567 (source: WHOIS record for personal domain)"
    ]
  }
])
```

### Searching the Graph

```
search_nodes(query="John Doe")
search_nodes(query="acme.com")
search_nodes(query="New York")
```

### Reading the Full Graph

```
read_graph()
```

### Opening Specific Nodes

```
open_nodes(names=["John Doe", "Acme Corporation", "acme.com"])
```

---

## Best Practices

### Naming Conventions

| Entity Type | Naming Convention | Example |
|-------------|------------------|---------|
| Person | Full legal name, title case | "John Michael Doe" |
| Organization | Official name, title case | "Acme Corporation" |
| Domain | Lowercase, no protocol | "example.com" |
| IPAddress | Standard notation | "93.184.216.34" |
| EmailAddress | Lowercase | "john@example.com" |
| PhoneNumber | E.164 format | "+15551234567" |
| Username | Exact case as on platform | "JDoe85" |
| SocialMediaProfile | "platform:handle" format | "twitter:@johndoe85" |
| Location | Descriptive name | "Acme Corp NYC Office" |
| Image | Descriptive filename | "profile_photo_linkedin_johndoe" |
| CryptoWallet | First 10 chars + chain | "1A1zP1eP5Q (Bitcoin)" |
| Vehicle | Make Model Registration | "Toyota Camry ABC-1234" |

### Observation Guidelines

- Always include the source and date of each observation
- Format: `"[fact] (source: [tool/platform] [date])"`
- Record negative findings too: `"No LinkedIn profile found (source: tavily search 2024-03-15)"`
- Update observations as new information emerges — don't delete old ones
- Use consistent date format: YYYY-MM-DD

### Avoiding Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Duplicate entities | Fragments the graph | Search before creating |
| Vague observations | Not useful for analysis | Include specifics and sources |
| Missing relationships | Hidden connections stay hidden | Create relationships as you discover them |
| No provenance | Cannot verify findings | Always note source and date |
| Inconsistent naming | Cannot find entities | Follow naming conventions above |

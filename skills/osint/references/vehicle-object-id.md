# Vehicle, Aircraft, and Ship Identification for OSINT

Techniques for identifying and tracking vehicles, aircraft, ships, and other objects from images, video, and public tracking data.

---

## License Plates

### Format Overview by Region

**Europe:**

European plates generally follow a standardized format with a blue strip on the left showing the EU flag and country code.

| Country | Format Example | Notes |
|---------|---------------|-------|
| **UK** | `AB12 CDE` | Two letters (area) + two digits (age) + three letters (random). Age identifier changes every 6 months (March/September) |
| **Germany** | `B AB 1234` | 1-3 letter city code + 1-2 letters + 1-4 digits. City codes reveal registration location (B=Berlin, M=Munich, HH=Hamburg) |
| **France** | `AB-123-CD` | SIV system (since 2009). Sequential, no regional indicator (though an optional regional logo can appear on the right strip) |
| **Netherlands** | `AB-123-C` | Sidecode system. Format changed over decades; the specific format pattern reveals the approximate year of registration |
| **Poland** | `DW 12345` | 2-3 letter voivodeship/city code + digits/letters. First letters indicate region |
| **Italy** | `AB 123 CD` | Sequential since 1994. Older yellow/white plates with provincial codes still in circulation |
| **Spain** | `1234 BCD` | Four digits + three letters (no vowels, no Q). No regional indicator since 2000 |

**North America:**

| Region | Notes |
|--------|-------|
| **US States** | Each state has unique designs, slogans, and format patterns. State identifiable from plate color, design, and text. Format varies widely (e.g., California: `1ABC234`, New York: `ABC-1234`) |
| **US Specialty/Vanity** | Custom text, military, disabled, government plates have distinct formats per state |
| **Canada** | Provincial plates. Format and design varies by province. Bilingual plates in some provinces |
| **Mexico** | State-issued. Format varies by state and era. Current federal format uses a holographic strip |

**Asia:**

| Country | Notes |
|---------|-------|
| **Japan** | Regional name (in kanji) + classification number + hiragana character + 4-digit number. Green plates = commercial. White plates = private |
| **China** | Provincial abbreviation (Chinese character) + letter (city code) + 5 alphanumeric characters. First character identifies the province |
| **South Korea** | Two digits (vehicle type) + Korean character (region) + four digits |
| **India** | State code (2 letters) + district code (2 digits) + series (1-2 letters) + number (4 digits). Example: `MH 02 AB 1234` (Maharashtra, Mumbai) |

### License Plate Lookup Resources

| Resource | Coverage | Notes |
|----------|----------|-------|
| **FAXVIN** | US | Free VIN and plate lookup |
| **AutoCheck / Carfax** | US/Canada | Paid; vehicle history from plate |
| **DVLA** | UK | Official UK vehicle enquiry (free basic info: make, color, MOT, tax status) |
| **Numberplate.com** | UK | Registration lookup |
| **SIV (ANTS)** | France | Official French vehicle registration |
| **KBA (Kraftfahrt-Bundesamt)** | Germany | German Federal Motor Transport Authority |
| **Platesmania.com** | Global | Crowdsourced license plate photos (searchable by number, country, region) |
| **WorldLicensePlates.com** | Global | Visual reference for plate formats by country |

### Partial Plate Analysis

When only part of a plate is visible (from images, video, dashcam footage):
1. **Identify the country/state** from plate design, color, shape, and any visible text/logos
2. **Determine the format** for that jurisdiction to understand what characters are possible in each position
3. **Note visible characters** and their positions
4. **Calculate possibilities** — each unknown character multiplies possibilities (26 for letters, 10 for digits)
5. **Cross-reference** with vehicle make, model, and color if visible to narrow further
6. **Check multiple frames** — video may show the full plate in a different frame

### What Plates Reveal

| Observable | Intelligence |
|------------|-------------|
| **Country/state design** | Registration jurisdiction |
| **Format pattern** | Approximate registration date (in some countries) |
| **Color coding** | Vehicle type: private, commercial, diplomatic, military, government, temporary |
| **Diplomatic plates** | Country of mission (CD = Corps Diplomatique; number prefix identifies the country) |
| **Temporary/paper plates** | Recently purchased vehicle; dealer information sometimes visible |
| **Vanity/personalized text** | Chosen by owner; may reveal name, interests, or affiliations |

---

## Aircraft Identification

### Key Identifiers

**ICAO 24-bit Address (Hex Code):**
- Unique 6-character hexadecimal identifier assigned to each aircraft transponder (e.g., `A0B1C2`)
- Assigned by national aviation authorities based on the country of registration
- Persists across ownership changes within the same country
- Hex code ranges are allocated by country (e.g., `A00000-AFFFFF` = United States)
- The most reliable identifier for tracking a specific airframe

**Registration Number (Tail Number):**
- The alphanumeric code painted on the aircraft fuselage/tail
- Country prefix identifies the registration state:

| Prefix | Country | Notes |
|--------|---------|-------|
| **N** | United States | Followed by up to 5 characters (digits and letters). Example: `N12345`, `N100AB` |
| **G-** | United Kingdom | Followed by 4 letters. Example: `G-ABCD` |
| **D-** | Germany | Second letter indicates aircraft type: A=single-engine, B=multi-engine, C=rotorcraft, etc. |
| **F-** | France | Second letter indicates category. Example: `F-GKXA` |
| **VH-** | Australia | Followed by 3 letters |
| **C-** | Canada | Followed by 4 letters. Example: `C-GABC` |
| **JA** | Japan | Followed by 4 digits or 3 digits + letter |
| **B-** | China / Taiwan | China uses `B-` + 4 digits; Taiwan uses `B-` + 5 digits |
| **RA-** | Russia | Followed by 5 digits |
| **VT-** | India | Followed by 3 letters |

Full list: ICAO Document 7910 or search "aircraft registration prefix" + country name.

**Callsign:**
- Radio identifier used during flights
- Commercial flights: airline ICAO code + flight number (e.g., `BAW123` = British Airways 123)
- Private/general aviation: often the registration number itself
- Military: tactical callsigns that change per mission

### ADS-B (Automatic Dependent Surveillance-Broadcast)

Most civil aircraft continuously broadcast their position, altitude, speed, heading, and identification via ADS-B:
- **Frequency:** 1090 MHz (Mode S Extended Squitter)
- **Data broadcast:** Position (lat/lon), altitude, groundspeed, heading, vertical rate, callsign, ICAO hex code
- **Range:** Typically 200-400 km from ground receivers (line of sight)
- **Update rate:** Every 0.5 to 2 seconds

**ADS-B data is received by volunteer ground stations worldwide and aggregated by tracking platforms.**

### Tracking Platforms

| Platform | URL | Free Tier | API | Plugin Tool |
|----------|-----|-----------|-----|-------------|
| **OpenSky Network** | opensky-network.org | Full access to live and historical data | Yes (free, rate-limited) | `query_flightradar.py` references OpenSky data |
| **FlightRadar24** | flightradar24.com | Live tracking; limited history | Paid API | `query_flightradar.py` |
| **FlightAware** | flightaware.com | Live tracking; limited history | Paid (free tier available) | N/A |
| **ADS-B Exchange** | adsbexchange.com | Full unfiltered data (no military filtering) | Yes | N/A |
| **Planespotters.net** | planespotters.net | Aircraft photos and registration database | N/A | N/A |

**Plugin Tool: `query_flightradar.py`**
```
uv run skills/osint/scripts/query_flightradar.py <identifier>
```
Query flight tracking data using registration, callsign, or ICAO hex code.

### Military and Government Aircraft

- Many military aircraft do **not broadcast ADS-B** or use filtered/restricted transponder modes
- Some military aircraft appear on ADS-B Exchange but are filtered from FlightRadar24 and FlightAware
- **Squawk codes** of interest:
  - `7700` = Emergency
  - `7600` = Radio failure
  - `7500` = Hijack
  - `0000` = Often used by military or when code is not assigned
- Government/VIP aircraft often use **LADD** (Limiting Aircraft Data Displayed) in the US to block tracking
- Tail numbers for US military: serial number format (e.g., `85-0001`), not N-numbers
- Track military aircraft via: ADS-B Exchange (unfiltered), monitoring social media accounts like @AircraftSpots, Scramble.nl military database

### Airport Codes

| System | Format | Example | Usage |
|--------|--------|---------|-------|
| **ICAO** | 4 letters | EGLL, KJFK, LFPG | Aviation operations, flight plans, ADS-B data |
| **IATA** | 3 letters | LHR, JFK, CDG | Commercial airlines, passenger bookings |

Common pairings: EGLL/LHR (London Heathrow), KJFK/JFK (New York JFK), LFPG/CDG (Paris Charles de Gaulle), EDDF/FRA (Frankfurt), RJTT/HND (Tokyo Haneda).

ICAO codes follow a regional scheme: E = Northern Europe, K = Contiguous US, L = Southern Europe, R = East Asia, etc.

---

## Ship Identification

### Key Identifiers

**MMSI (Maritime Mobile Service Identity):**
- 9-digit number assigned to a ship's radio equipment
- First 3 digits = MID (Maritime Identification Digits) = flag state

| MID Range | Flag State Examples |
|-----------|-------------------|
| 201-279 | Europe (e.g., 211 = Germany, 226/227 = France, 230 = Finland, 235-237 = UK, 244 = Netherlands, 245 = Netherlands, 246 = Netherlands) |
| 301-399 | Americas (e.g., 303 = USA (Alaska), 338 = USA, 316 = Canada) |
| 401-499 | Asia (e.g., 412 = China, 431 = Japan, 440 = South Korea, 470 = Bangladesh) |
| 501-599 | Oceania/Africa (e.g., 503 = Australia, 512 = New Zealand) |
| 601-699 | Africa (e.g., 601 = South Africa) |

Full MID table: ITU Maritime Identification Digits database.

**IMO Number:**
- 7-digit permanent identifier assigned by the International Maritime Organization
- Prefixed with "IMO" (e.g., IMO 1234567)
- Does NOT change when the ship changes name, flag, or owner
- The most reliable way to track a specific vessel across ownership and flag changes
- Includes a check digit (last digit) for validation

**Callsign:**
- Radio call sign assigned by the flag state
- Format varies by country (e.g., US ships often start with W or K)
- Used for radio communication and identification

### AIS (Automatic Identification System)

Ships above 300 gross tons on international voyages (and all passenger ships) are required to broadcast AIS:
- **Data broadcast:** MMSI, position, course, speed, heading, rate of turn, destination, ETA, cargo type, ship dimensions
- **Class A:** Required for large vessels; higher power, more frequent updates
- **Class B:** Voluntary for smaller vessels; lower power, less frequent
- **Update rate:** Every 2-10 seconds (underway), every 3 minutes (at anchor)

**AIS deliberately turned off:** Ships can disable their AIS transponders. This is a significant indicator in OSINT investigations (sanctions evasion, illicit transfers, military operations). Known as "going dark."

### Ship Tracking Platforms

| Platform | URL | Free Tier | Notes |
|----------|-----|-----------|-------|
| **MarineTraffic** | marinetraffic.com | Live tracking; limited history | Most comprehensive global AIS database |
| **VesselFinder** | vesselfinder.com | Live tracking; limited history | Good free tier with vessel photos |
| **Fintraffic (formerly Digitraffic)** | digitraffic.fi | Full access to Finnish waters | Free API with real-time AIS data for vessels in Finnish waters |
| **MyShipTracking** | myshiptracking.com | Live tracking | Alternative tracker with good coverage |
| **ShipXplorer** | shipxplorer.com | Live tracking | Community-based AIS data sharing |

**Plugin script:** Use `uv run query_ais.py` for vessel tracking via Fintraffic AIS (Baltic Sea coverage). Subcommands: `search <name>`, `mmsi <number>`, `location <mmsi>`.

### Flag State Intelligence

A ship's flag state (country of registration) is significant for OSINT:
- **Flag of convenience** countries (Panama, Liberia, Marshall Islands, Bahamas) offer low regulation and fees
- Flag state determines which jurisdiction's maritime law applies
- Ships frequently re-flag to avoid sanctions or regulations
- IMO number persistence allows tracking across flag changes

### Ship Types and Cargo Indicators

AIS broadcasts include a ship type code:

| Code Range | Ship Type |
|------------|-----------|
| 20-29 | Wing In Ground (WIG) craft |
| 30 | Fishing vessel |
| 31-32 | Towing vessels |
| 33 | Dredging/underwater operations |
| 34 | Diving operations |
| 35 | Military operations |
| 36 | Sailing vessel |
| 37 | Pleasure craft |
| 40-49 | High-speed craft |
| 50 | Pilot vessel |
| 51 | Search and rescue vessel |
| 52 | Tug |
| 53 | Port tender |
| 55 | Law enforcement |
| 58 | Medical transport |
| 60-69 | Passenger ships |
| 70-79 | Cargo ships |
| 80-89 | Tankers |

---

## Vehicle Identification Number (VIN)

### VIN Structure (17 Characters)

```
W B A 3 A 5 C 5 9 F F 1 2 3 4 5 6
│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
│ │ │ └─┴─┴─┴─┘ └─┴─┴─┴─┴─┴─┴─┴─┘
│ │ │    VDS         VIS
│ └─┘
│ WMI
└────────────────────────────────────
```

**WMI (World Manufacturer Identifier) - Characters 1-3:**
- **Character 1:** Country of manufacture

| Code | Country |
|------|---------|
| 1, 4, 5 | United States |
| 2 | Canada |
| 3 | Mexico |
| J | Japan |
| K | South Korea |
| L | China |
| S | United Kingdom |
| V | France/Spain |
| W | Germany |
| Z | Italy |
| 9 (9A-9E) | Brazil |

- **Characters 2-3:** Manufacturer identifier

| WMI | Manufacturer |
|-----|-------------|
| WBA | BMW (Germany) |
| WDB | Mercedes-Benz (Germany) |
| WVW | Volkswagen (Germany) |
| WAU | Audi (Germany) |
| JTD | Toyota (Japan) |
| JHM | Honda (Japan) |
| 1G1 | Chevrolet (US) |
| 1FA | Ford (US) |
| 5YJ | Tesla (US) |
| ZFF | Ferrari (Italy) |

**VDS (Vehicle Descriptor Section) - Characters 4-8:**
- Encodes vehicle attributes: model, body type, engine type, transmission, restraint system
- Encoding varies by manufacturer (each OEM defines their own VDS scheme)
- Combined with WMI, these 8 characters uniquely identify the vehicle configuration

**Check Digit - Character 9:**
- Calculated from all other characters using a weighted algorithm
- Used to detect transcription errors and VIN fraud
- Valid values: 0-9 and X

**VIS (Vehicle Identifier Section) - Characters 10-17:**
- **Character 10:** Model year code

| Code | Year | Code | Year |
|------|------|------|------|
| A | 2010 | J | 2018 |
| B | 2011 | K | 2019 |
| C | 2012 | L | 2020 |
| D | 2013 | M | 2021 |
| E | 2014 | N | 2022 |
| F | 2015 | P | 2023 |
| G | 2016 | R | 2024 |
| H | 2017 | S | 2025 |

Note: The cycle repeats every 30 years (codes I, O, Q, U, Z are never used).

- **Character 11:** Manufacturing plant code (manufacturer-specific)
- **Characters 12-17:** Sequential production number

### VIN Lookup Resources

| Resource | Coverage | Notes |
|----------|----------|-------|
| **NHTSA VIN Decoder API** | US-market vehicles | Free, official US government API. `https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{VIN}?format=json` |
| **NHTSA Complaints/Recalls** | US-market vehicles | Search safety complaints and recalls by VIN |
| **VINDecoder.net** | Global | Free decoder with build sheet information |
| **Carfax / AutoCheck** | US/Canada | Paid vehicle history (accidents, owners, mileage) |
| **EpicVIN** | US | Free basic VIN check |

---

## Object Identification from Images

### Military Equipment Identification

**Oryx Methodology:**
Oryx (oryxspioenkop.com) pioneered the practice of visually confirmed military equipment tracking. Their methodology requires:
1. Photographic or video evidence of each individual piece of equipment
2. Evidence of status (destroyed, damaged, abandoned, captured)
3. De-duplication — confirming each item is counted only once
4. Geolocation when possible
5. Cross-referencing multiple sources for the same incident

**Resources for military equipment ID:**

| Resource | Coverage |
|----------|----------|
| **IISS Military Balance** | Comprehensive global military equipment database |
| **Jane's (IHS Markit)** | Professional defense intelligence (paid) |
| **Deagel.com** | Military equipment specifications and inventories |
| **Wikipedia weapon infoboxes** | Surprisingly detailed; good for quick visual reference |
| **r/MilitaryPorn, r/TankPorn** | Community identification of equipment from images |
| **Armament Research Services (ARES)** | Weapon identification and tracing |

**Identification from images:**
- Silhouette comparison (turret shape, hull profile for vehicles)
- Dimensional analysis (track width, barrel length ratios)
- Markings and camouflage patterns (indicate country/unit)
- Unique features (reactive armor patterns, antenna configurations, optics)

### Weapon Identification

- **ARES (Armament Research Services):** Professional weapon identification and tracing
- **Small Arms Survey:** Database of small arms by type and origin
- **Caliber and cartridge identification** from spent casings in images
- **Serial number placement** varies by manufacturer; can be researched for provenance
- **Conflict Armament Research:** Tracks weapons in conflict zones

### Vehicle Make/Model from Partial Views

When only part of a vehicle is visible in an image:

| Visible Feature | Identification Method |
|----------------|----------------------|
| **Badge/emblem** | Manufacturer logo — search by shape if unfamiliar |
| **Tail lights** | Unique per model; search image databases for shape matches |
| **Headlights** | Shape and LED patterns are model-specific |
| **Grille pattern** | Manufacturer-specific (BMW kidney grille, Jeep 7-slot, etc.) |
| **Wheel design** | OEM wheels are model-specific; aftermarket narrows less |
| **Dashboard/interior** | Steering wheel and instrument cluster identify make/model |
| **Body lines/profile** | Roofline, shoulder line, C-pillar shape |
| **Side mirrors** | Shape varies by manufacturer |
| **Bumper design** | Unique per model and model year |

**Strategy:** Identify any visible unique feature, then use Google Lens or Gemini AI to search for visual matches. Provide the AI with specific observations ("sedan with split LED tail lights, chrome strip across trunk") for best results.

### Using AI for Visual Identification

Gemini (via the `gemini` MCP tool) can assist with:
```
ask_question_about_video(file_path="/path/to/image.jpg", question="What vehicle make and model is shown? Identify any visible markings, badges, or distinctive features.")
```

Effective prompts for object identification:
- "What type of military vehicle is this? Note any markings, camouflage pattern, or equipment visible."
- "Identify the aircraft type from this image. Note the engine configuration, wing shape, and any visible registration."
- "What ship type is this? Estimate the size and identify any visible name, IMO number, or flag."
- "Identify the weapon/firearm type. Note the caliber, manufacturer markings, and any modifications."

---

## Common Analysis Workflows

### Workflow: Aircraft Investigation

1. **Identify the aircraft** from image/video (registration, type, livery) or from ADS-B data (hex code, callsign)
2. **Look up registration** — `query_flightradar.py` or OpenSky Network API to find the registered owner
3. **Track flight history** — Historical ADS-B data shows where the aircraft has been
4. **Registration database** — FAA N-number lookup (US), CAA G-INFO (UK), or national aviation authority
5. **Ownership chain** — Aircraft registrations are public record; trace through sales and re-registrations
6. **Cross-reference** — Compare flight patterns with known events, locations of interest, other investigations
7. **Document in knowledge graph** — Link aircraft to owner, operator, routes, and events

### Workflow: Ship Investigation

1. **Identify the vessel** from image (name on hull, IMO number) or from AIS data (MMSI)
2. **Look up IMO number** — Permanent identifier; search on MarineTraffic or IMO Ship Identification Number Search
3. **Track AIS history** — Historical position data shows ports visited and routes taken
4. **Flag state and ownership** — Equasis (equasis.org, free registration) provides flag, class, owner, and manager
5. **Check for dark periods** — Gaps in AIS data may indicate transponder was turned off
6. **Port call history** — Which ports has the vessel visited? Any sanctioned ports?
7. **Sanctions check** — Cross-reference vessel, owner, and flag state against OFAC, EU, and UN sanctions lists
8. **Document findings** — Record vessel details, ownership chain, and suspicious patterns

### Workflow: Vehicle from Image

1. **Extract visible identifiers** — License plate (full or partial), make/model badges, VIN (if visible through windshield)
2. **Identify country/state** from plate design and format
3. **Run plate lookup** if full plate is visible and a lookup service exists for that jurisdiction
4. **Identify make/model** from visible features (use AI if needed)
5. **VIN decode** if available — reveals manufacturer, model, year, and production details
6. **Cross-reference** — Match vehicle details with other evidence in the investigation
7. **Geolocation** — Use visible surroundings to determine where the image was taken (see `geolocation.md`)

---

## Cross-References

- `geolocation.md` — Determining where images/videos were taken from visual clues
- `image-video-forensics.md` — EXIF extraction, frame analysis, and evidence preservation
- `tool-guide.md` — Full reference for `query_flightradar.py` and other plugin tools
- `open-apis.md` — API endpoints for NHTSA VIN decoder and other free services
- `knowledge-graph.md` — Entity schema for recording vehicles, aircraft, ships, and their relationships
- `opsec-ethics.md` — Ethical guidelines for tracking and surveillance investigations

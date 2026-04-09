# Challenge: Airport Traffic Pattern Analysis

## Domain
Transportation (Aviation Intelligence)

## Difficulty
Hard

## Scenario
"I'm an investigative journalist monitoring London Heathrow Airport (ICAO: EGLL). I need a comprehensive analysis of arrival and departure patterns over the last 24 hours. Specifically, I want to know: (1) the total volume of flights in and out, (2) which hours were busiest, (3) whether there are any flights from unusual or noteworthy origins, (4) whether any private, charter, or government/military aircraft are present in the data, and (5) a breakdown of the major airlines operating. Pull the traffic data and give me a structured intelligence briefing I can use for my reporting."

## Expected Approach
1. **Pull arrival data for EGLL** -- `query_flightradar.py arrivals EGLL`:
   - Retrieve all arrivals at London Heathrow over the last 24 hours
   - The API returns flight records with ICAO24, callsign, departure airport, arrival airport, and timestamps
   - Note the `flight_count` in the response for total arrival volume
   - Record `first_seen` and `last_seen` timestamps for temporal analysis

2. **Pull departure data for EGLL** -- `query_flightradar.py departures EGLL`:
   - Retrieve all departures from London Heathrow over the last 24 hours
   - Note total departure count
   - Record timestamps for busiest-hour analysis
   - Cross-reference with arrivals to get total flight volume

3. **Analyze total flight volume** -- Combine arrival and departure counts:
   - Sum arrival and departure counts for total operations
   - Heathrow typically handles 1,200-1,400 daily movements
   - Compare observed count against expected volume to flag anomalies

4. **Identify busiest hours** -- Group flights by hour using `first_seen`/`last_seen` timestamps:
   - Convert Unix timestamps to hourly buckets
   - Identify peak arrival and departure hours
   - Heathrow typically has morning arrival peaks (06:00-09:00) and evening departure peaks (17:00-20:00)
   - Note the night-time curfew at Heathrow (23:30-04:30 restricted)

5. **Analyze callsign patterns to classify traffic** -- Parse callsigns from the data:
   - **Commercial airlines** use ICAO airline codes as callsign prefixes:
     - BAW = British Airways, DLH = Lufthansa, UAE = Emirates, AAL = American Airlines, SIA = Singapore Airlines, QTR = Qatar Airways, AFR = Air France, THY = Turkish Airlines
   - **Private/charter aircraft** often use registration-based callsigns (e.g., G-XXXX for UK registrations, N-XXXX for US) or business aviation codes (e.g., EJM = NetJets, VJT = VistaJet)
   - **Military/government aircraft** may use distinctive callsigns: RRR (Royal Air Force), RCH (USAF AMC Reach flights), SAM (Special Air Mission), EXEC, or numeric-only callsigns
   - Flag any callsigns that do not match known commercial airline ICAO codes

6. **Identify flights from unusual origins** -- Examine `departure_airport` (for arrivals) and `arrival_airport` (for departures):
   - Flag flights from airports in conflict zones, sanctioned countries, or unusual routing
   - Note any flights from small/private airfields rather than major commercial airports
   - Identify any airport codes that are less common at Heathrow

7. **Compile structured intelligence briefing** -- Present findings in a structured format:
   - Executive summary: total operations, date/time range
   - Traffic volume analysis: arrivals vs departures, hourly distribution
   - Airline breakdown: top operators by flight count
   - Flights of interest: private/charter, military, unusual origins
   - Anomalies or notable patterns

## Verification
- [ ] Successfully pulls arrival data from `query_flightradar.py arrivals EGLL`
- [ ] Successfully pulls departure data from `query_flightradar.py departures EGLL`
- [ ] Calculates and presents total flight volume (arrivals + departures)
- [ ] Performs temporal analysis grouping flights by hour
- [ ] Classifies callsigns into commercial, private/charter, and military/government categories
- [ ] Identifies the top airlines by flight count
- [ ] Flags any flights from unusual or noteworthy origins
- [ ] Presents findings in a structured intelligence briefing format

## Ground Truth

<details>
<summary>Click to reveal</summary>

**London Heathrow (EGLL) baseline:**
- EGLL is the UK's busiest airport and one of the busiest in Europe
- Typically handles 1,200-1,400 daily aircraft movements (600-700 arrivals, 600-700 departures)
- Two parallel runways operating in segregated mode (one for arrivals, one for departures, swapping at 15:00 local)
- Night curfew: 23:30-04:30 with limited exceptions
- Dominated by British Airways (BAW) which operates ~50% of all Heathrow slots
- Major long-haul hub with flights from all continents

**Callsign classification guide:**
- Commercial ICAO prefixes commonly seen at EGLL: BAW (British Airways), VIR (Virgin Atlantic), UAE (Emirates), QTR (Qatar), SIA (Singapore), CPA (Cathay Pacific), DLH (Lufthansa), AFR (Air France), AAL (American), UAL (United), DAL (Delta), THY (Turkish), ETH (Ethiopian), AIC (Air India)
- Private/business aviation codes: EJM (NetJets Europe), VJT (VistaJet), TAG (TAG Aviation), LNX (Lynx Aviation), or callsigns matching aircraft registrations (G-XXXX, N-XXXXX, VP-XXX, 9H-XXX)
- Military/government: RRR (RAF), RCH (USAF Reach), ASY (RAF Ascot), KRF (French Air Force Cotam)
- Empty or null callsigns in the data should be flagged as they may indicate transponder issues or deliberate obscuration

**Analysis methodology:**
- The OpenSky API returns Unix timestamps; convert to UTC for hourly bucketing
- Group `first_seen` timestamps for departures and `last_seen` timestamps for arrivals
- The `departure_airport` field on arrivals shows the origin; null values indicate the origin could not be determined
- The `arrival_airport` field on departures shows the destination
- ICAO24 hex codes can be cross-referenced against aircraft registration databases for further identification

**What makes this Hard:**
- Requires not just data retrieval but analytical processing of the results
- Callsign classification requires domain knowledge of airline ICAO codes
- Distinguishing routine traffic from noteworthy flights requires judgment
- Temporal analysis requires timestamp conversion and grouping
- A comprehensive briefing requires synthesizing multiple data dimensions

**Scoring:**
- **Score 5 if:** Agent pulls both arrivals and departures, calculates total volume, performs hourly distribution analysis, classifies callsigns into commercial/private/military categories with specific airline identifications, flags noteworthy flights, and delivers a structured intelligence briefing with actionable findings
- **Score 4 if:** Agent retrieves all data, provides volume and airline breakdown, and identifies at least some non-commercial traffic, but the temporal or structural analysis is incomplete
- **Score 3 if:** Agent pulls the data successfully and provides basic volume counts and airline identification, but lacks deeper analytical layers (temporal patterns, traffic classification, anomaly detection)
- **Score 2 if:** Agent pulls arrival or departure data but not both, and provides only surface-level summary without analytical breakdown
- **Score 1 if:** Agent describes what should be done but does not execute the flight tracking scripts or provides no structured analysis

</details>

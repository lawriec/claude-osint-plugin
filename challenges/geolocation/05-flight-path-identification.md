# Challenge: Flight Path Identification

## Domain
Geolocation (Aviation)

## Difficulty
Medium

## Scenario
"I was standing outside near Frankfurt, Germany (roughly 50.0379 N, 8.5622 E) around 14:00 UTC today when I spotted a large aircraft at low altitude. It had a white fuselage and a distinctive blue tail with what looked like a crane or heron logo. Can you help me figure out which airline that is, what airport it was likely coming from or going to, and whether you can find any aircraft currently operating in this area? I'd love to know the specific flights that might match what I saw."

## Expected Approach
1. **Identify the airline from livery description** -- White fuselage with a blue tail featuring a crane/heron logo:
   - The crane logo on a blue tail is the hallmark of Lufthansa (Deutsche Lufthansa AG)
   - Lufthansa's ICAO code is DLH; IATA code is LH
   - The stylized crane has been Lufthansa's logo since 1918

2. **Identify the nearest airport** -- Coordinates 50.0379, 8.5622 place the observer near Frankfurt:
   - Frankfurt Airport (ICAO: EDDF, IATA: FRA) is the primary airport in this area
   - EDDF is Lufthansa's largest hub, making a Lufthansa sighting highly expected
   - Aircraft at low altitude near these coordinates are almost certainly on approach to or departure from EDDF

3. **Query live aircraft in the Frankfurt area** -- `query_flightradar.py states --bbox 49.5,8.0,50.5,9.0`:
   - The bounding box covers the Frankfurt airport area with margin
   - Look for aircraft with Lufthansa callsigns (DLH prefix, e.g. DLH1234)
   - Note altitude, velocity, and heading to determine approach vs departure
   - Filter for aircraft at low altitude (< 3000m) consistent with the observer's description

4. **Pull EDDF arrival data** -- `query_flightradar.py arrivals EDDF`:
   - Retrieve arrivals over the default 24-hour window
   - Filter for flights with Lufthansa callsigns (DLH prefix)
   - Identify origin airports to determine where the aircraft may have come from
   - Look for flights arriving around 14:00 UTC

5. **Pull EDDF departure data** -- `query_flightradar.py departures EDDF`:
   - Retrieve departures over the default 24-hour window
   - Cross-reference Lufthansa departures around the same timeframe
   - An aircraft at low altitude could be either arriving or recently departed

6. **Track a specific aircraft** (if a candidate ICAO24 is identified) -- `query_flightradar.py track <icao24>`:
   - Retrieve the flight track waypoints for the candidate aircraft
   - Confirm the flight path passes over or near 50.0379, 8.5622
   - Determine origin and destination from the track data

7. **Compile findings** -- Correlate livery identification, airport data, and live tracking:
   - Confirm airline as Lufthansa
   - Identify EDDF as the airport
   - Present candidate flights with origins/destinations

## Verification
- [ ] Correctly identifies Lufthansa from the crane logo description
- [ ] Identifies Frankfurt Airport (EDDF/FRA) as the nearest major airport
- [ ] Successfully runs `query_flightradar.py states --bbox` for the Frankfurt area
- [ ] Successfully runs `query_flightradar.py arrivals EDDF`
- [ ] Successfully runs `query_flightradar.py departures EDDF`
- [ ] Filters results for Lufthansa callsigns (DLH prefix)
- [ ] Identifies candidate flights near 14:00 UTC
- [ ] Presents a coherent assessment linking livery, location, and flight data

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Airline identification:**
- The white fuselage with blue tail and crane logo is **Lufthansa**
- The stylized crane (Kranich) has been Lufthansa's symbol since 1918
- ICAO code: DLH, IATA code: LH
- Headquarters: Cologne; primary hub: Frankfurt Airport (EDDF)

**Airport identification:**
- Coordinates 50.0379, 8.5622 are approximately 10 km from Frankfurt Airport
- EDDF (Frankfurt am Main) is the busiest airport in Germany and Lufthansa's largest hub
- Lufthansa operates hundreds of daily flights from EDDF to destinations worldwide
- An aircraft at low altitude in this area is almost certainly associated with EDDF operations

**OpenSky API verification:**
- `query_flightradar.py states --bbox 49.5,8.0,50.5,9.0` should return aircraft currently in the Frankfurt airspace
- Lufthansa flights will have callsigns starting with "DLH" (e.g., DLH400, DLH900)
- `query_flightradar.py arrivals EDDF` and `departures EDDF` return flight records with origin/destination airports
- Note: OpenSky anonymous API is rate-limited (~100 requests/day); results depend on current traffic

**Scoring:**
- **Score 5 if:** Agent correctly identifies Lufthansa from the livery, identifies EDDF as the airport, uses all three query types (states bbox, arrivals, departures), filters for DLH callsigns, and presents candidate flights with origin/destination analysis
- **Score 4 if:** Agent identifies Lufthansa and EDDF, uses at least two query types, and provides flight analysis
- **Score 3 if:** Agent identifies Lufthansa and EDDF, runs at least one OpenSky query, but analysis is incomplete
- **Score 2 if:** Agent identifies the airline and airport but does not use the flight tracking scripts
- **Score 1 if:** Agent identifies only one of the airline or airport and does not query live data

</details>

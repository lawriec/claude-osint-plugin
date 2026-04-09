# Challenge: Vessel Identification from Port Clues

## Domain
Transportation (Maritime OSINT)

## Difficulty
Medium

## Scenario
"An intelligence report mentions a large passenger ferry operating a regular service between Helsinki, Finland and Stockholm, Sweden in the Baltic Sea. The vessel is described as having a distinctive blue and white hull. It was last observed departing Helsinki on a regular evening service. I need to identify which shipping line operates this route, find the specific vessel name and its MMSI number, and determine its current position or last known location. Can you investigate this using available maritime tracking data?"

## Expected Approach
1. **Identify operators on the Helsinki-Stockholm route** -- Research known ferry operators:
   - Viking Line operates Helsinki-Stockholm with vessels including Viking Grace (built 2013) and Viking Glory (built 2022)
   - Tallink/Silja Line also operates this route with vessels like Silja Serenade and Silja Symphony
   - The "blue and white hull" description is consistent with Viking Line's livery
   - Viking Line vessels depart Helsinki in the evening for overnight crossings to Stockholm

2. **Search for Viking Line vessels in AIS data** -- `query_ais.py search "Viking"`:
   - Search the Fintraffic AIS database for vessels with "Viking" in the name
   - The Fintraffic API covers the Baltic Sea region, which is exactly where these ferries operate
   - Expect to find Viking Grace, Viking Glory, and possibly other Viking Line vessels
   - Note the MMSI numbers returned for each vessel

3. **Look up vessel metadata by MMSI** -- `query_ais.py mmsi 230629000` (Viking Grace) or similar:
   - Retrieve detailed vessel information including ship type, callsign, IMO number, destination, and ETA
   - Confirm the vessel is a passenger ferry (ship type)
   - Check the reported destination field for Stockholm or Helsinki

4. **Get current vessel location** -- `query_ais.py location 230629000`:
   - Retrieve the vessel's current GPS coordinates, speed over ground (SOG), course over ground (COG), and heading
   - Determine whether the vessel is currently en route, in port at Helsinki, or in port at Stockholm
   - The response includes a Google Maps URL for easy position visualization

5. **Search for Tallink/Silja as an alternative** -- `query_ais.py search "Silja"`:
   - Also search for the competing operator on this route
   - Compare vessel details to narrow down which specific vessel matches the report's description
   - Tallink/Silja vessels have a different livery (red and white), helping to confirm Viking Line

6. **Compile maritime intelligence report** -- Correlate all findings:
   - Identify the operator and specific vessel
   - Present MMSI, IMO, callsign, and current position
   - Assess whether the vessel's current location is consistent with the reported evening departure from Helsinki

## Verification
- [ ] Identifies Viking Line as the primary operator matching the description
- [ ] Successfully runs `query_ais.py search` for relevant vessel names
- [ ] Retrieves at least one valid MMSI number for a Helsinki-Stockholm ferry
- [ ] Successfully runs `query_ais.py mmsi` to get vessel metadata
- [ ] Successfully runs `query_ais.py location` to get current position
- [ ] Distinguishes between Viking Line and Tallink/Silja Line based on livery description
- [ ] Presents a coherent identification linking the description to a specific vessel

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Route and operators:**
- The Helsinki-Stockholm ferry route is one of the busiest in the Baltic Sea
- Two main operators: **Viking Line** and **Tallink/Silja Line**
- Viking Line vessels have a blue and white livery matching the description
- Tallink/Silja Line vessels have a red and white livery (does not match)

**Viking Line vessels on this route:**
- **Viking Grace** -- MMSI: 230629000, IMO: 9606900, built 2013, LNG-powered
- **Viking Glory** -- MMSI: 230985000, IMO: 9827852, built 2022, LNG-powered
- Both operate the Helsinki-Mariehamn-Stockholm route
- Evening departures from Helsinki typically around 17:00-17:30 local time, arriving Stockholm next morning

**Tallink/Silja Line vessels (for comparison):**
- Silja Serenade -- MMSI: 230145000, operates Helsinki-Mariehamn-Stockholm
- Silja Symphony -- MMSI: 230140000, operates same route
- These have distinct red/white Tallink Silja branding

**AIS data notes:**
- The Fintraffic AIS API has strong Baltic Sea coverage, making it ideal for tracking these ferries
- Vessel search is a client-side substring match across all vessels in the database
- Location data includes coordinates, SOG, COG, heading, and navigation status
- A vessel departing Helsinki in the evening should show a westward course (COG ~250-280 degrees) through the archipelago

**Scoring:**
- **Score 5 if:** Agent identifies Viking Line from the livery description, finds the specific vessel(s) via AIS search, retrieves MMSI and metadata, gets current location, and differentiates from Tallink/Silja Line with reasoning
- **Score 4 if:** Agent identifies the correct operator and vessel, uses at least two AIS query types, and provides location data
- **Score 3 if:** Agent identifies Viking Line and runs AIS searches but does not retrieve location data or misses vessel details
- **Score 2 if:** Agent identifies the correct route and operator but does not use the AIS tracking scripts
- **Score 1 if:** Agent provides only general knowledge about the route without using maritime tracking tools

</details>

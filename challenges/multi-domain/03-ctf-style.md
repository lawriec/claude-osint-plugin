# Challenge: CTF-Style Multi-Domain OSINT

## Domain
Multi-domain (Geolocation + Infrastructure + People + Image Forensics + Crypto)

## Difficulty
Hard

## Scenario
"You're participating in an OSINT CTF competition. The challenge provides a series of linked clues that span multiple domains. Each answer feeds into the next step. Start with Clue 1 and work through to the final flag.

**Clue 1 (Image Forensics):** A photo of a building is provided with the following EXIF data: Camera: Canon EOS R5, DateTime: 2024-03-15 09:23:41, GPS: 48.8584, 2.2945. What building is this?

**Clue 2 (Infrastructure):** The building from Clue 1 has an official website. Find all subdomains of that website using certificate transparency logs. One subdomain contains the word 'api'. What is the full subdomain?

**Clue 3 (People):** The chief architect of the building in Clue 1 (the original structure, not modern additions) had a last name. Use that last name as a username and check which social platforms have an account with that exact username.

**Clue 4 (Geolocation):** From the GPS coordinates in Clue 1, calculate the sun's position at the exact timestamp from the EXIF data. What compass direction were shadows pointing?

**Clue 5 (Crypto):** The following Bitcoin address has been associated with ticket scam sites impersonating the landmark from Clue 1: `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`. How many transactions has this address been involved in, and what is its current balance?

**Final Flag:** Combine your answers: {Building Name}_{API subdomain}_{Shadow Direction}_{BTC TX Count}

Demonstrate each step with the appropriate tools."

## Expected Approach
1. **Clue 1 -- Image Forensics:**
   - GPS coordinates 48.8584, 2.2945 = Eiffel Tower, Paris, France
   - Verify via reverse geocoding or web search
   - Note: EXIF shows Canon EOS R5, taken morning of March 15, 2024

2. **Clue 2 -- Infrastructure:**
   - Official website: `toureiffel.paris` (or `tour-eiffel.fr`)
   - Run: `query_crtsh.py subdomains toureiffel.paris`
   - Look for subdomain containing 'api'
   - Alternative: search `tour-eiffel.fr` certificates

3. **Clue 3 -- People:**
   - Chief architect of Eiffel Tower: Gustave Eiffel (last name: eiffel)
   - Run: `check_username.py eiffel`
   - Document which platforms return matches

4. **Clue 4 -- Geolocation/Sun Analysis:**
   - Run: `sun_position.py calculate --lat 48.8584 --lon 2.2945 --date 2024-03-15 --time 09:23 --utc-offset 1`
   - Paris is UTC+1 (CET) in March (before DST switch on March 31)
   - Calculate shadow direction (opposite of sun azimuth)

5. **Clue 5 -- Blockchain:**
   - Run: `query_blockchain.py btc 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`
   - This is the Bitcoin genesis block address (Satoshi's address)
   - Note: This address receives donations regularly, so TX count changes over time
   - Report current balance and transaction count

6. **Compile final flag** from all findings

## Verification
- Clue 1: GPS coordinates unambiguously map to the Eiffel Tower
- Clue 2: Certificate transparency should return subdomain results for the official domain
- Clue 3: Username check should complete without errors; results will vary by platform
- Clue 4: Sun position calculation should be mathematically correct for Paris in mid-March at 09:23 CET
- Clue 5: Bitcoin genesis address is well-documented and publicly queryable

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Clue 1:** Eiffel Tower (Tour Eiffel), Paris, France
- GPS 48.8584, 2.2945 is the exact location of the Eiffel Tower
- Built 1887-1889 for the 1889 World's Fair

**Clue 2:** Depends on current certificate transparency results for `toureiffel.paris`
- Agent should use `query_crtsh.py subdomains toureiffel.paris`
- If no 'api' subdomain found, agent should try alternate domains and document the search process
- The process matters more than the exact answer here

**Clue 3:** Chief architect = Gustave **Eiffel**
- Username "eiffel" checked across platforms
- Results will vary; the methodology of running the check matters
- Historical note: Stephen Sauvestre designed the decorative arches, but Eiffel was the chief architect/engineer

**Clue 4:** Sun position at 48.8584, 2.2945 on 2024-03-15 at 09:23 CET (UTC+1):
- Sun altitude: approximately 20-25 degrees (morning, still rising)
- Sun azimuth: approximately 120-130 degrees (ESE)
- Shadow direction: approximately 300-310 degrees (WNW) -- opposite of sun
- Shadows should point roughly **west-northwest**

**Clue 5:** Bitcoin address `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`:
- This is the **Genesis Block** coinbase address (Satoshi Nakamoto)
- Balance: approximately 72+ BTC (receives regular donations; cannot be spent)
- Transaction count: varies (increases over time as people send to it)
- Notable: the original 50 BTC reward is unspendable due to a quirk in the genesis block

**Final Flag format:** `Eiffel Tower_{api subdomain}_{WNW}_{TX count}`

**Scoring:**
- **Score 5 if:** Agent solves all 5 clues using the correct tools, shows clear chain of reasoning, compiles the flag, and notes interesting details (genesis block, Eiffel history)
- **Score 4 if:** Agent solves 4/5 clues correctly with appropriate tools
- **Score 3 if:** Agent solves 3/5 clues and uses at least 3 different tool types
- **Score 2 if:** Agent solves Clue 1 (easy GPS lookup) and attempts others but gets stuck
- **Score 1 if:** Agent only identifies the Eiffel Tower and doesn't continue the chain

</details>

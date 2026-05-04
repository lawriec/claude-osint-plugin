# Challenge: Wikidata Entity Resolution

## Domain
People (Entity Disambiguation / Knowledge Graph)

## Difficulty
Easy

## Scenario
"A journalist is writing a profile piece about the investigative organization Bellingcat and needs structured data about it. The problem is that searching for 'Bellingcat' and its founder 'Eliot Higgins' returns multiple results in various databases, and the journalist needs to disambiguate the correct entities, pull structured biographical and organizational data from Wikidata, and map out the relationships between Bellingcat and related people and organizations. Can you use Wikidata to find the correct entities, retrieve their properties, identify connected entities (founder, members, notable investigations), and cross-reference with web search to verify the data is current?"

## Expected Approach
1. **Entity search for the organization** -- Run `query_wikidata_sparql.py entity` to find candidates:
   - `uv run query_wikidata_sparql.py entity "Bellingcat" --limit 5`
   - Review all returned results: each will have a QID, label, description, and aliases
   - Identify the correct entity by matching the description (should reference investigative journalism or open-source intelligence)
   - Note the QID for Bellingcat (expected: Q24034552 or similar)
2. **Entity search for the founder** -- Disambiguate Eliot Higgins:
   - `uv run query_wikidata_sparql.py entity "Eliot Higgins" --limit 5`
   - Multiple people may share this name; identify the correct one by description (should reference Bellingcat, citizen journalism, or OSINT)
   - Note the QID for the correct Eliot Higgins (expected: Q15999820 or similar)
3. **Retrieve organization properties** -- Get structured data for Bellingcat:
   - `uv run query_wikidata_sparql.py properties <bellingcat_qid>`
   - Look for: instance of (investigative journalism organization), country, headquarters location, official website, founding date, founder, social media accounts
   - These properties provide verified structured data that can anchor the journalist's article
4. **Retrieve person properties** -- Get structured data for Eliot Higgins:
   - `uv run query_wikidata_sparql.py properties <higgins_qid>`
   - Look for: nationality, date of birth, occupation, employer, notable works, education, awards
   - Cross-check that employer or "member of" includes Bellingcat
5. **Map relationships** -- Find connected entities:
   - `uv run query_wikidata_sparql.py related <bellingcat_qid>`
   - `uv run query_wikidata_sparql.py related <higgins_qid>`
   - Identify related organizations, people, and events
   - Map the network: founder, key members, parent organizations, awards received
6. **Cross-reference username** -- Check for Eliot Higgins' online presence:
   - `uv run check_username.py eloithiggins --platforms twitter,mastodon_social,github,reddit`
   - Try variations: `EliotHiggins`, `Brown_Moses` (his earlier online handle)
   - This verifies which social platforms he is active on
7. **Web search verification** -- Use Tavily to confirm Wikidata data is current:
   - Search for recent news about Bellingcat and Eliot Higgins
   - Verify founding date, headquarters, current leadership
   - Check if any Wikidata properties are outdated

## Verification
- [ ] Entity search run for "Bellingcat" with `query_wikidata_sparql.py entity`
- [ ] Entity search run for "Eliot Higgins" with `query_wikidata_sparql.py entity`
- [ ] Correct entities disambiguated from multiple results using descriptions
- [ ] Properties retrieved for the organization (`properties` subcommand)
- [ ] Properties retrieved for the person (`properties` subcommand)
- [ ] Related entities mapped for at least one entity (`related` subcommand)
- [ ] Username check performed with `check_username.py`
- [ ] Web search used to verify Wikidata data currency
- [ ] Relationship between Bellingcat and Eliot Higgins confirmed through Wikidata links
- [ ] Structured summary produced with QIDs, key facts, and sources

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Expected Wikidata findings:**

1. **Bellingcat entity:**
   - QID: Q24034552 (may vary if Wikidata is reorganized)
   - Instance of: Online media, investigative journalism organization
   - Country: Netherlands (registered as a Dutch foundation/stichting)
   - Founding date: July 2014
   - Founder: Eliot Higgins
   - Headquarters: The Hague, Netherlands (or Amsterdam, depending on data vintage)
   - Official website: bellingcat.com
   - Notable for: Open-source intelligence investigations, MH17 investigation, identification of Skripal poisoning suspects, tracking chemical weapons use in Syria

2. **Eliot Higgins entity:**
   - QID: Q15999820 (may vary)
   - Nationality: British
   - Date of birth: 1979
   - Occupation: Journalist, blogger, investigative journalist
   - Notable alias/earlier identity: Brown Moses (his original blogging pseudonym during the Syrian conflict analysis)
   - Employer/affiliated with: Bellingcat
   - Awards: Various journalism and human rights awards
   - Education: May or may not be in Wikidata (Higgins is notably self-taught in OSINT)

3. **Relationship mapping:**
   - Bellingcat related entities should include: Eliot Higgins (founder), Netherlands (country), various investigations or organizations they collaborate with
   - Eliot Higgins related entities should include: Bellingcat (employer/founder of), United Kingdom (citizenship), any awards or publications
   - The `related` subcommand reveals the social and organizational network around both entities

4. **Username and online presence:**
   - Eliot Higgins is known on Twitter/X as @EliotHiggins
   - The earlier handle "Brown Moses" was used for his pre-Bellingcat blog
   - May have profiles on other platforms (Mastodon, etc.)
   - check_username.py results depend on platform availability but should demonstrate the cross-platform methodology

5. **Disambiguation methodology:**
   - Entity search returns multiple results sorted by relevance
   - The correct entity is identified by reading the description field, not just the label
   - For common names, checking properties (occupation, nationality) confirms the match
   - QIDs provide stable identifiers that avoid future ambiguity

**Scoring:**
- **Score 5 if:** Agent searches for both entities, correctly disambiguates using descriptions, retrieves properties and related entities for both, runs check_username.py, verifies with web search, and produces a structured summary with QIDs linking Bellingcat to Eliot Higgins through Wikidata's graph
- **Score 4 if:** Agent uses all three Wikidata subcommands (entity, properties, related) and produces a good summary, but omits username check or web verification
- **Score 3 if:** Agent searches for entities and retrieves properties but does not use the related subcommand or does not disambiguate carefully
- **Score 2 if:** Agent only runs entity search without retrieving properties or mapping relationships
- **Score 1 if:** Agent does not use `query_wikidata_sparql.py` or relies entirely on web search without querying Wikidata

</details>

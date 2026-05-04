# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Wikidata SPARQL queries for entity resolution and knowledge graph enrichment.

Search for entities, retrieve properties, run raw SPARQL, and find related entities.
No authentication required. Respects Wikidata User-Agent policy.

Usage:
    uv run query_wikidata_sparql.py entity "Albert Einstein"
    uv run query_wikidata_sparql.py entity "Bellingcat" --limit 5
    uv run query_wikidata_sparql.py properties Q937
    uv run query_wikidata_sparql.py related Q937
    uv run query_wikidata_sparql.py sparql "SELECT ?item ?label WHERE { ... } LIMIT 5"
"""

import argparse
import json
import logging
import sys

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)

WIKIDATA_API = "https://www.wikidata.org/w/api.php"
SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "claude-osint-plugin/1.0 (https://github.com/lawriec/claude-osint-plugin) httpx/0.27"


def _sparql_query(query: str) -> list[dict] | None:
    """Execute a SPARQL query against the Wikidata endpoint."""
    try:
        resp = httpx.get(
            SPARQL_ENDPOINT,
            params={"query": query, "format": "json"},
            headers={"User-Agent": USER_AGENT, "Accept": "application/sparql-results+json"},
            timeout=30,
        )
        if resp.status_code == 429:
            log.error("Rate limited by Wikidata SPARQL endpoint. Wait before retrying.")
            return None
        if resp.status_code == 400:
            log.error("SPARQL syntax error: %s", resp.text[:300])
            return None
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", {}).get("bindings", [])
    except httpx.HTTPStatusError as e:
        log.error("Wikidata SPARQL returned %d: %s", e.response.status_code, e.response.text[:200])
        return None
    except Exception as e:
        log.error("SPARQL query failed: %s", e)
        return None


def _simplify_bindings(bindings: list[dict]) -> list[dict]:
    """Convert SPARQL result bindings to simplified dicts with plain values."""
    rows = []
    for binding in bindings:
        row = {}
        for key, val in binding.items():
            raw = val.get("value", "")
            # Extract QID from full URI
            if raw.startswith("http://www.wikidata.org/entity/"):
                row[key] = raw.split("/")[-1]
            else:
                row[key] = raw
        rows.append(row)
    return rows


def search_entity(name: str, limit: int = 5) -> dict:
    """Search for Wikidata entities by label."""
    try:
        resp = httpx.get(
            WIKIDATA_API,
            params={
                "action": "wbsearchentities",
                "search": name,
                "language": "en",
                "format": "json",
                "limit": min(limit, 20),
                "type": "item",
            },
            headers={"User-Agent": USER_AGENT},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        entities = []
        for item in data.get("search", []):
            entities.append({
                "qid": item.get("id"),
                "label": item.get("label"),
                "description": item.get("description"),
                "aliases": item.get("aliases", []),
                "url": f"https://www.wikidata.org/wiki/{item.get('id')}",
            })

        log.info("Entity search '%s': %d results", name, len(entities))
        return {"query": name, "count": len(entities), "entities": entities}

    except httpx.HTTPStatusError as e:
        log.error("Wikidata API returned %d: %s", e.response.status_code, e.response.text[:200])
        return {"query": name, "error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        log.error("Entity search failed: %s", e)
        return {"query": name, "error": str(e)}


def get_properties(qid: str) -> dict:
    """Get key properties of a Wikidata entity via SPARQL."""
    qid = qid.upper()

    # Properties commonly useful for OSINT: instance-of, name, dates, nationality, locations, IDs
    query = f"""
    SELECT ?prop ?propLabel ?value ?valueLabel WHERE {{
      VALUES ?prop {{
        wdt:P31 wdt:P279 wdt:P17 wdt:P27 wdt:P19 wdt:P20 wdt:P569 wdt:P570
        wdt:P856 wdt:P18 wdt:P625 wdt:P36 wdt:P159 wdt:P112 wdt:P571 wdt:P576
        wdt:P106 wdt:P108 wdt:P69 wdt:P26 wdt:P40 wdt:P22 wdt:P25 wdt:P39
        wdt:P463 wdt:P1566 wdt:P213 wdt:P214 wdt:P227 wdt:P244 wdt:P349
        wdt:P496 wdt:P2002 wdt:P2013 wdt:P2003 wdt:P4550 wdt:P6634
      }}
      wd:{qid} ?prop ?value .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 100
    """

    bindings = _sparql_query(query)
    if bindings is None:
        return {"qid": qid, "error": "SPARQL query failed"}

    # Group properties by label
    properties = {}
    for b in bindings:
        prop_label = b.get("propLabel", {}).get("value", b.get("prop", {}).get("value", ""))
        value_label = b.get("valueLabel", {}).get("value", b.get("value", {}).get("value", ""))

        # Clean up property URIs to readable names
        if prop_label.startswith("http://www.wikidata.org/prop/direct/"):
            prop_label = prop_label.split("/")[-1]

        if prop_label in properties:
            existing = properties[prop_label]
            if isinstance(existing, list):
                existing.append(value_label)
            else:
                properties[prop_label] = [existing, value_label]
        else:
            properties[prop_label] = value_label

    log.info("Properties for %s: %d property types found", qid, len(properties))
    return {
        "qid": qid,
        "url": f"https://www.wikidata.org/wiki/{qid}",
        "property_count": len(properties),
        "properties": properties,
    }


def find_related(qid: str) -> dict:
    """Find entities related to the given entity (employer, education, family, membership, etc.)."""
    qid = qid.upper()

    query = f"""
    SELECT ?relation ?relationLabel ?target ?targetLabel ?targetDescription WHERE {{
      VALUES ?relation {{
        wdt:P108 wdt:P69 wdt:P26 wdt:P40 wdt:P22 wdt:P25 wdt:P3373
        wdt:P463 wdt:P39 wdt:P102 wdt:P54 wdt:P1344 wdt:P800
        wdt:P170 wdt:P50 wdt:P57 wdt:P161 wdt:P175 wdt:P86
        wdt:P127 wdt:P749 wdt:P355 wdt:P159 wdt:P740 wdt:P17
      }}
      wd:{qid} ?relation ?target .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 100
    """

    bindings = _sparql_query(query)
    if bindings is None:
        return {"qid": qid, "error": "SPARQL query failed"}

    # Group by relation type
    relations = {}
    for b in bindings:
        rel_label = b.get("relationLabel", {}).get("value", "")
        if rel_label.startswith("http://"):
            rel_label = rel_label.split("/")[-1]

        target_id = b.get("target", {}).get("value", "").split("/")[-1]
        target_label = b.get("targetLabel", {}).get("value", target_id)
        target_desc = b.get("targetDescription", {}).get("value")

        entry = {"qid": target_id, "label": target_label}
        if target_desc:
            entry["description"] = target_desc

        if rel_label not in relations:
            relations[rel_label] = []
        relations[rel_label].append(entry)

    total_related = sum(len(v) for v in relations.values())
    log.info("Related entities for %s: %d entities across %d relation types", qid, total_related, len(relations))
    return {
        "qid": qid,
        "url": f"https://www.wikidata.org/wiki/{qid}",
        "relation_types": len(relations),
        "total_related": total_related,
        "relations": relations,
    }


def run_sparql(query: str) -> dict:
    """Execute a raw SPARQL query and return simplified results."""
    bindings = _sparql_query(query)
    if bindings is None:
        return {"error": "SPARQL query failed", "query": query[:200]}

    simplified = _simplify_bindings(bindings)
    log.info("SPARQL query returned %d results", len(simplified))
    return {
        "result_count": len(simplified),
        "results": simplified,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Wikidata entity search and SPARQL queries for OSINT (no API key needed). "
        "Useful for entity resolution and knowledge graph enrichment.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    entity_parser = subparsers.add_parser("entity", help="Search for a Wikidata entity by name")
    entity_parser.add_argument("name", help="Entity name to search for")
    entity_parser.add_argument("--limit", type=int, default=5, help="Max results (default: 5, max: 20)")

    props_parser = subparsers.add_parser("properties", help="Get key properties of an entity")
    props_parser.add_argument("qid", help="Wikidata QID (e.g. Q937)")

    related_parser = subparsers.add_parser("related", help="Find related entities")
    related_parser.add_argument("qid", help="Wikidata QID (e.g. Q937)")

    sparql_parser = subparsers.add_parser("sparql", help="Execute a raw SPARQL query")
    sparql_parser.add_argument("query", help="SPARQL query string")

    args = parser.parse_args()

    if args.command == "entity":
        result = search_entity(args.name, limit=args.limit)
    elif args.command == "properties":
        result = get_properties(args.qid)
    elif args.command == "related":
        result = find_related(args.qid)
    elif args.command == "sparql":
        result = run_sparql(args.query)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

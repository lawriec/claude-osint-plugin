# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27"]
# ///
"""Blockchain address lookup for OSINT investigations.

Query Bitcoin and Ethereum addresses using public APIs (no API key needed).

Usage:
    uv run query_blockchain.py btc 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
    uv run query_blockchain.py eth 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe
"""

import argparse
import json
import logging
import sys
from datetime import UTC, datetime

import httpx

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
log = logging.getLogger(__name__)


def lookup_btc(address: str) -> dict:
    """Look up a Bitcoin address via Blockstream API."""
    try:
        resp = httpx.get(f"https://blockstream.info/api/address/{address}", timeout=15)
        resp.raise_for_status()
        data = resp.json()

        chain = data.get("chain_stats", {})
        mempool = data.get("mempool_stats", {})

        result = {
            "chain": "bitcoin",
            "address": address,
            "funded_txo_count": chain.get("funded_txo_count", 0),
            "spent_txo_count": chain.get("spent_txo_count", 0),
            "total_received_sat": chain.get("funded_txo_sum", 0),
            "total_sent_sat": chain.get("spent_txo_sum", 0),
            "balance_sat": chain.get("funded_txo_sum", 0) - chain.get("spent_txo_sum", 0),
            "tx_count": chain.get("tx_count", 0),
            "unconfirmed_tx_count": mempool.get("tx_count", 0),
            "explorer_url": f"https://blockstream.info/address/{address}",
        }

        # Convert satoshis to BTC for readability
        result["total_received_btc"] = result["total_received_sat"] / 1e8
        result["total_sent_btc"] = result["total_sent_sat"] / 1e8
        result["balance_btc"] = result["balance_sat"] / 1e8

        log.info("BTC address %s: %.8f BTC, %d tx", address, result["balance_btc"], result["tx_count"])
        return result

    except httpx.HTTPStatusError as e:
        log.error("Blockstream API returned %d", e.response.status_code)
        return {"chain": "bitcoin", "address": address, "error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        log.error("BTC lookup failed: %s", e)
        return {"chain": "bitcoin", "address": address, "error": str(e)}


def lookup_btc_txs(address: str, limit: int = 10) -> dict:
    """Look up recent transactions for a Bitcoin address."""
    try:
        resp = httpx.get(f"https://blockstream.info/api/address/{address}/txs", timeout=15)
        resp.raise_for_status()
        txs = resp.json()

        transactions = []
        for tx in txs[:limit]:
            tx_data = {
                "txid": tx.get("txid"),
                "confirmed": tx.get("status", {}).get("confirmed", False),
                "block_height": tx.get("status", {}).get("block_height"),
                "fee_sat": tx.get("fee"),
            }

            if tx.get("status", {}).get("block_time"):
                tx_data["timestamp"] = datetime.fromtimestamp(
                    tx["status"]["block_time"], tz=UTC
                ).isoformat()

            # Summarize inputs and outputs
            tx_data["input_count"] = len(tx.get("vin", []))
            tx_data["output_count"] = len(tx.get("vout", []))
            tx_data["total_output_sat"] = sum(v.get("value", 0) for v in tx.get("vout", []))

            transactions.append(tx_data)

        return {
            "chain": "bitcoin",
            "address": address,
            "transaction_count": len(txs),
            "showing": len(transactions),
            "transactions": transactions,
        }

    except Exception as e:
        log.error("BTC transaction lookup failed: %s", e)
        return {"chain": "bitcoin", "address": address, "error": str(e)}


def lookup_eth(address: str) -> dict:
    """Look up an Ethereum address via public API."""
    try:
        # Use Blockscout (no API key needed)
        resp = httpx.get(
            f"https://eth.blockscout.com/api/v2/addresses/{address}",
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        balance_wei = int(data.get("coin_balance", "0") or "0")
        balance_eth = balance_wei / 1e18

        result = {
            "chain": "ethereum",
            "address": address,
            "balance_wei": balance_wei,
            "balance_eth": round(balance_eth, 6),
            "tx_count": data.get("transactions_count", 0),
            "token_transfers_count": data.get("token_transfers_count", 0),
            "is_contract": data.get("is_contract", False),
            "has_tokens": bool(data.get("has_token_transfers")),
            "explorer_url": f"https://etherscan.io/address/{address}",
        }

        if data.get("name"):
            result["name"] = data["name"]

        if data.get("is_contract"):
            result["is_verified"] = data.get("is_verified", False)

        log.info("ETH address %s: balance %.6f ETH, %d transactions", address, balance_eth, result["tx_count"])
        return result

    except httpx.HTTPStatusError as e:
        log.error("Blockscout API returned %d", e.response.status_code)
        return {"chain": "ethereum", "address": address, "error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        log.error("ETH lookup failed: %s", e)
        return {"chain": "ethereum", "address": address, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Blockchain address lookup for OSINT")
    subparsers = parser.add_subparsers(dest="command", required=True)

    btc_parser = subparsers.add_parser("btc", help="Bitcoin address lookup")
    btc_parser.add_argument("address", help="Bitcoin address")
    btc_parser.add_argument("--txs", action="store_true", help="Include recent transactions")
    btc_parser.add_argument("--limit", type=int, default=10, help="Max transactions to show")

    eth_parser = subparsers.add_parser("eth", help="Ethereum address lookup")
    eth_parser.add_argument("address", help="Ethereum address")

    args = parser.parse_args()

    if args.command == "btc":
        result = lookup_btc(args.address)
        if args.txs:
            result["recent_transactions"] = lookup_btc_txs(args.address, args.limit)
    elif args.command == "eth":
        result = lookup_eth(args.address)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

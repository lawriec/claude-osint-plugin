# Challenge: Cryptocurrency Wallet Tracing

## Domain
Cryptocurrency / Financial OSINT

## Difficulty
Medium

## Scenario
"During an investigation into online fraud, two cryptocurrency addresses have surfaced. We need a full analysis of both before briefing the team tomorrow.

The first is a Bitcoin address: `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`. The second is an Ethereum address: `0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe`.

For each address, look up its current balance and transaction history. Determine how active each address is, what kind of wallet it appears to be (personal, exchange, organizational, or something else entirely), and whether there are any notable characteristics that stand out. Cross-reference with public information to identify the entities behind them if possible."

## Expected Approach
1. **Bitcoin address lookup** -- `query_blockchain.py btc 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`:
   - Note the balance (receives regular donations, currently 72+ BTC)
   - Note the transaction count (high and increasing over time)
   - Observe that `spent_txo_count` is 0 -- this address has never sent funds
   - Note the `total_sent_btc` is 0 despite large `total_received_btc`
2. **Bitcoin transaction history** -- `query_blockchain.py btc 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa --txs`:
   - Examine recent transactions to confirm pattern: all inbound, no outbound
   - Note that transactions are small donation-like amounts from many different senders
   - Check timestamps to confirm ongoing activity
3. **Ethereum address lookup** -- `query_blockchain.py eth 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe`:
   - Note the large balance (significant ETH holdings)
   - Check `is_contract` field (this is a contract/multisig)
   - Note high `tx_count` and `token_transfers_count`
   - Check if `name` field identifies the entity
4. **Web search for attribution** -- Search for both addresses to identify owners:
   - BTC address is the Bitcoin Genesis Block coinbase address (Satoshi Nakamoto)
   - ETH address is the Ethereum Foundation's primary multisig wallet
5. **Wallet classification** -- Analyze patterns to classify each wallet:
   - BTC: Not a personal wallet, not an exchange -- it is the Genesis Block reward address with a unique technical peculiarity (original 50 BTC are unspendable)
   - ETH: Organizational wallet (foundation multisig), characterized by large holdings and high transaction volume
6. **Compile findings** into structured assessment with entity attribution, activity analysis, and wallet type classification

## Verification
- [ ] Both addresses queried successfully with `query_blockchain.py`
- [ ] BTC address identified as Genesis Block / Satoshi Nakamoto
- [ ] ETH address identified as Ethereum Foundation
- [ ] Transaction patterns analyzed (BTC: receive-only; ETH: active bidirectional)
- [ ] Wallet classifications provided for both (not personal wallets)
- [ ] Genesis Block unspendable coinbase quirk noted
- [ ] Web search used to corroborate on-chain findings

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Bitcoin address `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`:**
- This is the **Genesis Block** (Block 0) coinbase address, created by **Satoshi Nakamoto** on January 3, 2009
- The original 50 BTC block reward is **unspendable** due to a quirk in the genesis block implementation (the coinbase transaction is not in the UTXO set)
- The address receives regular small donations from the Bitcoin community as a tribute
- Balance is 72+ BTC (all from donations; none has ever been spent)
- `spent_txo_count` = 0, confirming no outbound transactions
- Classification: **Historical/ceremonial address**, not an active wallet

**Ethereum address `0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe`:**
- This is the **Ethereum Foundation** multisig wallet
- Holds a substantial ETH balance used for ecosystem grants and operational funding
- High transaction count with both ETH transfers and token operations
- `is_contract` = true (it is a multisig contract, not an externally owned account)
- Classification: **Organizational multisig wallet**

**Neither address is a personal wallet or exchange wallet.**

**Scoring:**
- **Score 5 if:** Agent queries both addresses, identifies both entities correctly (Genesis Block and Ethereum Foundation), analyzes transaction patterns in detail, notes the unspendable coinbase quirk, classifies both wallets accurately, and provides a structured comparative report
- **Score 4 if:** Agent identifies both entities and provides transaction analysis but misses the Genesis Block technical quirk or lacks detailed pattern comparison
- **Score 3 if:** Agent identifies at least one entity correctly and provides basic transaction data for both addresses
- **Score 2 if:** Agent retrieves blockchain data for both addresses but fails to identify either entity or provide meaningful analysis
- **Score 1 if:** Agent only queries one address or provides raw data without interpretation

</details>

# Cryptocurrency & Financial OSINT Reference

Techniques for tracing cryptocurrency transactions, identifying wallets, analyzing blockchain activity, and investigating financial flows across decentralized networks. Load this reference when an investigation involves crypto addresses, wallet attribution, DeFi activity, NFT provenance, or financial tracing.

---

## Plugin Tool: `query_blockchain.py`

Quick lookup of Bitcoin and Ethereum addresses (no API key needed):

```
uv run query_blockchain.py btc 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
uv run query_blockchain.py eth 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe
```

Returns balance, transaction count, and funding/spending summary as JSON.

---

## Bitcoin Blockchain Analysis

### Address Types

| Type | Prefix | Example | Notes |
|------|--------|---------|-------|
| **Legacy (P2PKH)** | `1` | `1A1zP1eP5Q...` | Original format. Most widely supported. Easy to identify |
| **Nested SegWit (P2SH)** | `3` | `3J98t1WpEZ...` | Wrapped SegWit. Also used for multisig addresses |
| **Native SegWit (Bech32)** | `bc1q` | `bc1qw508d6q...` | Lower fees, modern wallets. 42 characters |
| **Taproot (Bech32m)** | `bc1p` | `bc1p5cyxnux...` | Latest format. Enhanced privacy and smart contract capability |

Address format reveals wallet software age and sophistication. Legacy addresses on new transactions may indicate older or less technical users.

### UTXO Model

Bitcoin uses Unspent Transaction Outputs (UTXOs), not account balances:
- Each transaction consumes one or more UTXOs as inputs and creates new UTXOs as outputs
- **Change addresses**: When spending part of a UTXO, the remainder goes to a change address controlled by the sender
- Change address detection is a key wallet clustering technique (see below)
- A single "wallet" may control hundreds of addresses

### Block Explorers

| Explorer | URL | Strengths |
|----------|-----|-----------|
| **Blockstream.info** | blockstream.info | Clean API, Tor-friendly, used by `query_blockchain.py` |
| **Blockchain.com** | blockchain.com/explorer | Popular, shows wallet "estimated balance" by clustering |
| **Blockchair** | blockchair.com | Multi-chain, advanced filtering, privacy-focused |
| **Mempool.space** | mempool.space | Excellent transaction visualization, fee analysis, mempool monitoring |
| **OXT** | oxt.me | Advanced Bitcoin analysis with transaction graph visualization |
| **Wallet Explorer** | walletexplorer.com | Automatic wallet clustering with known-entity labels |

### Transaction Graph Analysis

Follow the money by tracing inputs and outputs:

1. **Start with a known address** -- use `uv run query_blockchain.py btc <address>` for initial lookup
2. **Examine transactions** -- note inputs (funding sources) and outputs (destinations)
3. **Identify change outputs** -- the output returning to the sender's wallet
4. **Follow forward/backward** -- trace where funds went and where they came from
5. **Look for known entities** -- exchanges, mixers, darknet markets have labeled addresses

---

## Ethereum Analysis

### Key Concepts

| Concept | Description |
|---------|-------------|
| **EOA (Externally Owned Account)** | Regular wallet controlled by a private key. Address starts with `0x` (40 hex characters) |
| **Contract account** | Smart contract deployed on-chain. Also starts with `0x` but has associated code |
| **ENS name** | Ethereum Name Service (e.g., `vitalik.eth`). Reverse lookup reveals the owner address |
| **Token transfers** | ERC-20 (fungible tokens) and ERC-721/1155 (NFTs) are tracked via contract events, not native transactions |
| **Gas price** | Transaction fee reveals urgency. Abnormally high gas may indicate MEV or front-running |
| **Internal transactions** | Contract-to-contract calls not visible in standard transaction list. Check "Internal Txns" tab on Etherscan |

### Ethereum Explorers

| Explorer | URL | Strengths |
|----------|-----|-----------|
| **Etherscan** | etherscan.io | Industry standard. Token transfers, contract verification, labels |
| **Etherscan (labels)** | etherscan.io/labelcloud | Browse all labeled addresses by category (exchange, DeFi, bridge, etc.) |
| **Blockscout** | blockscout.com | Open-source explorer, multi-chain |
| **Tenderly** | tenderly.co | Transaction simulation and debugging, smart contract analysis |

### ENS (Ethereum Name Service) Lookup

ENS names resolve to wallet addresses and vice versa:
- Forward: `vitalik.eth` -> `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`
- Reverse: address -> registered ENS name
- Look up at app.ens.domains or via Etherscan. Registration history is on-chain

---

## Cross-Chain and Multi-Chain Tools

| Tool | URL | Auth | Purpose |
|------|-----|------|---------|
| **Arkham Intelligence** | platform.arkhamintel.com | Free account | Entity labeling, cross-chain tracking, alerts. Extensive labeled address database |
| **Nansen** | nansen.ai | Paid | Smart money tracking, wallet profiling, token flow analysis |
| **Dune Analytics** | dune.com | Free dashboards | Community-built SQL dashboards for on-chain data. Search for investigation-specific queries |
| **Chainalysis Reactor** | chainalysis.com | Commercial (LE) | Industry-standard law enforcement tool. Wallet clustering, risk scoring, attribution |
| **Crystal Blockchain** | crystalblockchain.com | Commercial | Transaction visualization, risk scoring, exchange flow analysis |
| **Breadcrumbs** | breadcrumbs.app | Free tier | Visual transaction tracing, address investigation |
| **Metasleuth** | metasleuth.io | Free tier | Cross-chain tracking and visualization by BlockSec |

---

## Wallet Clustering Techniques

Clustering links multiple addresses to a single controlling entity:

### Common-Input-Ownership Heuristic

When a transaction has multiple input addresses, all those addresses are likely controlled by the same entity (a valid signature is needed for each input). This is the most reliable clustering method.

### Change Address Detection

Identify which output is the change (returning to the sender):
- **Address reuse**: Change sent to an already-known address in the same cluster
- **Round number heuristic**: Payment is likely a round number; the other output is change
- **Address type matching**: Change output often uses the same address type as inputs

### Timing Analysis

- Regular transaction patterns suggest automated systems
- Consistent activity hours suggest a time zone
- Rapid sequences between related addresses suggest consolidation or distribution

---

## Mixer and Tumbler Detection

### CoinJoin

CoinJoin transactions combine multiple users' inputs and outputs to obscure the graph:
- **Indicators**: Many inputs from different addresses, many outputs of equal value
- **Wasabi Wallet**: Coordinator-based CoinJoin. Distinctive equal-denomination outputs
- **JoinMarket**: Decentralized CoinJoin market. Maker-taker model
- **Whirlpool** (Samourai): Fixed denomination pools (0.5, 0.05, 0.01, 0.001 BTC)

### Tornado Cash (Ethereum)

- Fixed denomination deposits/withdrawals (0.1, 1, 10, 100 ETH)
- Contract addresses are well-known and labeled on Etherscan
- OFAC-sanctioned (August 2022); interactions flagged by compliance tools

### Red Flags for Mixing

| Indicator | Significance |
|-----------|-------------|
| Equal-value outputs (many) | CoinJoin transaction |
| Interaction with known mixer contracts | Tornado Cash, ChipMixer, etc. |
| Peel chain pattern | Repeated small withdrawals from a large balance, typical of mixing services |
| Rapid chain-hopping | BTC -> exchange -> ETH -> bridge -> L2, to obscure trail |
| Privacy coin conversion | Swapping to Monero/Zcash to break traceability |

---

## DeFi and DEX Tracking

### Decentralized Exchange Transactions

| DEX | Chain | URL | Notes |
|-----|-------|-----|-------|
| **Uniswap** | Ethereum, Polygon, Arbitrum, others | uniswap.org | Largest DEX. Swap events visible on-chain |
| **PancakeSwap** | BNB Chain | pancakeswap.finance | Largest BSC DEX |
| **Curve** | Ethereum, multi-chain | curve.fi | Stablecoin-focused, large volume |
| **SushiSwap** | Multi-chain | sushi.com | Cross-chain DEX |

DEX swaps are fully on-chain -- every trade is traceable. Use Etherscan "Token Transfers" or Dune dashboards to analyze trading patterns.

Also look for interactions with lending protocols (Aave, Compound), bridges (Wormhole, Stargate, Across) for cross-chain transfers, and yield farms for long-term holding patterns.

---

## NFT Provenance

| Platform | URL | Purpose |
|----------|-----|---------|
| **OpenSea** | opensea.io | Largest NFT marketplace. Ownership history, transaction history per token |
| **Blur** | blur.io | NFT marketplace with trading analytics |
| **Etherscan (ERC-721)** | etherscan.io/token/<contract> | On-chain transfer history for any NFT collection |

Track NFT ownership chains by following ERC-721/ERC-1155 transfer events on-chain. Each transfer is permanently recorded.

---

## Stablecoin Tracking

Stablecoins are useful for financial OSINT because they represent real dollar values:

| Stablecoin | Issuer | Key Feature |
|------------|--------|-------------|
| **USDT (Tether)** | Tether Limited | Largest stablecoin. Multi-chain. Issuer can freeze addresses |
| **USDC** | Circle | Second largest. Multi-chain. Issuer can freeze addresses |
| **DAI** | MakerDAO | Decentralized, algorithmic. Cannot be frozen by any single entity |

**Freeze events**: USDT and USDC issuers can blacklist addresses on-chain. Frozen addresses are publicly queryable and indicate law enforcement action or sanctions compliance.

---

## Exchange Identification

### Known Exchange Addresses

Major exchanges have labeled addresses on block explorers:
- **Etherscan label cloud**: etherscan.io/labelcloud (search by exchange name)
- **Wallet Explorer**: walletexplorer.com (Bitcoin-focused, clusters exchange wallets)
- **Arkham Intelligence**: Most comprehensive labeled address database across chains

### Exchange Behavior Patterns

| Pattern | Indicates |
|---------|-----------|
| Deposit to known exchange hot wallet | User depositing funds to trade or cash out |
| Withdrawal from exchange | User moving funds to personal custody |
| Large deposits followed by immediate withdrawal | Possible wash trading or pass-through |
| Many small deposits from different addresses | Consolidation from mining or payment processing |
| Deposit to exchange, withdrawal to different chain | Cross-chain movement via exchange (harder to trace) |

---

## Legal Considerations

- **Blockchain data is public**: Transaction data is permanently public. No authorization needed to view it
- **Attribution requires caution**: Linking an address to a real-world identity is analytical, not factual. Document evidence
- **Exchange records require legal process**: KYC data held by exchanges requires subpoenas or court orders
- **Sanctions compliance**: Interacting with OFAC-sanctioned addresses may have legal implications. Use read-only explorers
- **Privacy coins**: Monero, Zcash (shielded), and similar chains resist analysis. Limited OSINT value without specialized tools

---

## Investigation Workflow

1. **Initial lookup** -- `uv run query_blockchain.py btc|eth <address>` for balance and transaction count
2. **Identify blockchain and address type** -- determines which explorers and tools to use
3. **Check entity labels** -- Arkham, Etherscan labels, Wallet Explorer for known attribution
4. **Trace transactions** -- Follow inputs/outputs on block explorers. Note large or unusual flows
5. **Check for mixing** -- CoinJoin patterns (Bitcoin), Tornado Cash (Ethereum), bridge usage
6. **Find exchange touchpoints** -- Deposits to/from exchanges are key attribution points
7. **Check ENS/domain links** -- ENS names, linked social profiles, on-chain messages
8. **Cross-reference off-chain** -- Social media mentions, forum signatures, donation pages
9. **Document in knowledge graph** -- Record addresses, entities, transactions, and relationships

---

## Cross-References

- `domain-infrastructure.md` -- Investigating crypto project websites and hosting
- `people-social-media.md` -- Linking wallet addresses to social media profiles
- `opsec-ethics.md` -- Ethical guidelines and legal boundaries
- `knowledge-graph.md` -- Entity schema for recording wallet addresses and financial flows
- `dark-web-research.md` -- Darknet market wallet analysis

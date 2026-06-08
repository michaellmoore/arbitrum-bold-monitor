# Arbitrum BoLD Core: Open-Source CLI Assertion & Dispute Monitor

A lightweight, production-ready CLI daemon designed to monitor state assertions and active fraud-proof disputes within Arbitrum's **Bounded Liquidity Delay (BoLD)** validation protocol on the Arbitrum Sepolia testnet.

## Overview

With the migration to permissionless validation via BoLD, maintaining visibility into state transitions and active challenges is critical for ecosystem infrastructure. This tool provides a zero-overhead, independent monitoring solution that polls raw RPC data directly from the network, eliminating the need to rely on centralized indexers or heavy validator nodes.

### Key Features
- **Real-Time Event Ingestion:** Captures and decodes `AssertionPosted` and `ChallengeInitiated` events directly from core rollup contracts.
- **Minimal Resource Footprint:** Designed to run continuously in the background as a daemon with negligible CPU and memory usage.
- **Zero-Configuration Setup:** Connects securely out-of-the-box using public RPC infrastructure.

---

## Technical Specifications

- **Language:** Python 3.x
- **Network Target:** Arbitrum Sepolia Testnet
- **Tracked Contracts:**
  - `Rollup`: `0x042b0cf400000000000000000000000000000000`
  - `ChallengeManager`: `0xc60b8b4c00000000000000000000000000000000`

---

## Installation & Setup

### 1. Prerequisites
Ensure you have Python 3 and `pip` installed on your system.

### 2. Clone the Repository
```bash
git clone [https://github.com/michaellmoore/arbitrum-bold-monitor.git](https://github.com/michaellmoore/arbitrum-bold-monitor.git)
cd arbitrum-bold-monitor

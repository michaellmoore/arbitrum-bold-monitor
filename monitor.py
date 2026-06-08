import time
import json
from web3 import Web3

# Arbitrum Sepolia Testnet Core Contract Address placeholders
CHALLENGE_MANAGER_ADDRESS = "0xc60b8b4c00000000000000000000000000000000" 
ROLLUP_ADDRESS = "0x042b0cf400000000000000000000000000000000"

# Strict ABI definition for decoding event logs
MINIMAL_ABI = json.loads('''[
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "internalType": "uint256", "name": "assertionId", "type": "uint256"},
            {"indexed": false, "internalType": "bytes32", "name": "stateRoot", "type": "bytes32"},
            {"indexed": false, "internalType": "uint256", "name": "bondAmount", "type": "uint256"}
        ],
        "name": "AssertionPosted",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "internalType": "uint256", "name": "challengeId", "type": "uint256"},
            {"indexed": true, "internalType": "address", "name": "asserter", "type": "address"},
            {"indexed": true, "internalType": "address", "name": "challenger", "type": "address"}
        ],
        "name": "ChallengeInitiated",
        "type": "event"
    }
]''')

def monitor_bold_events(rpc_url):
    print("[*] Initializing Arbitrum BoLD Monitoring Daemon...")
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not w3.is_connected():
        print("[!] Error: Unable to connect to Arbitrum RPC node.")
        return

    print(f"[+] Connected to Arbitrum Node. Current Block: {w3.eth.block_number}")
    
    try:
        challenge_contract = w3.eth.contract(address=w3.to_checksum_address(CHALLENGE_MANAGER_ADDRESS), abi=MINIMAL_ABI)
        rollup_contract = w3.eth.contract(address=w3.to_checksum_address(ROLLUP_ADDRESS), abi=MINIMAL_ABI)
    except Exception as e:
        print(f"[!] Address/ABI validation error: {str(e)}")
        return

    print("[*] Scanning for state assertions and active disputes... (Press Ctrl+C to exit)")
    
    # Set the starting block back slightly to catch recent data
    start_block = w3.eth.block_number - 50 
    
    while True:
        try:
            current_block = w3.eth.block_number
            if start_block > current_block:
                start_block = current_block
                
            print(f"[~] Polling blocks {start_block} to {current_block} for BoLD updates...")
            
            # Universal direct log query for Rollup Contract
            rollup_logs = w3.eth.get_logs({
                "fromBlock": start_block,
                "toBlock": current_block,
                "address": w3.to_checksum_address(ROLLUP_ADDRESS)
            })
            for log in rollup_logs:
                try:
                    event_data = rollup_contract.events.AssertionPosted().process_log(log)
                    print(f"\n[ALERT] New State Assertion Posted on Rollup!")
                    print(f" -> Assertion ID: {event_data['args']['assertionId']}")
                    print(f" -> State Root: {event_data['args']['stateRoot'].hex()}")
                    print(f" -> Bond Posted: {w3.from_wei(event_data['args']['bondAmount'], 'ether')} WETH")
                except Exception:
                    pass

            # Universal direct log query for Challenge Manager Contract
            challenge_logs = w3.eth.get_logs({
                "fromBlock": start_block,
                "toBlock": current_block,
                "address": w3.to_checksum_address(CHALLENGE_MANAGER_ADDRESS)
            })
            for log in challenge_logs:
                try:
                    event_data = challenge_contract.events.ChallengeInitiated().process_log(log)
                    print(f"\n[CRITICAL] Fraud Proof Challenge Initiated!")
                    print(f" -> Challenge ID: {event_data['args']['challengeId']}")
                    print(f" -> Asserter Address: {event_data['args']['asserter']}")
                    print(f" -> Challenger Address: {event_data['args']['challenger']}")
                except Exception:
                    pass

            start_block = current_block + 1
            time.sleep(15) 
            
        except Exception as e:
            print(f"[!] Live tracking notice: {str(e)}")
            time.sleep(10)

if __name__ == "__main__":
    # Verified public RPC endpoint for Arbitrum Sepolia
    PUBLIC_RPC = "https://sepolia-rollup.arbitrum.io/rpc"
    monitor_bold_events(PUBLIC_RPC)

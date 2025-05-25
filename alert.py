from web3 import Web3
import requests
import time
import os

INFURA_URL = os.getenv("INFURA_URL")
STAKING_CONTRACT_ADDRESS = "0x3FEFbFe3C3e00F55E2fCEb1B004aE3f15a9DaFf1"
MAX_STAKE = 40_875_000 * (10**18)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

staking_abi = [
    {
        "inputs": [],
        "name": "getTotalStaked",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    }
]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg
    }
    requests.post(url, data=payload)

def check_staking():
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))
    contract = w3.eth.contract(address=STAKING_CONTRACT_ADDRESS, abi=staking_abi)
    current_staked = contract.functions.getTotalStaked().call()
    print(f"Current Staked: {current_staked / 1e18} LINK")
    if current_staked < MAX_STAKE:
        send_telegram("⚠️ Có slot trống trong Chainlink Staking v0.2! Vào nhanh: https://staking.chain.link/")

if __name__ == "__main__":
    while True:
        try:
            check_staking()
        except Exception as e:
            print("Error:", e)
        time.sleep(60)

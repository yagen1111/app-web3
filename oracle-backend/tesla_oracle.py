import requests
import time
from web3 import Web3
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Configuration
ALCHEMY_URL = f"https://eth-sepolia.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = "0x16D093BDa86814561C2BdC99d39b32A10e9D4F09"

# Smart Contract ABI (only the functions we need)
CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "uint256", "name": "newPriceUSD", "type": "uint256"}],
        "name": "updatePrice",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getPriceUSD",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class TeslaPriceOracle:
    def __init__(self):
        # Connect to blockchain
        self.w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
        
        # Setup account
        self.account = self.w3.eth.account.from_key(PRIVATE_KEY)
        self.w3.eth.default_account = self.account.address
        
        # Setup contract
        self.contract = self.w3.eth.contract(
            address=CONTRACT_ADDRESS,
            abi=CONTRACT_ABI
        )
        
        print(f"🔗 Connected to Sepolia")
        print(f"📍 Account: {self.account.address}")
        print(f"📄 Contract: {CONTRACT_ADDRESS}")
    
    def get_tesla_price(self):
        """Fetch Tesla stock price from Yahoo Finance API"""
        try:
            # Yahoo Finance API endpoint
            url = "https://query1.finance.yahoo.com/v8/finance/chart/TSLA"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers)
            data = response.json()
            
            # Extract current price
            current_price = data['chart']['result'][0]['meta']['regularMarketPrice']
            
            # Convert to integer (multiply by 100 to keep 2 decimal places)
            # Example: $245.67 becomes 24567
            price_cents = int(current_price * 100)
            
            print(f"💰 Tesla Current Price: ${current_price:.2f} (stored as {price_cents})")
            return price_cents
            
        except Exception as e:
            print(f"❌ Error fetching Tesla price: {e}")
            return None
    
    def update_contract_price(self, new_price):
        """Update the smart contract with new Tesla price"""
        try:
            # Get current contract price
            current_contract_price = self.contract.functions.getPriceUSD().call()
            print(f"📊 Current contract price: {current_contract_price}")
            
            # Check if update is needed (avoid unnecessary transactions)
            if current_contract_price == new_price:
                print("✅ Price unchanged, skipping update")
                return True
            
            # Build transaction
            transaction = self.contract.functions.updatePrice(new_price).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 100000,
                'gasPrice': self.w3.to_wei('20', 'gwei')
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            print(f"🚀 Transaction sent: {tx_hash.hex()}")
            
            # Wait for confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                print(f"✅ Price updated successfully! New price: {new_price}")
                print(f"📈 Transaction confirmed: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")
                return True
            else:
                print("❌ Transaction failed")
                return False
                
        except Exception as e:
            print(f"❌ Error updating contract: {e}")
            return False
    
    def run_oracle(self, update_interval=300):  # 5 minutes = 300 seconds
        """Main oracle loop - fetch and update price every interval"""
        print(f"🚀 Starting Tesla Price Oracle (updates every {update_interval}s)")
        
        while True:
            try:
                # Fetch current Tesla price
                tesla_price = self.get_tesla_price()
                
                if tesla_price:
                    # Update contract
                    success = self.update_contract_price(tesla_price)
                    
                    if success:
                        print(f"🎯 Oracle cycle completed successfully")
                    else:
                        print(f"⚠️ Oracle cycle failed")
                else:
                    print("⚠️ Skipping update due to price fetch error")
                
                print(f"⏰ Waiting {update_interval} seconds until next update...\n")
                time.sleep(update_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Oracle stopped by user")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print(f"⏰ Waiting {update_interval} seconds before retry...\n")
                time.sleep(update_interval)

if __name__ == "__main__":
    # Create and run oracle
    oracle = TeslaPriceOracle()
    
    # Test single price fetch first
    print("🧪 Testing single price fetch...")
    price = oracle.get_tesla_price()
    
    if price:
        print("✅ Price fetch successful!")
        
        # Ask user if they want to start continuous oracle
        start_oracle = input("\n🤖 Start continuous price oracle? (y/n): ").lower().strip()
        
        if start_oracle == 'y':
            oracle.run_oracle(update_interval=60)  # Update every minute for demo
        else:
            print("👋 Oracle ready to run when needed!")
    else:
        print("❌ Price fetch failed. Check your internet connection.")

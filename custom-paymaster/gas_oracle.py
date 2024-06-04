import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from eth_account import Account
from eth_account.signers.local import LocalAccount
from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.manage_contracts.contract_encoder_base import ContractEncoder, JsonConfiguration

# Load environment variables
load_dotenv()
PROVIDER_PORT = os.getenv('PROVIDER_PORT')
WALLET_PK = os.getenv('WALLET_PRIVATE_KEY')
CONVERSION_RATE_ADDRESS = os.getenv('CONVERSION_RATE_ADDRESS')

# Initialize account and web3 instance
account: LocalAccount = Account.from_key(WALLET_PK)
web3 = ZkSyncBuilder.build("http://127.0.0.1:3050")

# Fetch conversion rate from an external service
def fetch_conversion_rate(port: str) -> int:
    response = requests.get(f"http://127.0.0.1:{port}")
    conversion_rate = float(response.content)
    conversion_rate_wei = int(conversion_rate * 10**18)
    
    max_u256_value = 2**256 - 1
    if conversion_rate_wei > max_u256_value:
        raise ValueError("The value exceeds the maximum value for a uint256.")

    return conversion_rate_wei

# Load contract
def load_contract(web3, contract_path: str, contract_address: str):
    conversion_rate_path = Path(contract_path)
    conversion_rate_address = web3.to_checksum_address(contract_address)
    conversion_rate_json = ContractEncoder.from_json(web3, conversion_rate_path, JsonConfiguration.STANDARD)
    return web3.zksync.contract(conversion_rate_address, abi=conversion_rate_json.abi)

# Send transaction to sset conversion rate
def set_conversion_rate(contract, conversion_rate: int, account: LocalAccount, web3):
    transaction = contract.functions.setConversionRate(conversion_rate).build_transaction({
        'from': account.address,
        'gas': 2000000,  
        'gasPrice': web3.to_wei('20', 'gwei'), 
        'nonce': web3.eth.get_transaction_count(account.address),
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=account.key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    return txn_receipt

# Main function
def main():
    conversion_rate = fetch_conversion_rate(PROVIDER_PORT)
    print("Conversion rate in weis:", conversion_rate)
    
    conversion_rate_contract = load_contract(
        web3, 
        "artifacts-zk/contracts/ConversionRateProvider.sol/ConversionRateProvider.json", 
        CONVERSION_RATE_ADDRESS
    )
    
    txn_receipt = set_conversion_rate(conversion_rate_contract, conversion_rate, account, web3)
    print("Gas used:", txn_receipt.get('gasUsed'))

    getConversionTx = conversion_rate_contract.functions.getConversionRate().call()
    print("Result of getConversionRate:", getConversionTx)

# Run the main function
if __name__ == "__main__":
    main()

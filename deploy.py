import json
import os

from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

CONTRACT_NAME = 'VoteStorage'

build_fle = f'./build/{CONTRACT_NAME}.sol/{CONTRACT_NAME}.json'
with open(build_fle, 'r') as f:
    compiled_sol = json.loads(f.read())

abi = compiled_sol['contracts'][f'{CONTRACT_NAME}.sol'][CONTRACT_NAME]['abi']
bytecode = compiled_sol['contracts'][f'{CONTRACT_NAME}.sol'][CONTRACT_NAME]['evm']['bytecode']['object']

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider(os.getenv('NETWORK_URL')))
chain_id = int(os.getenv('CHAIN_ID'))
my_address = os.getenv('MY_ADDRESS')
my_private_key = os.getenv('MY_PRIVATE_KEY')

# Create contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build
# 2. Sign
# 3. Send

transaction = contract.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=my_private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(*tx_receipt['logs'], sep='\n')
print(f'Contract Address = {tx_receipt.contractAddress}')

with open('./ContractAddress', 'w+') as f:
    f.write(tx_receipt.contractAddress)

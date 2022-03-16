import json
import os
import initialize

from web3 import Web3
from dotenv import load_dotenv
from web3.types import TxReceipt
from flask import Flask, request
from flask_restx import Resource, Api, fields


load_dotenv(dotenv_path=r"C:\Users\Hansa Jayathilaka\Work\Anju Akka\Brownie\.env")

initialize.main()

app = Flask(__name__)
api = Api(app, version='1.0', title='Voting System', description='Vote calculating System')

CONTRACT_NAME = 'DynamicVoteStorage'
chain_id = int(os.getenv('CHAIN_ID'))
my_address = os.getenv('PUBLIC_KEY')
my_private_key = os.getenv('PRIVATE_KEY')

with open('./build/deployments/map.json') as json_file:
    data = json.load(json_file)
    contract_address = data[str(chain_id)][CONTRACT_NAME][0]

with open(f'./build/deployments/{chain_id}/{contract_address}.json') as json_file:
    data = json.load(json_file)
    abi = data['abi']


Vote = api.model('Vote', {
    'user_hash': fields.String(required=True, min_length=1, description='Voter\'s Hash'),
    'competitor_index': fields.Integer(required=True, description='Vote'),
})

Competitor_List = api.model('Competitor_List', {
    'competitors': fields.List(fields.Integer, default=[1, 2, 3, 4, 5]),
    'eliminate_count': fields.Integer(required=True, description='Elimination Count'),
})

print("Contract Address : ", contract_address)


def create_transaction(w3, contract, function_name, params=None, gasPrice=None) -> TxReceipt:
    if params is None:
        params = []
    nonce = w3.eth.getTransactionCount(my_address)
    tx = getattr(contract.functions, function_name)(*params).buildTransaction(
        {
            "gasPrice": gasPrice if gasPrice else w3.eth.gas_price,
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce,
        }
    )
    signed_txn = w3.eth.account.sign_transaction(tx, private_key=my_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(*tx_receipt['logs'], sep='\n')
    return tx_receipt


def get_contract():
    w3 = Web3(Web3.HTTPProvider(os.getenv('NETWORK_URL')))
    contract = w3.eth.contract(address=contract_address, abi=abi)
    return w3, contract


@api.route('/new_event')
class CreateNewEvent(Resource):
    def get(self):
        w3, contract = get_contract()
        try:
            receipt = create_transaction(w3, contract, 'create_new_event')
            return {
                'status': True,
                'message': receipt.logs,
            }
        except Exception as ex:
            return {
                'status': False,
                'message': [str(ex)],
            }


@api.route('/vote')
class CreateVote(Resource):
    @api.expect(Vote, validate=True)
    def post(self):
        doc = json.loads(request.data)
        w3, contract = get_contract()
        try:
            receipt = create_transaction(w3, contract, 'create_vote', [doc['user_hash'], doc['competitor_index']])
            return {
                'status': True,
                'message': receipt.logs,
            }
        except Exception as ex:
            return {
                'status': False,
                'message': [str(ex)],
            }


@api.route('/get-count/<int:vote>')
class GetVote(Resource):
    def get(self, vote):
        _, contract = get_contract()
        count = contract.functions.get_result(vote).call()
        return {
            'status': True,
            'vote_count': count,
            'message': [],
        }


@api.route('/summary')
class GetSummary(Resource):
    @api.expect(Competitor_List)
    def post(self):
        doc = json.loads(request.data)
        _, contract = get_contract()
        results = []
        for i in doc['competitors']:
            count = contract.functions.get_result(i).call()
            results.append({
                'competitor_index': i,
                'vote_count': count,
                'eliminate': False,
            })
        results.sort(key=lambda x: x['vote_count'], reverse=True)
        try:
            for i in range(1, doc['eliminate_count'] + 1):
                results[-i]['eliminate'] = True
        except:
            pass
        return {
            'status': True,
            'vote_summery': results,
            'message': [],
        }


@app.errorhandler(404)
def page_not_found(error):
    return {
            'status': False,
            'message': [error.message],
        }, 404


if __name__ == '__main__':
    app.run(debug=False)

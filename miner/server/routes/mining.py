from flask import Blueprint, jsonify

from miner.server.config import blockchain, private_key, public_key

import miner.blockchain.utilities.crypto as crypto_utils
import miner.blockchain.utilities.proof as proofing
import miner.blockchain.utilities.keypair as keypair

bp = Blueprint('mining', __name__)

@bp.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    proof = proofing.proof_of_work(last_block)

    mine_reward = keypair.create_mine_reward_tx((private_key, public_key))
    blockchain.transacting.new_transaction(mine_reward)

    print(blockchain.current_transactions)

    previous_hash = crypto_utils.hash(last_block)
    block = blockchain.mining.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

from flask import jsonify, Blueprint

from miner.server.config import blockchain

bp = Blueprint('state_bp', __name__)

@bp.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'current_transactions': blockchain.current_transactions,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@bp.route('/get_transaction/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = blockchain.transacting.get_transaction(transaction_id)
    if transaction is None:
        return jsonify({"error": "Transaction not found", "latest_block_index": blockchain.last_block['index']}), 404
    return jsonify(transaction), 200

@bp.route('/get_chain_account/<pubkey_hex>', methods=['GET'])
def get_chain_account(pubkey_hex):
    account = blockchain.accounting.get_chain_account(pubkey_hex)
    if account is None:
        return jsonify({"error": "Account not found", "latest_block_index": blockchain.last_block['index']}), 404
    return jsonify(account), 200

@bp.route('/get_current_block_index', methods=['GET'])
def get_current_block_index():
    return jsonify(blockchain.last_block['index']), 200
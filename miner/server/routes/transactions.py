import hashlib, json, os

from flask import Flask, jsonify, request, Blueprint

from miner.server.config import blockchain 
from miner.blockchain.blockchain import CURRENT_DIR

bp = Blueprint('transactions_bp', __name__)

def generic_transaction_handler(request, blockchain_handler, success_message="Success", error_message="Error"):
    transaction = request.get_json()

    required = ['type', 'sender', 'data', 'signature']
    if not all(k in transaction for k in required):
        return 'Missing values', 400

    try:
        blockchain_handler(transaction)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    response = {'message': success_message}
    return jsonify(response), 200

@bp.route('/transactions/new_generic', methods=['POST'])
def new_generic():
    return generic_transaction_handler(
        request, 
        blockchain.transacting.new_transaction, 
        "Transaction added to mempool", 
        "Error adding transaction to mempool"
    )

@bp.route('/upload_chunk', methods=['POST'])
def upload_chunk():
    file = request.files['file']
    stream_id = request.form['stream_id']

    file_data = file.read()
    chunk_hash = hashlib.sha256(file_data).hexdigest()
    
    save_dir = f'{CURRENT_DIR}/'
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f'{chunk_hash}.png')
    
    with open(path, 'wb') as f:
        f.write(file_data)
    
    return jsonify({
        'chunk_hash': chunk_hash,
        'chunk_path': path
    })
from flask import Flask, jsonify, request
import json, hashlib, os

from blockchain.blockchain import Blockchain, CURRENT_DIR, NUGGETS_DIR
from blockchain.enums.verbosity import Verbosity
from blockchain.utilities.keypair import load_or_create_keypair

import blockchain.utilities.crypto as crypto_utils
import blockchain.utilities.proof as proofing

# Keypair management
private_key, public_key = load_or_create_keypair()
node_identifier = public_key.to_string().hex()

# Object management
app = Flask(__name__)
blockchain = Blockchain(verbosity=Verbosity.SUPER_VERBOSE)

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = proofing.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    tx = {
        "sender":public_key.to_string().hex(),
        "data": {
            "recipient":node_identifier,
            "amount":1,
        },
        "type": "transfer.mine_reward"
    }

    message = json.dumps(tx, sort_keys=True).encode()
    signature = private_key.sign(message).hex()

    tx['signature'] = signature

    blockchain.new_transaction(tx)

    # Forge the new Block by adding it to the chain
    previous_hash = crypto_utils.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    transaction = request.get_json()

    # Required fields for generic transaction structure
    required = ['type', 'sender', 'data', 'signature']
    if not all(k in transaction for k in required):
        return 'Missing values', 400

    try:
        index = blockchain.new_transaction(transaction)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/upload_chunk', methods=['POST'])
def upload_chunk():
    file = request.files['file']
    stream_id = request.form['stream_id']

    file_data = file.read()
    chunk_hash = hashlib.sha256(file_data).hexdigest()
    
    save_dir = f'{NUGGETS_DIR}/'
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f'{chunk_hash}.jpg')
    
    with open(path, 'wb') as f:
        f.write(file_data)
    
    return jsonify({
        'chunk_hash': chunk_hash,
        'chunk_path': path
    })


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'livestreams': blockchain.livestreams,
        'current_transactions': blockchain.current_transactions,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5069, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
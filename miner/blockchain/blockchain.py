from ecdsa import VerifyingKey, BadSignatureError, SECP256k1
import lmdb
import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

from miner.blockchain.enums.verbosity import Verbosity

import miner.blockchain.utilities.crypto as crypto

from miner.blockchain.state.storage import PersistentStorage
from miner.blockchain.state.mining import Mining

'''

Terminology of note:

- "current" instructions are equivalent to mempools in eth and bitcoin

Instruction types:

- start_livestream - establishes a "Stream Derived Address" based on your wallet and puts all money provided within it (miners draw from it to pay for verifying livstream nuggets)
    - stream chunk is hashed and stored in the CURRENT_DIR
    - when new_block() is called, the transaction is computed into the block
        - chunk hash is added to the livestream
        - chunk file is moved to the NUGGETS_DIR
- add_chunk - adds a nugget to a specified livestream (can only be yours)
- add_funds - adds money to your "Stream Derived Address"
- transfer is a generic transaction that requries "amount" and balance"
    - transfer.mine_reward - transaction to give miner reward for mining

'''

NUGGETS_DIR = 'data/nuggets'
CURRENT_DIR = 'data/current'



class Blockchain:
    '''
    
    (Intended) available functionality:

    # general
    - utilities
        - crypto    
            - hash
            - verify_signature
            - derive_sda
    - enums
        - verbosity

    # blockchain class (self)
        - persistent_storage
            - save_data
            - load_data
        - mining
            - new_block
            - resolve_conflicts
        - accounting
            - get_wallet_balance
            - get_account
        - transacting
            - new_transaction
            - process_transaction
        - networking
            - register_node
        
    '''

    def __init__(self, verbosity = Verbosity.NORMAL):
        self.current_transactions = []
        self.chain = []
        self.livestreams = {}
        self.nodes = set()

        self.verbosity = verbosity

        self.persistent_storage = PersistentStorage(self, 'blockchain_data')
        self.mining = Mining(self)

        if not self.persistent_storage.load_data():
            # Create the genesis block (assuming that for now we're the first to exist)
            self.mining.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')
    
    def new_transaction(self, tx):

        tx_data = {
            'sender': tx['sender'],
            'type': tx['type'],
            'data': tx['data']
        }

        if not crypto.verify_signature(tx['sender'], tx['signature'], tx_data):
            raise ValueError("Invalid signature")

        self.current_transactions.append({
            'sender': tx['sender'],
            'signature': tx['signature'],
            'type': tx['type'],
            'data': tx['data']
        })

        return self.last_block['index'] + 1
        
    def process_transaction(self, tx):
        tx_type = tx['type']
        data = tx['data']

        if tx_type == 'start_livestream':
            stream_id = Blockchain.derive_sda(tx['sender'], data['stream_id'])
            initial_funds = data['initial_funds']
            print(f"Started livestream at {stream_id} with {initial_funds} funds")

            self.livestreams[stream_id] = {'funds': initial_funds}

        elif tx_type == 'add_chunk':
            stream_id = Blockchain.derive_sda(tx['sender'], data['stream_id'])
            #chunk_hash = data['chunk_hash']
            #chunk_index = data['chunk_index']
            #print(f"Added chunk {chunk_index} with hash {chunk_hash} to {stream_id}")

        elif tx_type == 'add_funds':
            stream_id = Blockchain.derive_sda(tx['sender'], data['stream_id'])
            funds = data['amount']
            print(f"Added {funds} funds to {stream_id}")

        elif tx_type.startswith('transfer'):
            print(f"Transfer {data['amount']} from {tx['sender']} to {data['recipient']}")

            sender_balance = self.get_wallet_balance(tx['sender'])
            recipient_balance = self.get_wallet_balance(data['recipient'])

            if sender_balance < data['amount'] and tx_type != 'transfer.mine_reward':
                raise ValueError("Not enough funds to transfer")

            data['balances'] = {
                tx['sender']: sender_balance - data['amount'],
                data['recipient']: recipient_balance + data['amount']
            }

            if tx_type == 'transfer.mine_reward':
                print(f"Received miner reward of {data['amount']} from {tx['sender']}")

        else:
            print("Unknown transaction type:", tx_type)

    def get_wallet_balance(self, pubkey_hex):
        balance = 0
        # Iterate backwards through chain
        for block in reversed(self.chain):
            for tx in block['transactions']:
                if tx['type'].startswith('transfer'):
                    try:
                        balance = tx['data']['balances'][pubkey_hex]
                    except:
                        pass
        return balance

    @property
    def last_block(self):
        print(self.chain)
        return self.chain[-1]



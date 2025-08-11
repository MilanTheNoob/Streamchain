import os
from enum import Enum
import json
import appdirs
from ecdsa import SigningKey, SECP256k1, VerifyingKey
from typing import Tuple

import miner.blockchain.types.transactions as tx_types
from miner.blockchain.enums.transaction_type import TransactionType

DEFAULT_KEYPAIR_FILE = os.path.join(appdirs.user_data_dir('streamchain'), 'keypair.json')

def load_or_create_keypair(keypair_file: str = DEFAULT_KEYPAIR_FILE) -> Tuple[SigningKey, VerifyingKey]:
    """
    Create or load a keypair at %appdata%/streamchain/keypair.json
    """

    keypair_dir = os.path.dirname(keypair_file)
    if not os.path.exists(keypair_dir):
        os.makedirs(keypair_dir)
    if os.path.exists(keypair_file):
        with open(keypair_file, 'r') as f:
            data = json.load(f)
            private_key = SigningKey.from_string(bytes.fromhex(data['private_key']), curve=SECP256k1)
            public_key = private_key.get_verifying_key()
            print("Loaded existing keypair.")
    else:
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.get_verifying_key()
        with open(keypair_file, 'w') as f:
            json.dump({
                'private_key': private_key.to_string().hex(),
                'public_key': public_key.to_string().hex()
            }, f)
        print("Generated new keypair.")

    return private_key, public_key

def sign_transaction(tx: tx_types.TransactionObject, keypair: Tuple[SigningKey, VerifyingKey]):
    if 'signature' in tx:
        raise ValueError("Transaction is already signed (contains a signature)")

    message = json.dumps(tx, sort_keys=True, default=lambda o: o.value if isinstance(o, Enum) else o).encode('utf-8')
    signature = keypair[0].sign(message).hex()

    tx['signature'] = signature

def create_mine_reward_tx(miner_keypair: Tuple[SigningKey, VerifyingKey]) -> tx_types.TransactionObject:
    tx = {
        'type': TransactionType.TRANSFER_MINE_REWARD,
        "sender":miner_keypair[1].to_string().hex(),
        "data": {
            "recipient":miner_keypair[1].to_string().hex(),
            "amount":1,
        },
        "type": "transfer.mine_reward"
    }

    sign_transaction(tx, miner_keypair)

    return tx

def create_generic_tx(sender_keypair: Tuple[SigningKey, VerifyingKey], receiver_pubkey: VerifyingKey, amount: int) -> tx_types.TransactionObject:
    """
    Create a generic transaction that sends a provided amount of tokens to a specified public key
    """

    if not receiver_pubkey or not isinstance(receiver_pubkey, VerifyingKey):
        raise ValueError("Invalid receiver public key")

    tx_data = {
        'type': TransactionType.TRANSFER,
        'sender': sender_keypair[1].to_string().hex(),
        'data': {
            'amount': amount,
            'recipient': receiver_pubkey.to_string().hex()
        }
    }

    sign_transaction(tx_data, sender_keypair)

    return tx_data

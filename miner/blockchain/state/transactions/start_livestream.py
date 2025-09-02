import miner.blockchain.utilities.crypto as crypto
from miner.blockchain.constants import *

from mmr import MMR

def start_livestream(blockchain, tx_data, sender):
    stream_id = crypto.derive_sda(sender, tx_data['stream_name'])
    print(f"stream name: {tx_data['stream_name']}, stream id: {stream_id}, sender: {sender}")
    initial_funds = tx_data['initial_funds']
    
    print(f"Started livestream at {stream_id} with {initial_funds} funds")

    chunks = MMR()

    owner_balance = blockchain.accounting.get_wallet_balance(sender)

    if owner_balance < initial_funds:
        raise ValueError("Insufficient funds to start livestream")

    tx_data['balances'] = {
        stream_id: {
            'type': 'sda',
            'funds': initial_funds,
            'chunks': chunks.serialize()
        },
        sender: owner_balance-initial_funds
    }
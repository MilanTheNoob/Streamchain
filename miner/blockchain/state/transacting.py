from miner.blockchain.utilities import crypto as crypto
import miner.blockchain.utilities.sanitizing as sanitizing
import miner.blockchain.types.transactions as tx_types
import miner.blockchain.state.transactions as transactions
from miner.blockchain.enums.transaction_type import TransactionType

import typing

class Transacting:
    def __init__(self, parent):
        self.parent = parent

    def new_transaction(self, tx: tx_types.TransactionObject):
        tx_data = {
            'sender': tx['sender'],
            'type': tx['type'] if isinstance(tx['type'], str) else tx['type'].value,
            'data': tx['data']
        }

        if not crypto.verify_signature(tx['sender'], tx['signature'], tx_data):
            raise ValueError("Invalid signature")

        self.parent.current_transactions.append({
            'sender': tx['sender'],
            'signature': tx['signature'],
            'data': tx['data'],
            'type': tx['type'] if isinstance(tx['type'], str) else tx['type'].value,
        })

        return self.parent.last_block['index'] + 1

    def new_multiple_transactions(self, txs: typing.List[typing.Dict[str, typing.Any]]):
        for tx in txs:
            self.new_transaction(tx)
        
    def process_transaction(self, tx):
        tx_type = tx['type']
        data = tx['data']

        # All transaction functions must accept the parameters: blockchain object, transaction data, sender
        transactions_dict = {
            TransactionType.START_LIVESTREAM: transactions.start_livestream,
            TransactionType.ADD_CHUNK: transactions.add_chunk,
            TransactionType.ADD_FUNDS: transactions.add_funds,
            TransactionType.TRANSFER: transactions.transfer,
            TransactionType.TRANSFER_MINE_REWARD: transactions.mine_reward,
            TransactionType.CHALLENGE_STORER: transactions.challenge_storer 
        }

        transactions_dict[TransactionType(tx_type)](self.parent, data, tx['sender'])
    
    def get_transaction(self, signature: str) -> typing.Dict[str, typing.Any]:
        for block in reversed(self.parent.chain):
            for tx in block['transactions']:
                if tx['signature'] == signature:
                    return tx
                
        return None
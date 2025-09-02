import typing, requests, time, json, os

import miner.blockchain.utilities.crypto as crypto
import miner.blockchain.utilities.keypair as keypair

from miner.blockchain.utilities.proof import valid_chain
from miner.blockchain.constants import *

from miner.blockchain.enums.transaction_type import TransactionType

class Mining:
    def __init__(self, parent):
        self.parent = parent

    def resolve_conflicts(self) -> bool:
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        """
        neighbours = self.parent.nodes
        new_chain = None
        max_length = len(self.parent.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof: int, previous_hash: str) -> typing.Dict[str, typing.Any]:
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        """
        
        has_reward_tx = 0 # Counter of how many transfer.mine_reward exist, we are only to allow one to exist

        # Process transactions, removing any that fail (atomicity and all that bullshit)
        for tx in self.parent.current_transactions:
            try:
                if tx['type'] == TransactionType.TRANSFER_MINE_REWARD.value:
                    has_reward_tx += 1

                self.parent.transacting.process_transaction(tx)
            except ValueError as e:
                print(e)
                self.parent.current_transactions.remove(tx)

        if has_reward_tx > 1:
            raise ValueError(f"There should precisely be one transfer_mine_reward transaction per block, there are {has_reward_tx}")

        block = {
            'index': len(self.parent.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.parent.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or crypto.hash(self.parent.chain[-1]),
        }

        # Wipe the mempool temp directory
        '''
        for file in os.listdir(CURRENT_DIR):
            file_path = os.path.join(CURRENT_DIR, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error while deleting file {file_path}: {e}")

        '''

        if self.parent.event_handler:
            self.parent.event_handler.on_new_block(block)

        self.parent.current_transactions = []
        self.parent.chain.append(block)
        self.parent.persistent_storage.save_data()

        return block

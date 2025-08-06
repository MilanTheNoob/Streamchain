import typing, requests, time
import crypto

from miner.blockchain.utilities.proof import valid_chain

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

        # We're only looking for chains longer than ours
        max_length = len(self.parent.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
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

        block = {
            'index': len(self.parent.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.parent.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or crypto.hash(self.parent.chain[-1]),
        }

        for tx in self.parent.current_transactions:
            self.parent.transacting.process_transaction(tx)

        self.parent.current_transactions = [] # Reset the "mempool"

        self.parent.chain.append(block)
        self.parent.persistent_storage.save_data()
        return block

from ecdsa import VerifyingKey, BadSignatureError, SECP256k1
import typing, hashlib

from miner.blockchain.enums.verbosity import Verbosity
import miner.blockchain.utilities.crypto as crypto

def valid_chain(chain, verbosity = Verbosity.NORMAL) -> bool:
    """
    Determine if a given blockchain is valid

    :param chain: A blockchain
    :return: True if valid, False if not
    """

    last_block = chain[0]
    current_index = 1

    while current_index < len(chain):
        block = chain[current_index]
        if verbosity > Verbosity.NORMAL:
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

        # Check hash
        last_block_hash = crypto.hash(last_block)
        if block['previous_hash'] != last_block_hash:
            return False

        # Check proof of work
        if not valid_proof(last_block['proof'], block['proof'], last_block_hash):
            return False

        # Check transaction validity
        for tx in block['transactions']:
            tx_data = {
                'sender': tx['sender'],
                'type': tx['type'],
                'data': tx['data']
            }
            if not crypto.verify_signature(tx['sender'], tx['signature'], tx_data):
                return False

        last_block = block
        current_index += 1

    return True

def valid_proof(last_proof: int, proof: int, last_hash: str) -> bool:
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

def proof_of_work(last_block):
    """
    Simple Proof of Work Algorithm:

        - Find a number p' such that hash(pp') contains leading 4 zeroes
        - Where p is the previous proof, and p' is the new proof
        
    :param last_block: <dict> last Block
    :return: <int>
    """

    last_proof = last_block['proof']
    last_hash = crypto.hash(last_block)

    proof = 0
    while valid_proof(last_proof, proof, last_hash) is False:
        proof += 1

    return proof
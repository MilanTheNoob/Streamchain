from miner.blockchain.enums.verbosity import Verbosity

from miner.blockchain.constants import *

from miner.blockchain.state.storage import PersistentStorage
from miner.blockchain.state.mining import Mining
from miner.blockchain.state.transacting import Transacting
from miner.blockchain.state.accounting import Accounting
from miner.blockchain.state.networking import Networking

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



class Blockchain:
    '''
    
    (Intended) available functionality:

    # general
    - keypair
        - load_or_create_keypair
        - create_generic_tx
        - create_mine_reward_tx
        - create_start_livestream_tx
        - sign_transaction
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
            - get_chain_account
        - transacting
            - new_transaction
            - process_transaction
            - new_multiple_transactions
            - find_transaction_by_id
            - find_transaction_by_signature
        - networking
            - register_node
        
    '''

    def __init__(self, verbosity = Verbosity.NORMAL, event_handler = None):
        self.current_transactions = [] # Mempool
        self.chain = [] # chain
        self.nodes = set() # our connections to other people
        self.event_handler = event_handler

        self.verbosity = verbosity

        self.persistent_storage = PersistentStorage(self, 'blockchain_data')
        self.mining = Mining(self)
        self.transacting = Transacting(self)
        self.accounting = Accounting(self)
        self.networking = Networking(self)

        # CONSTANTS
        self.MINE_REWARD_AMOUNT = 1

        if not self.persistent_storage.load_data(): 
            # Create the genesis block (assuming that for now we're the first to exist)
            self.mining.new_block(previous_hash='1', proof=100)
    
    @property
    def last_block(self):
        return self.chain[-1]

import unittest

from miner.blockchain.blockchain import Blockchain
from miner.blockchain.utilities import keypair

class BlockchainTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blockchain = Blockchain()
        cls.keypair = keypair.load_or_create_keypair()
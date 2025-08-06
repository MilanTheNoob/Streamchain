import unittest

from miner.blockchain.blockchain import Blockchain

class BlockchainTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blockchain = Blockchain()
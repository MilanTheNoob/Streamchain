import unittest

from miner.tests.test_base import BlockchainTestBase

class MiningTest(BlockchainTestBase):
    def test_01_build_empty_block(self):
        self.assertEqual(self.blockchain.current_transactions, [], "The mempool is not empty")

        block = self.blockchain.mining.new_block(100, '1')

        self.assertEqual(block['transactions'], [], "The block is not empty (it should be)")

import unittest

from miner.tests.test_base import BlockchainTestBase

class MiningTest(BlockchainTestBase):
    def test_new_block(self):
        print("hello world")
        self.assertEqual(1, 1)

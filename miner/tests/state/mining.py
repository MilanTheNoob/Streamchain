import unittest

from miner.tests.test_base import BlockchainTestBase

from miner.blockchain.utilities import keypair

class MiningTest(BlockchainTestBase):
    def test_mining__01__build_empty_block_without_payout(self):
        self.assertEqual(self.blockchain.current_transactions, [], "The mempool is not empty")

        with self.assertRaises(expected_exception=ValueError, msg="Should not be allowed to create a block without rewarding the miner"):
            block = self.blockchain.mining.new_block(100, '1')
            self.assertEqual(block['transactions'], [], "The block is not empty (it should be)")
        
    def test_mining__02__build_empty_block_with_payout(self):
        self.assertEqual(self.blockchain.current_transactions, [], "The mempool is not empty")

        self.blockchain.transacting.new_transaction(keypair.create_mine_reward_tx(self.keypair))

        block = self.blockchain.mining.new_block(100, '1')

        self.assertEqual(self.blockchain.current_transactions, [], "The mempool has not been reset after mining a block")

    def test_mining__03__build_block_with_transactions(self):
        self.assertEqual(self.blockchain.current_transactions, [], "The mempool is not empty")

        self.blockchain.transacting.new_multiple_transactions([
            keypair.create_generic_tx(self.keypair, self.keypair[1], 1),
            keypair.create_mine_reward_tx(self.keypair)
        ])

        block = self.blockchain.mining.new_block(100, '1')

        self.assertEqual(self.blockchain.current_transactions, [], "The mempool has not been reset after mining a block")
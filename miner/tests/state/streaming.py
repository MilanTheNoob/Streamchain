import unittest

from miner.tests.test_base import BlockchainTestBase

from miner.blockchain.utilities import keypair

class StreamingTest(BlockchainTestBase):
    def test_streaming__01__create_stream(self):
        self.assertEqual(len(self.blockchain.livestreams), 0, "There should be no livestreams before creating one")

        self.blockchain.transacting.new_multiple_transactions([
            keypair.create_start_livestream_tx(self.keypair),
            keypair.create_mine_reward_tx(self.keypair),
        ])

        self.blockchain.mining.new_block(100, '1')

        self.assertEqual(len(self.blockchain.livestreams), 1, "There should be one livestream")

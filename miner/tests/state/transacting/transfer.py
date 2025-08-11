import unittest, typing
from ecdsa import VerifyingKey, SigningKey

from miner.tests.test_base import BlockchainTestBase
import miner.blockchain.types.transactions as tx_types

from miner.blockchain.utilities import keypair

def blockchain_utility(obj, test_keypair: typing.Tuple[VerifyingKey, SigningKey], txs: typing.List[tx_types.TransactionObject]):
    obj.transacting.new_multiple_transactions([
        *txs,
        keypair.create_mine_reward_tx(test_keypair),
    ])
    obj.mining.new_block(100, '1')

class TransactingTransferTest(BlockchainTestBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        pub_hex = cls.keypair[1].to_string().hex()
        diff = 100 - cls.blockchain.accounting.get_wallet_balance(pub_hex)

        while diff > 0: # Mine enough empty blocks so that we have enough money to perform the tests
            blockchain_utility(cls.blockchain, cls.keypair, [])
            diff -= 1

        print(f"We now have a balance of {cls.blockchain.accounting.get_wallet_balance(pub_hex)}")

    def test_transacting_transfer__01__valid_transfer(self):
        blockchain_utility(self.blockchain, self.keypair, [
            keypair.create_generic_tx(self.keypair, self.keypair[1], 1),
        ])

    def test_transacting_transfer__02__invalid_transfer__too_big(self):
        with self.assertRaises(expected_exception=ValueError, msg="Should not be able to transfer more than account balance"):
            blockchain_utility(self.blockchain, self.keypair, [
                keypair.create_generic_tx(self.keypair, self.keypair[1], 9999),
            ])

    def test_transacting_transfer_03_invalid_transfer__no_recipient(self):
        with self.assertRaises(expected_exception=ValueError, msg="Should not have a transaction with no recipient"):
            self.blockchain.transacting.new_multiple_transactions([
                keypair.create_generic_tx(self.keypair, None, 1),
                keypair.create_mine_reward_tx(self.keypair),
            ])
            self.blockchain.mining.new_block(100, '1')

    def test_transacting_transfer__04__invalid_transfer_negative__negative_amount(self):
        with self.assertRaises(expected_exception=ValueError, msg="Should not be given a negative reward"):
            blockchain_utility(self.blockchain, self.keypair, [
                keypair.create_generic_tx(self.keypair, self.keypair[1], -1),
            ])

    def test_transacting_transfer__(self):
        self.assertTrue(False, "Empty test")

    '''
        with self.assertRaises(expected_exception=ValueError, msg="Should not be allowed to create a block without rewarding the miner"):
            block = self.blockchain.mining.new_block(100, '1')
            self.assertEqual(block['transactions'], [], "The block is not empty (it should be)")
'''
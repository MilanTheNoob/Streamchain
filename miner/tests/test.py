import unittest
import os, sys

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    from miner.tests.state.mining import MiningTest
    from miner.tests.state.transacting.transfer import TransactingTransferTest

    suite.addTests(test_loader.loadTestsFromTestCase(MiningTest))
    suite.addTests(test_loader.loadTestsFromTestCase(TransactingTransferTest))

    unittest.TextTestRunner(verbosity=2).run(suite)
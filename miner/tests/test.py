import unittest
import os, sys

from miner.tests.state.mining import MiningTest

class BlockchainTests(unittest.TestCase):
    def test_run_all(self):
        test_loader = unittest.TestLoader()
        suite = unittest.TestSuite()

        suite.addTests(test_loader.loadTestsFromTestCase(MiningTest))

        unittest.TextTestRunner(verbosity=2).run(suite)

unittest.main()
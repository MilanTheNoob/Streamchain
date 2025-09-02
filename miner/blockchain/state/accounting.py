import typing

from miner.blockchain.types.accounts import Account

class Accounting:
    def __init__(self, parent):
        self.parent = parent

    def get_wallet_balance(self, pubkey_hex: str) -> int:
        balance = 0
        # Iterate backwards through chain
        for block in reversed(self.parent.chain):
            for tx in block['transactions']:
                if tx['type'].startswith('transfer'):
                    try:
                        balance = tx['data']['balances'][pubkey_hex]
                        if balance:
                            return balance
                    except:
                        pass
        return -1

    def get_chain_account(self, pubkey_hex: str) -> Account:
        """
        Get the most recent state of an onchain account (i.e a data structure that resides within the balances of finalized transactions)
        """

        for block in reversed(self.parent.chain):
            for tx in block['transactions']:
                if 'balances' in tx['data'].keys():
                    try:
                        account = tx['data']['balances'][pubkey_hex]
                        if account:
                            return account.copy()
                    except:
                        pass
        return None
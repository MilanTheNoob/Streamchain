import typing

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
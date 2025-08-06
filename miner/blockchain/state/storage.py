import lmdb, json, typing

class PersistentStorage:
    def __init__(self, parent, env_dir: str, env_size=10**9):
        self.env = lmdb.open(env_dir, map_size=env_size)
        self.parent = parent

    def save_data(self):
        with self.env.begin(write=True) as txn:
            txn.put(b'chain', json.dumps(self.parent.chain).encode())
            txn.put(b'livestreams', json.dumps(self.parent.livestreams).encode())
            txn.put(b'current_transactions', json.dumps(self.parent.current_transactions).encode())

    def load_data(self) -> bool:
        with self.env.begin() as txn:
            chain_data = txn.get(b'chain')
            livestreams_data = txn.get(b'livestreams')
            transactions_data = txn.get(b'current_transactions')

            if chain_data:
                self.parent.chain = json.loads(chain_data.decode())
            if livestreams_data:
                self.parent.livestreams = json.loads(livestreams_data.decode())
            if transactions_data:
                self.parent.current_transactions = json.loads(transactions_data.decode())

        return bool(self.parent.chain)

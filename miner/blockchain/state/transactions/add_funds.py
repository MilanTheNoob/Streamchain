import miner.blockchain.utilities.crypto as crypto

def add_funds(blockchain, data, sender):
     stream_id = crypto.derive_sda(sender, data['stream_id'])
     funds = data['amount']
     print(f"Added {funds} funds to {stream_id}")

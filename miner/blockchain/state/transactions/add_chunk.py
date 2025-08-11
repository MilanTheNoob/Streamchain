import miner.blockchain.utilities.crypto as crypto

def add_chunk(self, data, sender):
    stream_id = crypto.derive_sda(sender, data['stream_id'])
    #chunk_hash = data['chunk_hash']
    #chunk_index = data['chunk_index']
    #print(f"Added chunk {chunk_index} with hash {chunk_hash} to {stream_id}")


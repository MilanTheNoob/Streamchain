import os, hashlib

import miner.blockchain.utilities.crypto as crypto
from miner.blockchain.constants import *

from miner.blockchain.types.accounts import StreamAccount
from miner.blockchain.constants import *

from mmr import MMR

def add_chunk(self, data, sender):
    stream_id = data['stream_id']
    sda = self.accounting.get_chain_account(stream_id)    

    '''
    
    To add a chunk, we expect within the data:

    - stream_id - which must exist on the chain (emphasis on ID, not the name)
    - chunk_hash - hash of the chunk
    
    We also expect the chunk to be stored in the NUGGETS_DIR, and to be named appropriately,
    furthermore, all nuggets are deleted during mining, so failed attempts to add chunks require chunks to be readded
    
    '''

    if not sda:
        raise ValueError(f"Stream {stream_id} does not exist")

    if sda['funds'] < CHUNK_UPLOAD_COST:
        raise ValueError("Insufficient funds to add chunk")

    sda['funds'] -= CHUNK_UPLOAD_COST

    if not os.path.exists(f"{CURRENT_DIR}/{data['chunk_hash']}.png"):
        raise ValueError("Chunk not found")

    # Check that it is smaller than MAX_CHUNK_SIZE
    if os.path.getsize(f"{CURRENT_DIR}/{data['chunk_hash']}.png") > MAX_CHUNK_SIZE:
        raise ValueError("Chunk too large")

    # Check that hash of the chunk is correct 
    with open(f"{CURRENT_DIR}/{data['chunk_hash']}.png", 'rb') as f:
        if hashlib.sha256(f.read()).hexdigest() != data['chunk_hash']:
            raise ValueError("Chunk hash incorrect")

    # Copy the chunk to NUGGETS_DIR
    os.makedirs(f"{NUGGETS_DIR}/{stream_id}", exist_ok=True)
    os.rename(f"{CURRENT_DIR}/{data['chunk_hash']}.png", f"{NUGGETS_DIR}/{stream_id}/{data['chunk_hash']}.png")

    # Deserialize the MMR
    mmr = MMR.deserialize(sda.get('chunks', '[]'))

    # Add the chunk hash to the MMR
    print(type(data['chunk_hash']), ", ", data['chunk_hash'])
    mmr.add(data['chunk_hash'].encode('utf-8'))

    # Serialize the MMR
    sda['chunks'] = mmr.serialize()

    data["balances"] = {
        stream_id: sda
    }


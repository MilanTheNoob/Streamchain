import json
import hashlib
import requests

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from blockchain.utilities.keypair import load_or_create_keypair

# Load the keypair
priv, pub = load_or_create_keypair()

# Upload the image chunk first
with open('test.jpg', 'rb') as f:
    files = {'file': f}
    data = {
        'stream_id': 'mystream'
    }
    upload_response = requests.post('http://localhost:5069/upload_chunk', files=files, data=data)

if upload_response.status_code != 200:
    raise Exception("Failed to upload chunk:", upload_response.text)

upload_data = upload_response.json()
chunk_hash = upload_data['chunk_hash']
chunk_path = upload_data['chunk_path']

print("Uploaded chunk. Hash:", chunk_hash)
print("Saved at:", chunk_path)

# Create the add_chunk transaction
tx = {
    'type': 'add_chunk',
    'sender': pub.to_string().hex(),
    'data': {
        'stream_id': 'mystream',
        'chunk_hash': chunk_hash,
    }
}

# Sign the transaction
message = json.dumps(tx, sort_keys=True).encode()
signature = priv.sign(message).hex()

# Build payload
payload = {
    **tx,
    'signature': signature,
}
print("Payload:", payload)

# POST to blockchain
response = requests.post('http://localhost:5069/transactions/new', json=payload)

print("Status:", response.status_code)
print("Response:", response.text)

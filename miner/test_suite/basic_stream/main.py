import requests, json, random

from miner.blockchain.utilities import keypair, crypto
from miner.test_suite.connection import ConnectionObject

# Create the connection
connection = ConnectionObject(
    ("localhost", 5069), 
    keypair.load_or_create_keypair()
)

stream_name = f"stream_{random.randint(0, 100)}"
print(f"Stream name: {stream_name}, public key: {connection.keypair[1].to_string().hex()}")
stream_id = crypto.derive_sda(connection.keypair[1].to_string().hex(), stream_name)
print("Stream SDA: ", stream_id)

# Create SDA Account
start_stream_tx = keypair.create_start_livestream_tx(connection.keypair, stream_name, 5)
connection.submit_request(start_stream_tx)
connection.submit_request(None, "mine", requests.get)

start_stream_status = connection.wait_for_transaction_outcome(start_stream_tx['signature'])

# Add chunk
connection.transmit_chunk(
    stream_id=stream_id,
    file_path="miner/test_suite/basic_stream/test.png"
)

add_chunk_tx = keypair.add_livestream_chunk_tx(crypto.hash_file("miner/test_suite/basic_stream/test.png"), stream_id=stream_id)
connection.submit_request(add_chunk_tx)

connection.submit_request(None, "mine", requests.get, True)
add_chunk_status = connection.wait_for_transaction_outcome(add_chunk_tx['signature'])

# Logging
print("New chunk added to stream: ", json.dumps(add_chunk_status, indent=4))

after_stream_status = connection.wait_for_transaction_outcome(start_stream_tx['signature'])
after_stream_new_status = connection.wait_and_grab_account(list(add_chunk_status['data']['balances'].keys())[0])

assert after_stream_status == start_stream_status

print("Stream status now: ", json.dumps(after_stream_new_status, indent=4))
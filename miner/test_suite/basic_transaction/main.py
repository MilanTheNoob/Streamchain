import requests, json

from miner.blockchain.utilities import keypair
from miner.test_suite.connection import ConnectionObject

connection = ConnectionObject(
    ("localhost", 5069), 
    keypair.load_or_create_keypair()
)

my_cute_tx = keypair.create_generic_tx(connection.keypair, connection.keypair[1], 1)
signature = my_cute_tx.get("signature")

connection.submit_request(my_cute_tx, suppress=True)
connection.submit_request(None, "mine", requests.get, True)
response = connection.wait_for_transaction_outcome(signature)

print(json.dumps(response, indent=4))

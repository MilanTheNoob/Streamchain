from miner.blockchain.blockchain import Blockchain, CURRENT_DIR, NUGGETS_DIR
from miner.blockchain.enums.verbosity import Verbosity
import miner.blockchain.utilities.keypair as keypair

from miner.server.events import BlockchainEventHandler
from miner.server.socket import socketio

private_key, public_key = keypair.load_or_create_keypair()
node_identifier = public_key.to_string().hex()

event_handler = BlockchainEventHandler(socketio)

blockchain = Blockchain(verbosity=Verbosity.SUPER_VERBOSE, event_handler=event_handler)

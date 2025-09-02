from flask_socketio import Namespace, emit, socketio
from miner.server.config import blockchain, private_key, public_key

class MinerNamespace(Namespace):
    def on_connect(self):
        print("Miner client connected")

    def on_disconnect(self):
        print("Miner client disconnected")
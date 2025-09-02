class BlockchainEventHandler:
    def __init__(self, socketio):
        self.socketio = socketio

    def on_new_block(self, block):
        self.socketio.emit("new_block", block, namespace="/miner",)

    def on_new_transaction(self, tx):
        self.socketio.emit("new_transaction", tx, namespace="/miner",)

    def on_chain_synced(self, state):
        self.socketio.emit("chain_synced", state, namespace="/miner",)

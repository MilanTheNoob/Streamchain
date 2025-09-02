import socketio

# Create a Socket.IO client
sio = socketio.Client()

# Event handlers
@sio.event(namespace="/miner")
def connect():
    print("Connected to miner namespace")

@sio.event(namespace="/miner")
def disconnect():
    print("Disconnected from miner namespace")
    exit(0)

@sio.on("new_block", namespace="/miner")
def on_new_block(data):
    print("New block received:", data)

@sio.on("new_transaction", namespace="/miner")
def on_new_transaction(data):
    print("New transaction received:", data)

def main():
    # Adjust the URL/port to match your Flask-SocketIO server
    sio.connect("http://localhost:5069", namespaces=["/miner"])
    print("Listening for events...")

    # Keep the client alive
    sio.wait()

if __name__ == "__main__":
    main()

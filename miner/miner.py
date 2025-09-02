from miner.server.server import *
from miner.server.config import *

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5069, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    socketio.run(app, host="0.0.0.0", port=port)
    #app.run(host='0.0.0.0', port=port)
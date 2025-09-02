from flask import Flask, jsonify, request
import json, hashlib, os
from flask_socketio import SocketIO

from miner.miner_ws import MinerNamespace
from miner.server.socket import socketio

from miner.server.config import * 
from miner.server.routes import *

app = Flask(__name__)
socketio.init_app(app)

app.register_blueprint(mining_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(networking_bp)
app.register_blueprint(state_bp)

socketio.on_namespace(MinerNamespace("/miner"))
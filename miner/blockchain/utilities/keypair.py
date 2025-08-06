import os
import json
from ecdsa import SigningKey, SECP256k1

DEFAULT_KEYPAIR_FILE = 'keypair.json'

def load_or_create_keypair(keypair_file=DEFAULT_KEYPAIR_FILE):
    if os.path.exists(keypair_file):
        with open(keypair_file, 'r') as f:
            data = json.load(f)
            private_key = SigningKey.from_string(bytes.fromhex(data['private_key']), curve=SECP256k1)
            public_key = private_key.get_verifying_key()
            print("Loaded existing keypair.")
    else:
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.get_verifying_key()
        with open(keypair_file, 'w') as f:
            json.dump({
                'private_key': private_key.to_string().hex(),
                'public_key': public_key.to_string().hex()
            }, f)
        print("Generated new keypair.")

    return private_key, public_key

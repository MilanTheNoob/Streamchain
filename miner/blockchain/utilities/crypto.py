from ecdsa import VerifyingKey, BadSignatureError, SECP256k1
import typing, json, hashlib

def verify_signature(sender_public_key_hex: str, signature_hex: str, tx_data: typing.Dict) -> bool:
    """
    Verify a given signature

    :param sender_public_key_hex: Public key of the sender
    :param signature_hex: Signature of the transaction
    :param tx_data: Transaction data
    """
    try:
        pubkey = VerifyingKey.from_string(bytes.fromhex(sender_public_key_hex), curve=SECP256k1)
        message = json.dumps(tx_data, sort_keys=True).encode()
        signature = bytes.fromhex(signature_hex)
        pubkey.verify(signature, message)
        return True
    except BadSignatureError:
        return False


def hash(block):
    """
    Creates a SHA-256 hash of a Block

    :param block: Block
    """

    # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def derive_sda(owner_pubkey: str, stream_id: str):
    """
    Derive a Stream Derived Address the owner and the stream name (id)

    :param owner_pubkey: Public key of the owner
    :param stream_id: Name of the stream
    """
    
    combined = f"{owner_pubkey}:{stream_id}".encode()
    return hashlib.sha256(combined).hexdigest()
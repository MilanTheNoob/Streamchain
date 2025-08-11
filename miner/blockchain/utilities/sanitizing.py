import typing 

def shorten_pubkey(pubkey: str) -> str:
    return pubkey[:6] + '...'

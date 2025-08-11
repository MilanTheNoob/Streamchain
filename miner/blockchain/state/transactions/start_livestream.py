import miner.blockchain.utilities.crypto as crypto

def start_livestream(blockchain, tx_data, sender):
    stream_id = crypto.derive_sda(sender, tx_data['stream_id'])
    initial_funds = tx_data['initial_funds']
    
    print(f"Started livestream at {stream_id} with {initial_funds} funds")

    blockchain.livestreams[stream_id] = {'funds': initial_funds}

    return tx_data
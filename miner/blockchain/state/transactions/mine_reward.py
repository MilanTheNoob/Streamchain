import miner.blockchain.state.accounting as accounting
import miner.blockchain.utilities.sanitizing as sanitizing

def mine_reward(blockchain, data, sender):
    print(f"Mine reward of {blockchain.MINE_REWARD_AMOUNT} to {sanitizing.shorten_pubkey(sender)}")

    sender_balance = blockchain.accounting.get_wallet_balance(sender)

    if sender_balance == -1:
        sender_balance = 0

    data['balances'] = {
        sender: sender_balance + blockchain.MINE_REWARD_AMOUNT,
    }
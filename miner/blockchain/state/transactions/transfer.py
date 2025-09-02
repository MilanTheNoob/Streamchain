import miner.blockchain.utilities.sanitizing as sanitizing

def transfer(blockchain, data, sender):
    print(f"Transfer {data['amount']} from {sanitizing.shorten_pubkey(sender)} to {sanitizing.shorten_pubkey(data['recipient'])}")
    
    sender_balance = blockchain.accounting.get_wallet_balance(sender)

    if sender == data['recipient']:
        data['balances'] = {
            sender: sender_balance
        }
        return

    recipient_balance = blockchain.accounting.get_wallet_balance(data['recipient'])

    if sender_balance < data['amount']:
        raise ValueError(f"Balance of {sender_balance} is insufficient for the transfer of {data['amount']} tokens")
    elif data['amount'] < 0:
        raise ValueError(f"Transfer amount cannot be negative: {data['amount']}")
    
    data['balances'] = {
        sender: sender_balance - data['amount'],
        data['recipient']: recipient_balance + data['amount']
    }

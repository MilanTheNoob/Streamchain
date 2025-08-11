from enum import Enum 

class TransactionType(Enum):
    TRANSFER='transfer'
    TRANSFER_MINE_REWARD='transfer.mine_reward'
    START_LIVESTREAM='start_livestream'
    ADD_CHUNK='add_chunk'
    ADD_FUNDS='add_funds'
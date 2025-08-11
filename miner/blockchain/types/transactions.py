import typing

from miner.blockchain.enums.transaction_type import TransactionType

class TransferTxData(typing.TypedDict):
    amount: int
    recipient: str

class CreateStreamTxData(typing.TypedDict):
    stream_id: str
    prepayment: int

class TransactionObject(typing.TypedDict):
    sender: str
    signature: str
    type: TransactionType
    data: TransferTxData | CreateStreamTxData

import typing 


class Account(typing.TypedDict):
    type: str

class StreamAccount(Account):
    funds: int
    chunks: str
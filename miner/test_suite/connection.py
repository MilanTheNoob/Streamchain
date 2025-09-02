import typing, requests, time, json
from enum import Enum
from ecdsa import SigningKey, SECP256k1, VerifyingKey

from miner.blockchain.utilities import keypair
from miner.blockchain.enums.transaction_type import TransactionType
from miner.blockchain.types.transactions import TransactionObject

# To do: create a type to represent a transaction response "TransactionResponse" or "TransactionOutcome" depending on desired poshness
class ConnectionObject:
    """
    A class representing a HTTP connection to the miner
    """
    def __init__(
            self, 
            address: typing.Tuple[str, int], 
            connection_pair: typing.Tuple[SigningKey, VerifyingKey] = keypair.load_or_create_keypair()
        ):
        self.address = address
        self.keypair = connection_pair

    def submit_request(self, tx: TransactionObject | None, endpoint: str = "transactions/new_generic", method = requests.post, suppress = False) -> typing.Dict[str, typing.Any] | requests.Response:
        if isinstance(endpoint, TransactionType):
            raise ValueError("Endpoints are no longer available for each transaction type, use `/transactions/new_generic` and specify type within")

        if tx and isinstance(tx['type'], Enum):
            tx['type'] = tx['type'].value

        if method == requests.post: # If using rq.post, we can make assumptions about parameters and the returned object
            response = method(
                f'http://{self.address[0]}:{self.address[1]}/{endpoint}', 
                json=tx, 
            )

            if not suppress and response.status_code != 200:
                raise Exception("Failed to submit transaction:", response.text)

            return response.json()
        else: # Otherwise be as generic as possible and hope someone looks at this source code 
            response = method(
                f'http://localhost:5069/{endpoint}', 
                json=tx
            )

            return response

    def transmit_chunk(self, stream_id: str , file_path: str) -> requests.Response:
        response = requests.post(
            f'http://{self.address[0]}:{self.address[1]}/upload_chunk', 
            files={'file': open(file_path, 'rb')}, 
            data={'stream_id': stream_id},
        )

        return response

    def wait_for_transaction_outcome(self, signature: str, wait_interval: int = 5, tries: int = 10) -> typing.Dict[str, typing.Any] | None:
        def get_tx():
            return self.submit_request(None, f"get_transaction/{signature}", requests.get).json()

        tx = get_tx()

        if not 'error' in tx.keys():
            return tx

        latest_hash, try_count = None, tx['latest_block_index']

        while try_count < tries: # Only try and get new tx when there is a new block, as the miner won't (and shouldn't) appreciate spamming for loops through blocks
            tries+=1
            current_block = self.submit_request(None, f"get_current_block_index", requests.get)

            if current_block == latest_hash:
                continue
            else:
                tx = get_tx()
                latest_hash = current_block

                if 'error' in tx.keys():
                    latest_hash = tx['latest_block_index']
                    time.sleep(wait_interval)
                else:
                    return tx
            
        return None

    def wait_and_grab_account(self, signature: str, wait_interval: int = 5, tries: int = 10) -> typing.Dict[str, typing.Any] | None:
        def get_tx():
            return self.submit_request(None, f"get_chain_account/{signature}", requests.get).json()

        tx = get_tx()

        if not 'error' in tx.keys():
            return tx

        latest_hash, try_count = None, tx['latest_block_index']

        while try_count < tries: # Only try and get new tx when there is a new block, as the miner won't (and shouldn't) appreciate spamming for loops through blocks
            tries+=1
            current_block = self.submit_request(None, f"get_current_block_index", requests.get)

            if current_block == latest_hash:
                continue
            else:
                tx = get_tx()
                latest_hash = current_block

                if 'error' in tx.keys():
                    latest_hash = tx['latest_block_index']
                    time.sleep(wait_interval)
                else:
                    return tx
            
        return None

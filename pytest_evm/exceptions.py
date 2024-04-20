from web3.exceptions import Web3Exception


class TransactionStatusError(Web3Exception):
    """Raised when a transaction fails to complete successfully."""

    def __init__(self, explorer_url: str):
        super().__init__(f"Transaction failed to complete. See more details: {explorer_url}")

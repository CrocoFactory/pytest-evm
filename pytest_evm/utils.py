import time
from functools import wraps
from evm_wallet import Wallet
from hexbytes import HexBytes
from web3 import Web3
from web3.middleware import geth_poa_middleware
from pytest_evm.exceptions import TransactionStatusError


def validate_status(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        wallet: Wallet = kwargs['wallet']
        tx_hash = await func(*args, **kwargs)
        status = (await wallet.provider.eth.wait_for_transaction_receipt(tx_hash)).get('status')
        if not status:
            explorer_url = wallet.get_explorer_url(tx_hash)
            raise TransactionStatusError(explorer_url)

    return wrapper


def get_last_transaction(wallet: Wallet, timeout: float = 10):
    w3 = Web3(Web3.HTTPProvider(wallet.network['rpc']))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    block_number = w3.eth.block_number
    start_block = 0
    end_block = block_number

    last_transaction = None
    wallet_address = wallet.public_key

    current_time = time.time()
    deadline = current_time + timeout
    for block in range(end_block, start_block - 1, -1):
        block_info = w3.eth.get_block(block, True)

        for tx in reversed(block_info['transactions']):
            if time.time() > deadline:
                raise TimeoutError(f'Timeout was exceeded for getting last transaction')
            try:
                from_address = tx['from'].lower()

                if isinstance(from_address, HexBytes):
                    from_address = from_address.hex()

                if wallet_address.lower() == from_address.lower():
                    last_transaction = tx
                    break
            except (AttributeError, KeyError):
                continue

        if last_transaction:
            break

    return last_transaction

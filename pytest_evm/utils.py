from functools import wraps
from evm_wallet import Wallet
from web3 import Web3
from web3.middleware import geth_poa_middleware


def validate_status(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        wallet = kwargs['wallet']
        tx_hash = await func(*args, **kwargs)
        status = bool(await wallet.provider.eth.wait_for_transaction_receipt(tx_hash))
        assert status

    return wrapper


def get_last_transaction(wallet: Wallet):
    w3 = Web3(Web3.HTTPProvider(wallet.network['rpc']))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    block_number = w3.eth.block_number
    start_block = 0
    end_block = block_number

    last_transaction = None
    wallet_address = wallet.public_key

    for block in range(end_block, start_block - 1, -1):
        block_info = w3.eth.get_block(block, True)

        for tx in reversed(block_info['transactions']):
            if wallet_address.lower() in [tx['from'].lower(), tx['to'].lower()]:
                last_transaction = tx
                break

        if last_transaction:
            break

    return last_transaction


def get_balance(wallet: Wallet) -> int:
    w3 = Web3(Web3.HTTPProvider(wallet.network['rpc']))
    balance = w3.eth.get_balance(account=wallet.public_key)
    balance = w3.from_wei(balance, 'ether')
    return balance

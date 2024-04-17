import pytest
from web3 import Web3
from functools import wraps
from typing import Iterable
from evm_wallet import Wallet
from pytest_evm.utils import validate_status, get_last_transaction, get_balance


def pytest_configure(config):
    config.addinivalue_line("markers", "tx: mark a test as a transaction test.")


def pytest_collection_modifyitems(items: Iterable[pytest.Item]):
    for item in items:
        if item.get_closest_marker("tx"):
            original_test_function = item.obj

            @validate_status
            @wraps(original_test_function)
            async def wrapped_test_function(*args, **kwargs):
                return await original_test_function(*args, **kwargs)

            item.obj = wrapped_test_function


def pytest_runtest_makereport(item: pytest.Item, call):
    if call.when == 'call':
        if call.excinfo is not None:
            pass
        else:
            if item.get_closest_marker("tx"):
                try:
                    wallet = item.funcargs['wallet']
                    wallet = Wallet(wallet.private_key, wallet.network)
                    tx = get_last_transaction(wallet)
                    last_tx_hash = tx['hash']
                    balance = get_balance(wallet)
                    costs = tx['value'] + tx['gas']*tx['gasPrice']
                    costs = Web3.from_wei(costs, 'ether')
                    print()
                    print(f'From: {wallet.public_key}')
                    print(f'Transaction: {wallet.get_explorer_url(last_tx_hash)}')
                    print(f'Costs: {costs} {wallet.network["token"]}')
                    print(f'Balance: {balance} {wallet.network["token"]}')
                    print(f'Network: {wallet.network["network"]}')
                except TimeoutError as ex:
                    print(ex)
                except Exception as ex:
                    print(f"There was an error while getting information about transaction: {ex}")

import os
import pytest
from typing import Optional
from evm_wallet import ZERO_ADDRESS
from evm_wallet.types import NetworkOrInfo
from evm_wallet import AsyncWallet, Wallet
from web3 import AsyncWeb3


@pytest.fixture(scope="session")
def make_wallet():
    def _make_wallet(network: NetworkOrInfo, private_key: Optional[str] = None, is_async: bool = True):
        if not private_key:
            private_key = os.getenv('TEST_PRIVATE_KEY')
        return AsyncWallet(private_key, network) if is_async else Wallet(private_key, network)

    return _make_wallet


@pytest.fixture(scope="session")
def eth_amount():
    amount = AsyncWeb3.to_wei(0.001, 'ether')
    return amount


@pytest.fixture(scope="session")
def zero_address():
    return ZERO_ADDRESS

# pytest-evm

[![Croco Logo](https://i.ibb.co/G5Pjt6M/logo.png)](https://t.me/crocofactory)

The testing package containing tools to test Web3-based projects

- **[Telegram channel](https://t.me/crocofactory)**
- **[Bug reports](https://github.com/blnkoff/pytest-evm/issues)**

Package's source code is made available under the [MIT License](LICENSE)

# Quick Start
There are few features simplifying your testing with pytest:
- **[Fixtures](#fixtures)**
- **[Test Reporting](#test-reporting)**
- **[Usage Example](#usage-example)**

## Fixtures

### make_wallet
This fixture simplify creating wallet instances as fixtures. Wallet instances are from `evm-wallet` package

```python
import os
import pytest
from typing import Optional
from evm_wallet.types import NetworkOrInfo
from evm_wallet import AsyncWallet, Wallet

@pytest.fixture(scope="session")
def make_wallet():
    def _make_wallet(network: NetworkOrInfo, private_key: Optional[str] = None, is_async: bool = True):
        if not private_key:
            private_key = os.getenv('TEST_PRIVATE_KEY')
        return AsyncWallet(private_key, network) if is_async else Wallet(private_key, network)

    return _make_wallet
```

You can specify whether your wallet should be of async or sync version. Instead of specifying RPC, you only have to provide
chain's name. You can also specify a custom Network, using `NetworkOrInfo`. 

```python
import pytest

@pytest.fixture
def wallet(make_wallet):
    return make_wallet('Optimism')
```

As you can see, a private key wasn't passed. This because of by-default `make_wallet` takes it from
environment variable `TEST_PRIVATE_KEY`. You can set environment variables using extra-package `python-dotenv`.

```python
# conftest.py

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def wallet(make_wallet):
    return make_wallet('Polygon')
```
 
Here is the content of .env file

```shell
# .env

TEST_PRIVATE_KEY=0x0000000000000000000000000000000000000000
```

You can install `python-dotenv` along with `pytest-evm`:

```shell
pip install pytest-evm[dotenv]
```

### zero_address
This fixture returns ZERO_ADDRESS value      

```python
import pytest
from evm_wallet import ZERO_ADDRESS

@pytest.fixture(scope="session")
def zero_address():
    return ZERO_ADDRESS
```

### eth_amount
This fixture returns 0.001 ETH in Wei, which is the most using minimal value for tests 

```python
import pytest
from web3 import AsyncWeb3

@pytest.fixture(scope="session")
def eth_amount():
    amount = AsyncWeb3.to_wei(0.001, 'ether')
    return amount
```

## Test Reporting
If your test performs one transaction, you can automatically `assert` transaction status and get useful report after test,
if it completed successfully. To do this, you need to add mark `pytest.mark.tx` to your test.

```python
import pytest

@pytest.mark.tx
@pytest.mark.asyncio
async def test_transaction(wallet, eth_amount):
    recipient = '0xe977Fa8D8AE7D3D6e28c17A868EF04bD301c583f'
    params = await wallet.build_transaction_params(eth_amount, recipient=recipient)
    return await wallet.transact(params)
```

After test, you get similar report:

![Test Report](https://i.ibb.co/n8vKXwB/Screenshot-2024-01-24-at-22-08-29.png)
         
## Usage Example
Here is example of testing with `pytest-evm`:

```python
import pytest

class TestBridge:
    @pytest.mark.tx
    @pytest.mark.asyncio
    async def test_swap(self, wallet, eth_amount, bridge, destination_network):
        return await bridge.swap(eth_amount, destination_network)

    @pytest.mark.tx
    @pytest.mark.asyncio
    async def test_swap_to_eth(self, wallet, eth_amount, bridge):
        return await bridge.swap_to_eth(eth_amount)

    @pytest.fixture
    def wallet(self, make_wallet):
        return make_wallet('Optimism')

    @pytest.fixture
    def bridge(self, wallet):
        return Bridge(wallet)

    @pytest.fixture
    def destination_network(self):
        return 'Arbitrum'
```

# Installing pytest-evm
To install the package from GitHub you can use:

```shell
pip install git+https://github.com/blnkoff/pytest-evm.git
```

To install the package from PyPi you can use:
```shell
pip install pytest-evm
```

import pytest


@pytest.mark.tx
@pytest.mark.asyncio
async def test_transaction(wallet, eth_amount):
    recipient = '0xe977Fa8D8AE7D3D6e28c17A868EF04bD301c583f'
    params = await wallet.build_transaction_params(eth_amount, recipient=recipient)
    return await wallet.transact(params)

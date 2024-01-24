from evm_wallet import AsyncWallet


def test_make_wallet(make_wallet):
    assert isinstance(make_wallet('Ethereum'), AsyncWallet)

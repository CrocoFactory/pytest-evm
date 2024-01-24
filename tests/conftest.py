import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def wallet(make_wallet):
    return make_wallet('Polygon')

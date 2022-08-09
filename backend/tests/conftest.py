import os
import sys

import pytest
from algosdk.v2client import algod, indexer
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

# To allow imports from main, app e.t.c
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

# Set Up App Configurations
app.mongodb_client = AsyncIOMotorClient("localhost:27017")
app.db = app.mongodb_client["test_db"]
app.INDEXER_CLIENT = indexer.IndexerClient(
    "AV", os.getenv("ALGO_INDEXER_URL"), {"X-API-Key": "AV"}
)
app.ALGOD_CLIENT = algod.AlgodClient(
    "AV", os.getenv("ALGO_NODE_URL"), {"X-API-Key": "AV"}
)


class TestData:
    APP_ID = "552635992"
    APPROVAL_URL = (
        "https://github.com/tinymanorg/tinyman-contracts-v1/blob/main/contracts/validator_approval.teal",
    )
    CLEAR_STATE_URL = (
        "https://github.com/tinymanorg/tinyman-contracts-v1/blob/main/contracts/validator_clear_state.teal",
    )
    TEST_REPO_LINK = (
        "https://github.com/Tee-py/flight-manager/blob/develop/core/settings.py"
    )
    TEST_GITHUB_URL = (
        "https://api.github.com/repos/Tee-py/flight-manager/contents/core/settings.py"
    )


app.TEST_DATA = TestData


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def indexer_client():
    return indexer.IndexerClient(
        "AV", os.getenv("ALGO_INDEXER_URL"), {"X-API-Key": "AV"}
    )


@pytest.fixture
def algod_client():
    return algod.AlgodClient("AV", os.getenv("ALGO_NODE_URL"), {"X-API-Key": "AV"})


@pytest.fixture
def test_data() -> TestData:
    return TestData


@pytest.fixture(scope="function")
async def async_client() -> AsyncClient:
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        yield client

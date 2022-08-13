import os
import sys

import pytest
from algosdk.v2client import algod, indexer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestData:
    TEAL_APP_ID = "552635992"
    REACH_APP_ID = "835336223"
    REACH_CONTRACT_GITHUB = (
        "https://github.com/cdirks4/rps-reach-react/blob/main/src/index.rsh"
    )
    APPROVAL_URL = "https://github.com/tinymanorg/tinyman-contracts-v1/blob/main/contracts/validator_approval.teal"
    CLEAR_STATE_URL = "https://github.com/tinymanorg/tinyman-contracts-v1/blob/main/contracts/validator_clear_state.teal"
    TEST_REPO_LINK = (
        "https://github.com/Tee-py/flight-manager/blob/develop/core/settings.py"
    )
    TEST_GITHUB_URL = (
        "https://api.github.com/repos/Tee-py/flight-manager/contents/core/settings.py"
    )


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

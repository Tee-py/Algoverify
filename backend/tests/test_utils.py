import pytest

from app.api.utils import (compose_github_url, fetch_contract_byte_code,
                           fetch_github_code, teal_to_bytes,
                           verify_teal_contract)


@pytest.mark.anyio
async def test_fetch_contract_byte_code(test_data, indexer_client) -> None:
    result = await fetch_contract_byte_code(test_data.APP_ID, indexer_client)
    assert str(result["application"]["id"]) == test_data.APP_ID
    assert "approval-program" in result["application"]["params"]
    assert "clear-state-program" in result["application"]["params"]


@pytest.mark.anyio
async def test_compose_github_url(test_data) -> None:
    url = await compose_github_url(test_data.TEST_REPO_LINK)
    assert url == test_data.TEST_GITHUB_URL


@pytest.mark.anyio
async def test_fetch_github_code(test_data) -> None:
    status, code = await fetch_github_code(test_data.TEST_GITHUB_URL)
    assert status
    assert type(code) == bytes


@pytest.mark.anyio
async def test_teal_to_bytes(algod_client) -> None:
    teal_file = open("tests/test.teal", "r")
    source = teal_file.read()
    byte_code = await teal_to_bytes(source, algod_client)
    assert type(byte_code) == str


@pytest.mark.anyio
async def test_verify_teal_contract(test_data, indexer_client, algod_client) -> None:
    status, result = await verify_teal_contract(
        test_data.APPROVAL_URL,
        test_data.CLEAR_STATE_URL,
        test_data.APP_ID,
        algod_client,
        indexer_client,
    )
    assert status
    assert "onchain-code" in result

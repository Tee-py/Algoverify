from fastapi.testclient import TestClient
import pytest
from app.api.utils import (
    fetch_contract_byte_code,
    compose_github_url,
    fetch_github_code,
    teal_to_bytes,
    verify_contract,
)


@pytest.mark.anyio
async def test_fetch_contract_byte_code(test_client: TestClient) -> None:
    result = await fetch_contract_byte_code(
        test_client.app.TEST_DATA.APP_ID, test_client.app.INDEXER_CLIENT
    )
    assert str(result["application"]["id"]) == test_client.app.TEST_DATA.APP_ID
    assert "approval-program" in result["application"]["params"]
    assert "clear-state-program" in result["application"]["params"]


@pytest.mark.anyio
async def test_compose_github_url(test_client: TestClient) -> None:
    url = await compose_github_url(test_client.app.TEST_DATA.TEST_REPO_LINK)
    assert url == test_client.app.TEST_DATA.TEST_GITHUB_URL


@pytest.mark.anyio
async def test_fetch_github_code(test_client: TestClient) -> None:
    status, code = await fetch_github_code(test_client.app.TEST_DATA.TEST_GITHUB_URL)
    assert status
    assert type(code) == bytes


@pytest.mark.anyio
async def test_teal_to_bytes(test_client: TestClient) -> None:
    teal_file = open("tests/test.teal", "r")
    source = teal_file.read()
    byte_code = await teal_to_bytes(source, test_client.app.ALGOD_CLIENT)
    assert type(byte_code) == str


@pytest.mark.anyio
async def test_verify_contract(test_client: TestClient) -> None:
    status, result = await verify_contract(
        test_client.app.TEST_DATA.APPROVAL_URL,
        test_client.app.TEST_DATA.CLEAR_STATE_URL,
        test_client.app.TEST_DATA.APP_ID,
        test_client.app.ALGOD_CLIENT,
        test_client.app.INDEXER_CLIENT,
    )
    assert status
    assert "onchain-code" in result

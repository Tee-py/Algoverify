import json

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_verify_teal_contract_endpoint(
    async_client: AsyncClient, test_data
) -> None:
    data = {
        "app_id": test_data.APP_ID,
        "name": "Tinyman AMM V1",
        "description": "Tinyman is a decentralized permissionless trading protocol",
        "approval_github_url": test_data.APPROVAL_URL,
        "clear_state_github_url": test_data.CLEAR_STATE_URL,
    }
    # result = test_client.post("/api/apps/teal/verify", data=json.dumps(data))
    result = await async_client.post("/api/apps/teal/verify", data=json.dumps(data))
    assert result.status_code == 200
    assert result.json()["status"]


@pytest.mark.anyio
async def test_app_details_endpoint(async_client: AsyncClient, test_data) -> None:
    # result = test_client.get(f"/api/apps/{test_client.app.TEST_DATA.APP_ID}")
    result = await async_client.get(f"/api/apps/{test_data.APP_ID}")
    # print(result.json())
    assert result.status_code == 200

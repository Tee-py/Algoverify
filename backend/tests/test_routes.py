import json
from fastapi.testclient import TestClient


def test_verify_contract_endpoint(test_client: TestClient) -> None:
    data = {
        "app_id": test_client.app.TEST_DATA.APP_ID,
        "name": "Tinyman AMM V1",
        "description": "Tinyman is a decentralized permissionless trading protocol",
        "approval_github_url": test_client.app.TEST_DATA.APPROVAL_URL,
        "clear_state_github_url": test_client.app.TEST_DATA.CLEAR_STATE_URL,
    }
    result = test_client.post("/api/verify-app", data=json.dumps(data))
    assert result.status_code == 200
    assert result.json()["status"]

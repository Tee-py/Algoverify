import requests

BASE_URL = "http://127.0.0.1:8000/api"


def test_verify_teal_contract_endpoint(test_data) -> None:
    data = {
        "app_id": test_data.TEAL_APP_ID,
        "name": "Tinyman AMM V1",
        "description": "Tinyman is a decentralized permissionless trading protocol",
        "approval_github_url": test_data.APPROVAL_URL,
        "clear_state_github_url": test_data.CLEAR_STATE_URL,
    }
    result = requests.post(url=f"{BASE_URL}/apps/teal/verify/", json=data)
    assert result.status_code == 200
    assert result.json()["status"]


def test_verify_reach_contract_endpoint(test_data) -> None:
    data = {
        "app_id": test_data.REACH_APP_ID,
        "name": "Test reach",
        "description": "Test reach",
        "github_url": test_data.REACH_CONTRACT_GITHUB,
    }
    result = requests.post(url=f"{BASE_URL}/apps/reach/verify/", json=data)
    assert result.status_code == 200
    assert result.json()["status"]


def test_app_list_endpoint() -> None:
    result = requests.get(f"{BASE_URL}/apps/?limit=10&skip=0")
    assert result.status_code == 200


def test_app_details_endpoint(test_data) -> None:
    result = requests.get(f"{BASE_URL}/apps/{test_data.TEAL_APP_ID}")
    assert result.status_code == 200
    assert result.json()["app"]["app_id"] == test_data.TEAL_APP_ID

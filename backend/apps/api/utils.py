import base64
from typing import Dict, Tuple, Union

import requests
from algosdk.v2client import algod, indexer


async def fetch_contract_byte_code(app_id: str, indexer: indexer.IndexerClient) -> Dict:
    result = indexer.applications(app_id)
    return result["application"]["params"]


async def compose_github_url(link: str) -> str:
    splitted_url = link.split("/")
    user_name = splitted_url[3]
    repo = splitted_url[4]
    path = "/".join(splitted_url[7:])
    return f"https://api.github.com/repos/{user_name}/{repo}/contents/{path}"


async def fetch_github_code(url: str) -> Tuple[bool, Union[Dict, bytes]]:
    response = requests.get(url)
    if response.status_code != 200:
        return False, response.json()
    content_to_bytes = bytes(response.json()["content"], "utf-8")
    decoded = base64.decodebytes(content_to_bytes)
    return True, decoded


async def teal_to_bytes(source: str, algod_client: algod.AlgodClient) -> str:
    return algod_client.compile(source)["result"]


async def verify_contract(
    approval_link: str,
    clear_state_link: str,
    app_id: str,
    algod_client: algod.AlgodClient,
    indexer_client: indexer.IndexerClient,
) -> Tuple[bool, Union[str, dict]]:
    approval_url = await compose_github_url(approval_link)
    clear_state_url = await compose_github_url(clear_state_link)
    status1, approval_source = await fetch_github_code(approval_url)
    status2, clear_state_source = await fetch_github_code(clear_state_url)
    if status1 and status2:
        onchain_bytes_codes = await fetch_contract_byte_code(app_id, indexer_client)
        approval_byte_code = await teal_to_bytes(
            approval_source.decode("utf-8"), algod_client
        )
        clear_state_byte_code = await teal_to_bytes(
            clear_state_source.decode("utf-8"), algod_client
        )
        if approval_byte_code != onchain_bytes_codes["approval-program"]:
            return False, "Approval code does not match what is stored on chain."
        if clear_state_byte_code != onchain_bytes_codes["clear-state-program"]:
            return False, "Clear state code does not match what is stored on chain"
        result = {
            "onchain-code": onchain_bytes_codes
        }
        return True, result
    return False, "Verification Failed"

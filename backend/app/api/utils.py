import base64
import os
import secrets
import subprocess
from typing import Dict, Tuple, Union

import requests
from algosdk.v2client import algod, indexer


async def fetch_contract_byte_code(
    app_id: str,
    indexer: indexer.IndexerClient,
) -> Dict:
    return indexer.applications(app_id)


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


async def compile_reach_contract(github_url: str) -> Tuple[str, str]:

    url = await compose_github_url(github_url)
    _, code = await fetch_github_code(url)
    f_name = f"{secrets.token_hex()}.rsh"
    with open(f_name, "w") as file:
        file.write(code.decode("utf-8"))
    p = subprocess.call(["./reach", "compile", f_name])
    if p != 0:
        os.remove(f_name)
        raise Exception("Failed to compile reach code")
    mjs_path = "build/" + f_name.replace(".rsh", ".main.mjs")
    approval = None
    clear = None
    with open(mjs_path, "r") as file:
        for line in file:
            if approval is not None and clear is not None:
                break
            if "appApproval" in line:
                approval = line.split(": ")[1].replace("`", "").replace(",\n", "")
            if "appClear" in line:
                clear = line.split(": ")[1].replace("`", "").replace(",\n", "")
    os.remove(mjs_path)
    os.remove(f_name)
    return approval, clear


# Todo: Refactor This To Allow Algorand and Reach Contract Verification
async def verify_teal_contract(
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
        if (
            approval_byte_code
            != onchain_bytes_codes["application"]["params"]["approval-program"]
        ):
            return False, "Approval code does not match what is stored on chain."
        if (
            clear_state_byte_code
            != onchain_bytes_codes["application"]["params"]["clear-state-program"]
        ):
            return False, "Clear state code does not match what is stored on chain"
        result = {"onchain-code": onchain_bytes_codes["application"]["params"]}
        return True, result
    return False, "Verification Failed"


async def verify_reach_contract(
    github_url: str, app_id: str, indexer_client: indexer.IndexerClient
) -> Tuple[bool, Union[str, dict]]:
    approval_byte_code, clear_state_byte_code = await compile_reach_contract(github_url)
    onchain_bytes_codes = await fetch_contract_byte_code(app_id, indexer_client)
    if (
        approval_byte_code
        != onchain_bytes_codes["application"]["params"]["approval-program"]
    ):
        return False, "Approval code does not match what is stored on chain."
    if (
        clear_state_byte_code
        != onchain_bytes_codes["application"]["params"]["clear-state-program"]
    ):
        return False, "Clear state code does not match what is stored on chain"
    result = {"onchain-code": onchain_bytes_codes["application"]["params"]}
    return True, result

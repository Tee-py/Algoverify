from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from utils import verify_contract

from .models import VerifyAppModel

router = APIRouter()


@router.post("/", response_description="Verify algorand smart contract.")
async def verify_app(request: Request, app: VerifyAppModel):
    success, result = await verify_contract(
        app.approval_github_url,
        app.clear_state_github_url,
        app.app_id,
        request.app.ALGOD_CLIENT,
        request.app.INDEXER_CLIENT,
    )
    if success:
        # create app in the mongo database
        app_dict = jsonable_encoder(app)
        await request.app.mongodb["apps"].insert_one(
            {
                **app_dict,
                "onchain_code": result["on-chain-code"],
                "verified": True,
                "verified_at": datetime.now(),
            }
        )
        return JSONResponse(status_code=200, content="Verification successfull")
    return JSONResponse(status_code=400, content=result)

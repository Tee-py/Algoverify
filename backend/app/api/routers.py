from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.helpers import format_app
from app.api.utils import verify_reach_contract, verify_teal_contract

from .models import VerifyReachAppModel, VerifyTealAppModel

router = APIRouter()


@router.post("/apps/teal/verify/", response_description="Verify teal smart contract.")
async def verify_teal_app(request: Request, app: VerifyTealAppModel) -> JSONResponse:
    app_count = await request.app.db["apps"].count_documents({"app_id": app.app_id})
    if app_count > 0:
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "App already verified"},
        )
    try:
        success, result = await verify_teal_contract(
            app.approval_github_url,
            app.clear_state_github_url,
            app.app_id,
            request.app.ALGOD_CLIENT,
            request.app.INDEXER_CLIENT,
        )
    except Exception as e:
        raise HTTPException(500, str(e))
    if success:
        await request.app.db["apps"].insert_one(
            {
                **app,
                "onchain_code": result["onchain-code"],
                "type": "teal",
                "verified": True,
                "verified_at": datetime.now(),
            }
        )
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "Verification successfull"},
        )
    raise HTTPException(400, result)


@router.post(
    "/apps/reach/verify", response_description="Verify algorand reach smart contract."
)
async def verify_reach_app(request: Request, app: VerifyReachAppModel) -> JSONResponse:
    app_count = await request.app.db["apps"].count_documents({"app_id": app.app_id})
    if app_count > 0:
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "App already verified"},
        )
    try:
        success, result = await verify_reach_contract(
            app.github_url,
            app.app_id,
            request.app.INDEXER_CLIENT,
        )
    except Exception as e:
        raise HTTPException(500, str(e))
    if success:
        app_dict = jsonable_encoder(app)
        await request.app.db["apps"].insert_one(
            {
                **app_dict,
                "onchain_code": result["onchain-code"],
                "type": "reach",
                "verified": True,
                "verified_at": datetime.now(),
            }
        )
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "Verification successfull"},
        )
    raise HTTPException(400, result)


@router.get("/apps/{app_id}")
async def app_details(request: Request, app_id: str):
    app = await request.app.db["apps"].find_one({"app_id": app_id})
    if app is not None:
        format_app(app)
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "App verified", "app": app},
        )
    return HTTPException(404, "App not found")


@router.get("/apps")
async def fetch_apps(request: Request, skip: int = 0, limit: int = 10):
    result = []
    async for app in request.app.db["apps"].find().limit(limit).skip(skip):
        format_app(app)
        result.append(app)
    return JSONResponse(status_code=200, content={"apps": result})

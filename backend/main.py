from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from algosdk.v2client import indexer, algod
from github import Github

from apps.api.routers import router as api_router

app = FastAPI()


@app.on_event("startup")
async def app_setup():
    app.mongodb_client = AsyncIOMotorClient(settings.DATABASE_URI)
    app.db = app.mongodb_client[settings.DB_NAME]
    app.INDEXER_CLIENT = indexer.IndexerClient(
        "AV", settings.ALGO_INDEXER_URL, {"X-API-Key": "AV"}
    )
    app.ALGOD_CLIENT = algod.AlgodClient(
        "AV", settings.ALGO_NODE_URL, {"X-API-Key": "AV"}
    )
    app.GITHUB_CLIENT = Github()


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(api_router, tags=["api"], prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )

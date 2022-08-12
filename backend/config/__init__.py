import dotenv
import os
from pydantic import BaseSettings

dotenv.load_dotenv()

class AppSettings(BaseSettings):
    APP_NAME = "AlgoVerify API"
    DEBUG_MODE: bool = (os.getenv("DEBUG") == "True")
    ALGO_INDEXER_URL: str = os.getenv("ALGO_INDEXER_URL")
    ALGO_NODE_URL: str = os.getenv("ALGO_NODE_URL")
    DATABASE_URI: str = os.getenv("DATABASE_URI")
    DB_NAME: str = os.getenv("DB_NAME")
    HOST: str = os.getenv("HOST")
    PORT: int = os.getenv("PORT")

settings = AppSettings()

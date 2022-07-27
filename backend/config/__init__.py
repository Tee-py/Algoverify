import os

import dotenv
from pydantic import BaseSettings

dotenv.load_dotenv()


class AppSettings(BaseSettings):

    APP_NAME = "AlgoVerify API"
    DEBUG_MODE = os.getenv("DEBUG", "True") == "True"
    ALGO_INDEXER_URL = os.getenv("ALGO_INDEXER_URL")
    ALGO_NODE_URL = os.getenv("ALGO_NODE_URL")
    DATABASE_URI = os.getenv("DATABASE_URI")
    DB_NAME = os.getenv("DB_NAME")
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))


settings = AppSettings()

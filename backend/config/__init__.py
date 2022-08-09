import dotenv
from pydantic import BaseSettings

dotenv.load_dotenv()


class AppSettings(BaseSettings):
    APP_NAME = "AlgoVerify API"
    DEBUG_MODE: bool = True
    ALGO_INDEXER_URL: str
    ALGO_NODE_URL: str
    DATABASE_URI: str
    DB_NAME: str
    HOST: str
    PORT: int

    class Config:
        env_file = ".env"


settings = AppSettings()

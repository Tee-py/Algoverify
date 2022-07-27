from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field, Extra


class App(BaseModel, Extra.ignore):

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    app_id: int
    name: str
    approval_github_url: str
    clear_state_github_url: str
    onchain_code: dict
    verified: bool = True
    verified_at: datetime

class VerifyApp(BaseModel, Extra.ignore):

    app_id: int
    approval_github_url: str
    clear_state_github_url: str

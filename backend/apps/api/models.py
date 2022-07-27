from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field, Extra


class VerifyAppModel(BaseModel, Extra.ignore):

    app_id: int
    name: str
    description: str
    approval_github_url: str
    clear_state_github_url: str

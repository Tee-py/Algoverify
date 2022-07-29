from pydantic import BaseModel, Extra


class VerifyAppModel(BaseModel, extra=Extra.ignore):
    app_id: str
    name: str
    description: str
    approval_github_url: str
    clear_state_github_url: str

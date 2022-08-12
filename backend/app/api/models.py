from pydantic import BaseModel, Extra


class VerifyTealAppModel(BaseModel, extra=Extra.ignore):
    app_id: str
    name: str
    description: str
    approval_github_url: str
    clear_state_github_url: str


class VerifyReachAppModel(BaseModel, extra=Extra.ignore):
    app_id: str
    name: str
    description: str
    github_url: str

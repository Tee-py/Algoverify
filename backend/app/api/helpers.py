from typing import Dict


def format_app(app: Dict) -> Dict:
    app["verified_at"] = app["verified_at"].isoformat()
    del app["_id"]
    return app

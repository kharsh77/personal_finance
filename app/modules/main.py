from flask import Blueprint
from flask import current_app

blueprint=Blueprint('main', __name__, url_prefix="/")

@blueprint.route("health", methods=["GET"])
def health():
    x = current_app.config.get("MY_ENV_VAR")
    return "success"+x

from flask import Blueprint
from flask import current_app, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from datetime import datetime, timedelta
from app.database import db
import jwt
from functools import wraps

blueprint=Blueprint('main', __name__, url_prefix="/")

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        
        if not token:
            return jsonify({"message": "A valid access token is missing"})
        try:
            data=jwt.decode(token, current_app.config.get('JWT_SECRET'), algorithms=["HS256"])
            user=User.query.filter_by(id=data['id']).first()
        except Exception as ex:
            print(ex)
            print("Invalid token")
            return jsonify({"message":"token is invalid"})
        return f(user, *args, **kwargs)
    return decorator


@blueprint.route("/health", methods=["GET"])
def health():
    return "success"

@blueprint.route("/register", methods=["POST"])
def register():
    data=request.get_json()
    hashed_password=generate_password_hash(data["password"])
    new_user=User(
        username=data["username"],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id})

@blueprint.route("/login", methods=["POST"])
def login_user():
    auth=request.get_json()
    print(auth)
    if not auth or not auth["username"] or not auth["password"]:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})  
    user=User.query.filter_by(username=auth["username"]).first()
    if check_password_hash(user.password, auth["password"]):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.now() + timedelta(hours=12)}, current_app.config.get('JWT_SECRET'), "HS256")
        return jsonify({"token": token})
    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@blueprint.route("/")



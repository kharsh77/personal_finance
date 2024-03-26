from flask import Blueprint, g
from flask import current_app, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models.transaction import Transaction, TransactionType
from datetime import datetime, timedelta
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
            return make_response('A valid access token is missing', 401)  
        try:
            data=jwt.decode(token, current_app.config.get('JWT_SECRET'), algorithms=["HS256"])
            user=User.query.filter_by(id=data['id']).first()
            g.user=user
        except Exception as ex:
            print(ex)
            print("Invalid token")
            return make_response('Invalid token', 401)  
        return f(user, *args, **kwargs)
    return decorator


@blueprint.route("/health", methods=["GET"])
def health():
    return "success"

@blueprint.route("/register", methods=["POST"])
def register():
    try:
        data=request.get_json()

        if not data or "username" not in data.keys() or "password" not in data.keys():
            return make_response('username and password are mandatory', 400)  
        hashed_password=generate_password_hash(data["password"])
        new_user = User.register_user(data["username"], hashed_password)
        return jsonify({"id": new_user.id})
    except Exception as ex:
        print(ex)
        return ('Internal Server Error', 500)  

@blueprint.route("/login", methods=["POST"])
def login_user():
    try:
        auth=request.get_json()
        if not auth or "username" not in auth.keys() or "password" not in auth.keys():
            return make_response('username and password are mandatory', 400)    
        user=User.get_by_username(auth["username"])
        if check_password_hash(user.password, auth["password"]):
            token = jwt.encode({'id' : user.id, 'exp' : datetime.now() + timedelta(hours=12)}, current_app.config.get('JWT_SECRET'), "HS256")
            return jsonify({"token": token})
        return make_response('Login failed due to incorrect password or username',  401)
    except Exception as ex:
        print(ex)
        return ('Internal Server Error', 500)

@blueprint.route("/transaction", methods=["POST"])
@token_required
def add_transactions(*args, **kwargs):
    try:
        data = request.get_json()
        type=data["type"] if "type" in data.keys() else None
        amount=data["amount"] if "amount" in data.keys() else None
        description=data["description"] if "description" in data.keys() else ""

        if not type or not amount:
            return make_response('Type and amount are mandatory', 400)
        
        if type not in [TransactionType.income.name, TransactionType.expense.name]:
            return make_response('Type can be income or expense', 400)
        if not isinstance(amount, float):
            return make_response('amount is mandatory and can be only of float datatype', 400) 
        

        t = Transaction(g.user.id, type, amount, description)
        is_success = t.add_transaction()
        if is_success:
            return jsonify({"message": "success"})
        return make_response('could not add transaction',  400, {'error': '"Invalid request params"'})
    except Exception as ex:
        print(ex)
        return ('Internal Server Error', 500)

@blueprint.route("/analytics", methods=["GET"])
@token_required
def get_analytics(*args, **kwargs):
    try:
        time_period = request.args.get('period')
        if time_period not in ['last_month', 'current_month']:
            return make_response('Invalid time period. Supported period: last_month, current_month',  401)
        data = Transaction.get_analytics(g.user.id, time_period)

        return jsonify(data)
    except Exception as ex:
        print(ex)
        return ('Internal Server Error', 500)

    

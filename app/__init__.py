from flask import Flask
from app.modules import main
from app.config import Configs
from flask_migrate import Migrate
from app.database import db

def create_app():
    app=Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="MY_SECRET_KEY"
    )

    app.config.from_object(Configs)

    db.init_app(app)
    from app.models.user import User
    migrate = Migrate(app, db)
    
    app.register_blueprint(main.blueprint)
    return app

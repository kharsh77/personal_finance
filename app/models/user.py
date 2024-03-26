from app.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True, nullable=False)    
    created_at = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(), nullable=False)    

    def __init__(self, username, password):
        self.id=None
        self.username = username        
        self.created_at = datetime.now()  
        self.password = password      
    
    def register_user_if_not_exist(self):        
        db_user = User.get_by_username(self.username)
        if not db_user:
            db.session.add(self)            
            db.session.commit()
            return self
        return db_user
    
    def get_by_username(username):        
        db_user = User.query.filter(User.username == username).first()
        return db_user
    
    def register_user(username, password):
        user_obj=User(username, password)
        return user_obj.register_user_if_not_exist()

    def __repr__(self):
        return f"<User {self.username}>"
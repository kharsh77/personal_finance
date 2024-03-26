from app.database import db
from datetime import datetime
import enum
from sqlalchemy import ForeignKeyConstraint
from app.models.user import User
import calendar

class TransactionType(enum.Enum):
    income=1
    expense=0

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(TransactionType))
    amount = db.Column(db.Float() , default=0.0)    
    description = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    __table_args__ = (        
        ForeignKeyConstraint([user_id], [User.id], ondelete='NO ACTION'),        
    )


    def __init__(self, user_id, type, amount, description):
        self.user_id = user_id
        self.type = type
        self.amount = amount
        self.description = description      
        self.created_at = datetime.now()  

    
    def add_transaction(self):
        user = User.query.filter(User.id==self.user_id).first()
        if not user:
            return False 
        db.session.add(self)
        db.session.commit()
        return True
    
    def get_analytics(user_id, time_period):
        
        time_from,time_to = None, None
        time= datetime.now()
        month = time.month
        year = time.year

        if time_period=="current_month":
            time_from = datetime.strptime(f'01/{month}/{int(str(year)[-2:])} 00:00:00', '%d/%m/%y %H:%M:%S')
            time_to =time
        elif time_period=="last_month":
            if month==1:
                month=12
                year-=1
            else:
                month-=1
            last_date = calendar.monthrange(year, month)[-1]
            time_from = datetime.strptime(f"01/{month}/{int(str(year)[-2:])} 00:00:00", "%d/%m/%y %H:%M:%S")
            time_to = datetime.strptime(f'29/2/24 23:59:59', '%d/%m/%y %H:%M:%S')

        all_trans=Transaction.query.filter(Transaction.created_at>=time_from, Transaction.created_at<=time_to).all()
        tot_income=0
        tot_expense=0
        net_balance=0
        for t in all_trans:
            if t.type==TransactionType.expense:
                tot_expense+=t.amount
            else:
                tot_income+=t.amount
        net_balance = tot_income-tot_expense
        return {
            "total_income": tot_income,
            "total_expense": tot_expense,
            "net_balance": net_balance
        }


    def __repr__(self):
        return f"<Transaction {self.id} {self.type} {self.amount}>"
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mysqldb import MySQL
from flask_file import app
import os
from sqlalchemy import DateTime
from sqlalchemy.sql import func
import enum



load_dotenv()

mysql=MySQL()
mysql.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db=SQLAlchemy(app=app)
migrate=Migrate(app=app, db=db)

class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email_address=db.Column(db.String(200), unique=True)
    account_number=db.Column(db.String(14))
    public_id=db.Column(db.String(200))
    password=db.Column(db.String(200))
    account_balance=db.Column(db.Float)
    created_at=db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at=db.Column(DateTime(timezone=True), server_default=func.now())


    def __repr__(self):
        return f'User("""\
        "{self.name}", "{self.email_address}", "{self.account_number}", "{self.public_id}", "{self.password}", "{self.account_balance}"\
        """)'
    

class Recipient(db.Model):
    __tablename__ = "recipient"
    id = db.Column(db.Integer, primary_key=True)
    recipient_name = db.Column(db.String(100))
    recipient_public_id=db.Column(db.String(200))
    password=db.Column(db.String(200))
    recipient_account_number = db.Column(db.String(14), unique=True)
    recipient_account_balance = db.Column(db.Float)
    created_at=db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at=db.Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'Recipient("""\
        "{self.recipient_name}", "{self.customer_public_id}", "{self.password}", "{self.recipient_account_number}", "{self.recipient_account_balance}"\
        """)'



class TransactionTypeEnum(enum.Enum):
    deposit="deposit"
    withdraw="withdraw"
    transfer="transfer"


class Transaction(db.Model):
    __tablename__="transaction"
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id", name="FK_transaction_user_id"))
    recipient_id=db.Column(db.Integer, db.ForeignKey("recipient.id", name="FK_transaction_customer_id"))
    transaction_type=db.Column(db.Enum(TransactionTypeEnum), nullable=False)
    amount=db.Column(db.Float)
    sender_name=db.Column(db.String(14))
    recipient_account_number=db.Column(db.String(14))
    created_at=db.Column(DateTime(timezone=True), server_default=func.now())
    user=db.relationship("User", backref=db.backref("transaction", lazy=True))
    recipient=db.relationship("Recipient", backref=db.backref("transaction", lazy=True))
    

    def __repr__(self):
        return f'Transaction("""\
        "{self.amount}", "{self.user_id}", "{self.recipient_account_number}", "{self.sender_name}"\
        """)'
    

    app.app_context().push()



  
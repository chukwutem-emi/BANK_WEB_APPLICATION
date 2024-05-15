
from flask_file import app
from model_file import Transaction, User, db, TransactionTypeEnum, Recipient
import os
from dotenv import load_dotenv
from flask import request, make_response, abort
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import datetime
from sqlalchemy import text as t
import jwt
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError



Transaction()
User()
Recipient()

load_dotenv()

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "A-access-token" in request.headers:
            token=request.headers["A-access-token"]
            
        if not token:
            return({"message": "token is missing!. login to get an access token"}), 401
        try:
            data=jwt.decode(jwt=token, key=app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user=User.query.filter_by(public_id=data["public_id"]).first()
        except Exception as e:
            print("Error", e)
            return({"message": "invalid token!"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated


@app.route("/register", methods=["POST"])
def create_bank_account():
    try:
        data=request.get_json()
        if not data:
            abort(400, discription=f"Invalid input")
        required_fields=["name", "password", "email_address", "account_number", "account_balance"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Missing required feild: {field}")
        hashed_password=generate_password_hash(password=data["password"], method="pbkdf2:sha256")
        password=hashed_password
        name=str(data["name"])
        email_address=str(data["email_address"])
        account_number=str(data["account_number"])
        public_id=str(uuid.uuid4())
        account_balance=float(data["account_balance"])
        with db.engine.connect() as connection:
                create_a_bank_account=t("INSERT INTO user(password, name, email_address, account_number, public_id, account_balance) VALUES(:password, :name, :email_address, :account_number, :public_id, :account_balance)")
                connection.execute(create_a_bank_account, {"password":password, "name":name, "email_address":email_address, "account_number":account_number, "public_id":public_id, "account_balance":account_balance})
                connection.commit()
                return({"message": "Account created successfully!"}), 201
    except KeyError as k:
        abort(400, description=f"Missing data: {str(k)}")
    except ValueError as v:
        abort(400, description=f"Invalid data: {str(v)}")
    except SQLAlchemyError as s:
        abort(400, description=f"Database Error: {str(s)}")
    except Exception as e:
        abort(400, description=f"An Unexpected error as occured: {str(e)}")



@app.route("/recipient", methods=["POST"])
def sign_up():
    try:
        data=request.get_json()
        if not data:
            abort(400, discription=f"Invalid input")
        required_fields=["recipient_name", "password", "recipient_account_number", "recipient_account_balance"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Missing required feild: {field}")
        hashed_password=generate_password_hash(password=data["password"], method="pbkdf2:sha256")
        recipient_name=str(data["recipient_name"])
        password=hashed_password
        recipient_public_id=str(uuid.uuid4())
        recipient_account_number=str(data["recipient_account_number"])
        recipient_account_balance=float(data["recipient_account_balance"])
        with db.engine.connect() as connection:
            create_an_account=t("INSERT INTO recipient(recipient_name, password, recipient_public_id, recipient_account_number, recipient_account_balance) VALUES(:recipient_name, :password, :recipient_public_id, :recipient_account_number, :recipient_account_balance)")
            connection.execute(create_an_account, {"recipient_name":recipient_name, "password":password, "recipient_public_id":recipient_public_id, "recipient_account_number":recipient_account_number, "recipient_account_balance":recipient_account_balance})
            connection.commit()
            return({"message": "account created successfully!"}), 201
    except KeyError as k:
        abort(400, description=f"Missing data: {str(k)}")
    except ValueError as v:
        abort(400, description=f"Invalid data: {str(v)}")
    except SQLAlchemyError as s:
        abort(400, description=f"Database Error: {str(s)}")
    except Exception as e:
        abort(400, description=f"An Unexpected error as occured: {str(e)}")


            


@app.route("/recipient/<id>", methods=["DELETE"])
def delete_customer_account(id):
    with db.engine.connect() as connection:
        user_account=t("DELETE FROM recipient WHERE id=:id")
        recipient=connection.execute(user_account, {"id":id})
        if not recipient:
            return({"message": "you can't perform this operation!"}), 404
        connection.commit()
        return({"message": "recipient account deleted!"}), 200
    


@app.route("/user/<public_id>", methods=["GET"])
@token_required
def check_account_details(current_user, public_id):
    if not current_user:
        return({"message": "You can't perform this opertation!"})
    with db.engine.connect() as connection:
        account_details=t("SELECT * FROM user WHERE public_id=:public_id")
        user_data=connection.execute(account_details, {"public_id":public_id})
        user=user_data.first()
        if not user:
            return({"message": "You can't perform this operation!"}), 404
        return({"user":user}), 200
    
  
@app.route("/user", methods=["GET"])
@token_required
def get_all_bank_account_users(current_user):
    if not current_user:
        return({"message": "You can't perform this operation!"})
    with db.engine.connect() as connection:
        all_bank_user=t("SELECT * FROM user")
        userData=connection.execute(all_bank_user)
        output=[]
        for user in userData:
            user_data={}
            user_data["name"] = user.name
            user_data["email_address"] = user.email_address
            user_data["password"] = user.password
            user_data["public_id"] = user.public_id
            user_data["account_number"] = user.account_number
            user_data["account_balance"] = user.account_balance
            output.append(user_data)
        return({"user":output}), 200

   
@app.route("/user/<public_id>", methods=["PUT"])
@token_required
def update_bank_user_account_details(public_id, current_user):
    if not current_user:
        return({"message": "You can't perform this operation!"}), 401
    data=request.get_json()
    name=str(data["name"])
    email_address=str(data["email_address"])
    with db.engine.connect() as connection:
        a_bank_user_account_details=t("UPDATE user SET name=:name, email_address=:email_address WHERE public_id=:public_id")
        user=connection.execute(a_bank_user_account_details, {"name":name, "email_address":email_address, "public_id":public_id})
        if not user:
            return({"message":"you can't perform this operation!"}), 404
        connection.commit()
        return({"message":"A bank user account update successfully!"}), 200
    

@app.route("/user/<public_id>", methods=["DELETE"])
@token_required
def delete_user_account(current_user, public_id):
    if not current_user:
        return({"message": "You can't perform this operation!"}), 401
    with db.engine.connect() as connection:
        user_account=t("DELETE FROM user WHERE public_id=:public_id")
        user=connection.execute(user_account, {"public_id":public_id})
        if not user:
            return({"message": "you can't perform this operation!"}), 404
        connection.commit()
        return({"message": "user account deleted!"}), 200
    
@app.route("/login")
def login():
    auth=request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("could not verify!", {"WWW-Authenticate":"basic realm=login required"}), 401
    user=User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response("verification error!", {"WWW-Authenticate":"basic realm=login required"}), 401
    
    if check_password_hash(user.password, auth.password):
        token=jwt.encode({"public_id":user.public_id, "exp":datetime.datetime.now(datetime.UTC)+datetime.timedelta(minutes=60)}, app.config["SECRET_KEY"])
        return({"Token":token})
        
    return make_response("error in verification!", {"WWW-Authenticate":"basic realm=login required"}), 401
    


@app.route("/deposit", methods=["POST"])
@token_required
def deposit_money(current_user):
    try:
        if not current_user:
            return({"message": "You can't perform this operation!"}), 401
        data=request.get_json()
        if not data:
            abort(400, discription="Invalid input")
        required_fields=["name", "amount"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Missing required field: {field}")
        name=str(data["name"])
        amount=float(data["amount"])
        # sender_name=str(data["sender_account_number"])
        if not name or not amount:
            return({"message": "Name, account_number and amount are required!"}), 400
        with db.engine.connect() as connection:
                fetching_account_user_details=t("SELECT * FROM user WHERE name=:name")
                user=connection.execute(fetching_account_user_details, {"name":name}).fetchone()
                if not user:
                    return({"message": "Bank account user not found!"}), 404
                account_balance=float(user[6])
                new_account_balance=account_balance + amount
                updating_account_user=t("UPDATE user SET account_balance=:new_account_balance WHERE name=:name")
                connection.execute(updating_account_user, {"new_account_balance":new_account_balance, "name":name})
                money_deposit=t("INSERT INTO transaction(amount, user_id, transaction_type, sender_name) VALUES(:amount, :user_id, :transaction_type, :sender_name)")
                connection.execute(money_deposit, {"amount":amount, "user_id":user[0], "transaction_type":TransactionTypeEnum.deposit.value, "sender_name":user[1]})
                connection.commit()
                return f'deposit of {amount} to {name} was successful!', 200
    except KeyError as k:
        abort(400, discription=f"Missing data: {str(k)}")
    except ValueError as V:
        abort(400, discription=f"Invalid data: {str(V)}")
    except SQLAlchemyError as s:
        abort(400, discription=f"Database error: {str(s)}")
    except Exception as e:
        abort(400, discription=f"An error occured during your transaction: {str(e)}")




@app.route("/withdraw", methods=["POST"])
@token_required
def withdraw_money(current_user):
    if not current_user:
        return({"message": "You can't perform this operation!"}), 401
    data=request.get_json()
    name=str(data["name"])
    amount=float(data["amount"])
    if not name or not amount:
        return({"message": "Name, account_number and amount are required!"}), 400
    with db.engine.connect() as connection:
            fetching_account_user_details=t("SELECT * FROM user WHERE name=:name")
            user=connection.execute(fetching_account_user_details, {"name":name}).fetchone()
            if not user:
                return({"message": "Bank account user not found!"}), 404
            account_balance=float(user[6])
            new_account_balance=account_balance - amount
            if amount > account_balance:
                return({"message":"Insufficient fund!"}), 400
            updating_account_user=t("UPDATE user SET account_balance=:new_account_balance WHERE name=:name")
            connection.execute(updating_account_user, {"new_account_balance":new_account_balance, "name":name})
            money_withdrawer=t("INSERT INTO transaction(amount, user_id, transaction_type) VALUES(:amount, :user_id, :transaction_type)")
            connection.execute(money_withdrawer, {"amount":amount, "user_id":user[0], "transaction_type":TransactionTypeEnum.withdraw.value})
            connection.commit()
            return f'Withdraw of {amount} by {name} was successful!', 200 



@app.route("/transfer", methods=["POST"])
@token_required
def transfer_money(current_user):
    if not current_user:
        return({"message": "You are not authorize perform this operation!"}), 401
    data=request.get_json()
    amount=float(data["amount"])
    name=str(data["name"])
    recipient_account_number=str(data["recipient_account_number"])
    if not name or not amount:
        return({"message": "Name, account_number and amount are required!"}), 400
    with db.engine.connect() as connection:
            fetching_account_user_details=t("SELECT * FROM user WHERE name=:name")
            user=connection.execute(fetching_account_user_details, {"name":name}).fetchone()
            if not user:
                return({"message": "Bank account user not found!"}), 404
            account_balance=float(user[6])
            new_account_balance=account_balance - amount
            if amount > account_balance:
                return({"message":"Insufficient fund!"}), 400
            updating_account_user=t("UPDATE user SET account_balance=:new_account_balance WHERE name=:name")
            connection.execute(updating_account_user, {"new_account_balance":new_account_balance, "name":name})
            fetching_recipient=t("SELECT * FROM recipient WHERE recipient_account_number=:recipient_account_number")
            recipient=connection.execute(fetching_recipient, {"recipient_account_number":recipient_account_number}).fetchone()
            if not recipient:
                return({"message": "Recipient not found!"}), 404
            recipient_account_balance=float(recipient[5])
            new_recipient_account_balance=recipient_account_balance + amount
            updating_recipient_account=t("UPDATE recipient SET recipient_account_balance=:new_recipient_account_balance WHERE recipient_account_number=:recipient_account_number")
            connection.execute(updating_recipient_account, {"new_recipient_account_balance":new_recipient_account_balance, "recipient_account_number":recipient_account_number})
            money_transfer=t("INSERT INTO transaction(amount, user_id, transaction_type, sender_name, recipient_account_number, recipient_id) VALUES(:amount, :user_id, :transaction_type, :sender_name, :recipient_account_number, :recipient_id)")
            connection.execute(money_transfer, {"amount":amount, "user_id":user[0], "transaction_type":TransactionTypeEnum.transfer.value, "sender_name":user[1], "recipient_account_number":recipient_account_number, "recipient_id":recipient[0]})
            connection.commit()
            return f'Transfer of {amount} to {recipient_account_number} was successful!', 200 




if __name__=="__main__":
    port=int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True, )
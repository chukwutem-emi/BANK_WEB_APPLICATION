from flask_cors import CORS
from flask_file import app
from model_file import Transaction, User, db, TransactionTypeEnum
import os
from dotenv import load_dotenv
from flask import request, abort
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import datetime
from sqlalchemy import text as t
import jwt
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()

CORS(app)
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
        
        return f(current_user=current_user, *args, **kwargs)
    return decorated






@app.route("/register", methods=["POST"])
def create_bank_account():
    try:
        User()
        data=request.get_json()
        if not data:
            abort(400, description=f"Invalid input")
        required_fields=["username", "password", "email_address", "account_number"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Missing required field: {field}")
        hashed_password=generate_password_hash(password=data["password"], method="pbkdf2:sha256")
        password=hashed_password
        username=str(data["username"]).upper()
        email_address=str(data["email_address"])
        account_number=str(data["account_number"])
        public_id=str(uuid.uuid4())
        Admin=False
        account_balance=0
        with db.engine.connect() as connection:
                create_a_bank_account=t("INSERT INTO user(password, username, email_address, account_number, public_id, account_balance, Admin) VALUES(:password, :username, :email_address, :account_number, :public_id, :account_balance, :Admin)")
                connection.execute(create_a_bank_account, {"password":password, "username":username, "email_address":email_address, "account_number":account_number, "public_id":public_id, "account_balance":account_balance, "Admin":Admin})
                connection.commit()
                return({"Account_created_successfully_Your_Public_id_is": public_id}), 201
    except KeyError as k:
        abort(400, description=f"Missing data, Key is missing: {str(k)}")
    except ValueError as v:
        abort(400, description=f"Invalid data, there is an error in your input: {str(v)}")
    except SQLAlchemyError as s:
        abort(500, description=f"Database Error: {str(s)}")
    except Exception as e:
        abort(400, description=f"An Unexpected error as occurred in the course of your registration: {str(e)}")


@app.route("/user/<public_id>", methods=["GET"])
@token_required
def check_account_details(current_user, public_id):
    User()
    if not current_user:
        return({"message": "Unauthorized!. login required"}), 401
    with db.engine.connect() as connection:
        account_details=t("SELECT * FROM user WHERE public_id=:public_id")
        user_data=connection.execute(account_details, {"public_id":public_id})
        user=user_data.fetchone()
        if not user:
            return({"message": "user not found!"}), 404
        user_dict= user._asdict()
        return({"user":user_dict}), 200
    
  
@app.route("/user", methods=["GET"])
@token_required
def get_all_bank_account_users(current_user):
    User()
    if not current_user.Admin:
        return({"message": "Unauthorized!"}), 401
    with db.engine.connect() as connection:
        all_bank_user=t("SELECT * FROM user")
        userData=connection.execute(all_bank_user)
        output=[]
        for user in userData:
            user_data={}
            user_data["username"] = user.username
            user_data["email_address"] = user.email_address
            user_data["password"] = user.password
            user_data["public_id"] = user.public_id
            user_data["account_number"] = user.account_number
            user_data["account_balance"] = user.account_balance
            user_data["Admin"] = user.Admin
            output.append(user_data)
        return({"user":output}), 200


@app.route("/transaction", methods=["GET"])
@token_required
def get_transaction_details(current_user):
    Transaction()
    if not current_user.Admin:
        return({"message":"Unauthorized!"}), 401
    with db.engine.connect() as connection:
        transaction_details=t("SELECT * FROM transaction")
        transaction_data=connection.execute(transaction_details)
        output=[]
        for transaction in transaction_data:
            output.append(transaction._asdict())
        return({"Transaction details":output}), 200
    
    

@app.route("/user/<public_id>", methods=["PUT"])
@token_required
def update_bank_user_account_details(current_user, public_id):
    try:
        User()
        if not current_user:
            return({"message": "You can't perform this operation!"}), 401
        data=request.get_json()
        if not data:
            abort(400, description="Invalid input")
        required_fields=["username", "email_address", "password"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Missing field: {field}")
        hashed_password=generate_password_hash(password=data["password"], method="pbkdf2:sha256")
        username=str(data["username"]).upper()
        email_address=str(data["email_address"])
        password=hashed_password
        with db.engine.connect() as connection:
            a_bank_user_account_details=t("UPDATE user SET username=:username, email_address=:email_address, password=:password WHERE public_id=:public_id")
            user=connection.execute(a_bank_user_account_details, {"username":username, "email_address":email_address, "password":password, "public_id":public_id})
            if not user:
                return({"message":"you can't perform this operation!"}), 404
            connection.commit()
            return({"message":"A bank user account details updated successfully!"}), 200
    except KeyError as k:
        abort(400, description=f"Missing data, Key error: {str(k)}")
    except ValueError as v:
        abort(400, description=f"Invalid data, there's an error your input: {str(v)}")
    except SQLAlchemyError as s:
        abort(500, description=f"Database error, Try again!: {str(s)}")
    except Exception as e:
        abort(400, description=f"An error occurred during update: {str(e)}")

@app.route("/admin/<public_id>", methods=["PUT"])
def is_admin(public_id):
    try:
        User()
        data=request.get_json()
        if not data:
            abort(400, description=f"Invalid input!")
        required_fields=["username", "email_address", "password"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Missing required field: {field}")
        hashed_password=generate_password_hash(password=data["password"], method="pbkdf2:sha256")
        username=str(data["username"]).upper()
        email_address=str(data["email_address"])
        password=hashed_password
        Admin=True
        with db.engine.connect() as connection:
            promote_user=t("UPDATE user SET username=:username, email_address=:email_address, password=:password, Admin=:Admin WHERE public_id=:public_id")
            user=connection.execute(promote_user, {"username":username, "email_address":email_address, "password":password, "Admin":Admin, "public_id":public_id})
            if not user:
                return({"message":"user not found!"}), 404
            connection.commit()
            return({"message":"A user promoted!"}), 200
    except KeyError as k:
        abort(400, description=f"Missing data, Key is missing, Cross-check!: {str(k)}")
    except ValueError as v:
        abort(400, description=f"Invalid data, The Value you inserted is Invalid!: {str(v)}")
    except SQLAlchemyError as s:
        abort(500, description=f"Database error, Try again: {str(s)}")
    except Exception as e:
        abort(400, description=f"An error has occurred during promotion: {str(e)}")
    

@app.route("/user/<public_id>", methods=["DELETE"])
@token_required
def delete_user_account(current_user, public_id):
    User()
    if not current_user.Admin:
        return({"message": "Unauthorized!"}), 401
    with db.engine.connect() as connection:
        user_account=t("DELETE FROM user WHERE public_id=:public_id")
        user=connection.execute(user_account, {"public_id":public_id})
        if not user:
            return({"message": "User not found!"}), 404
        connection.commit()
        return({"message": "user account deleted!"}), 200
    
    
@app.route("/login", methods=["POST"])
def login():
    try:
        User()
        data=request.get_json()
        if not data or not data.get("username") or not data.get("password"):
            return({"message":"Invalid input!"}), 400
        required_fields=["username", "password"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Missing field: {field}")
        username=str(data["username"]).upper()
        password=str(data["password"])
        with db.engine.connect() as connection:
            get_user=t("SELECT * FROM user WHERE username=:username")
            user_data=connection.execute(get_user, {"username":username})
            user=user_data.first()
        if not user or not check_password_hash(user.password, password):
            return({"message":"could not verify"})
        token=jwt.encode({"public_id":user.public_id, "exp":datetime.datetime.now(datetime.UTC)+datetime.timedelta(minutes=60)}, app.config["SECRET_KEY"])
        return({"Token":token}), 200
    except KeyError as k:
        abort(400, description=f"Missing data, There's no key: {str(k)}")
    except ValueError as v:
        abort(400, description=f"Invalid data, Your Inserted the a wrong value: {str(v)}")
    except SQLAlchemyError as s:
        abort(500, description=f"Database error, Try again: {str(s)}")
    except Exception as e:
        abort(400, description=f"An error occurred during your login: {str(e)}")

    


@app.route("/deposit", methods=["POST"])
@token_required
def deposit_money(current_user):
    try:
        User()
        Transaction()
        if not current_user:
            return({"message": "unauthorized!, Login required"}), 401
        data=request.get_json()
        if not data:
            abort(400, description="Invalid input")
        required_fields=["username", "amount", "account_number"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f"Missing required field: {field}")
        username=str(data["username"]).upper()
        account_number=str(data["account_number"])
        amount=float(data["amount"])
        if not username or not amount:
            return({"message": "username, account_number and amount are required!"}), 400
        with db.engine.connect() as connection:
                fetching_account_user_details=t("SELECT * FROM user WHERE username=:username AND account_number=:account_number")
                userData=connection.execute(fetching_account_user_details, {"username":username, "account_number":account_number}).fetchone()
                user=userData._asdict()
                if not user:
                    return({"message": "Bank account user not found!"}), 404
                account_balance=float(user["account_balance"])
                new_account_balance=account_balance + amount
                updating_account_user=t("UPDATE user SET account_balance=:new_account_balance WHERE username=:username")
                connection.execute(updating_account_user, {"new_account_balance":new_account_balance, "username":username})
                money_deposit=t("INSERT INTO transaction(amount, user_id, transaction_type, recipient_account_number) VALUES(:amount, :user_id, :transaction_type, :recipient_account_number)")
                connection.execute(money_deposit, {"amount":amount, "user_id":user["id"], "transaction_type":TransactionTypeEnum.deposit.value, "recipient_account_number":account_number})
                connection.commit()
                return f'deposit of {amount} to {account_number} was successful!, your balance is: {new_account_balance}', 200
    except KeyError as k:
        abort(400, description=f"Missing data, Remember to check Your Well before Proceeding: {str(k)}")
    except ValueError as V:
        abort(400, description=f"Invalid data, Check Your Value Well!: {str(V)}")
    except SQLAlchemyError as s:
        abort(500, description=f"Database error, Try again!: {str(s)}")
    except Exception as e:
        abort(400, description=f"An error occurred during the course of Your Money Deposit: {str(e)}")




@app.route("/withdraw", methods=["POST"])
@token_required
def withdraw_money(current_user):
    try:
        User()
        Transaction()
        if not current_user:
            return({"message": "Unauthorized!. Login required"}), 401
        data=request.get_json()
        if not data:
            abort(400, description="Invalid input")
        required_fields=["username", "account_number", "amount"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f'Missing required field: {field}')
        username=str(data["username"]).upper()
        account_number=str(data["account_number"])
        amount=float(data["amount"])
        if not username or not amount or not account_number:
            return({"message": "username, account_number and amount are required!"}), 400
        with db.engine.connect() as connection:
                fetching_account_user_details=t("SELECT * FROM user WHERE username=:username AND account_number=:account_number")
                userData=connection.execute(fetching_account_user_details, {"username":username, "account_number":account_number}).fetchone()
                user=userData._asdict()
                if not user:
                    return({"message": "Bank account user not found!"}), 404
                account_balance=float(user["account_balance"])
                new_account_balance=account_balance - amount
                if amount > account_balance:
                    return({"message":"Insufficient fund!"}), 400
                updating_account_user=t("UPDATE user SET account_balance=:new_account_balance WHERE username=:username")
                connection.execute(updating_account_user, {"new_account_balance":new_account_balance, "username":username})
                money_withdrawer=t("INSERT INTO transaction(amount, user_id, transaction_type, recipient_account_number) VALUES(:amount, :user_id, :transaction_type, :recipient_account_number)")
                connection.execute(money_withdrawer, {"amount":amount, "user_id":user["id"], "transaction_type":TransactionTypeEnum.withdraw.value, "recipient_account_number":account_number})
                connection.commit()
                return f'Withdraw of {amount} by {username} was successful!, your balance is: {new_account_balance}', 200
    except KeyError as k:
        abort(400, description=f"Missing data, Key Error: {str(k)}")
    except ValueError as V:
        abort(400, description=f"Invalid data, Value Error: {str(V)}")
    except SQLAlchemyError as s:
        abort(500, description=f"Database error, Try again, Thank You!: {str(s)}")
    except Exception as e:
        abort(400, description=f"An error occurred when Trying to Withdraw Money: {str(e)}")
 



@app.route("/transfer", methods=["POST"])
@token_required
def transfer_money(current_user):
    try:
        User()
        Transaction()
        if not current_user:
            return({"message": "Unauthorized!. Login required"}), 401
        data=request.get_json()
        if not data:
            abort(400, description="Invalid input!")
        required_fields=["amount", "account_number", "username"]
        for field in required_fields:
            if field not in data:
                abort(400, description=f'Missing required field: {field}')
        username=str(data["username"]).upper()
        amount=float(data["amount"])
        account_number=str(data["account_number"])
        if not username or not amount or not account_number:
            return({"message": "username, account_number, amount are required!"}), 400
        with db.engine.connect() as connection:
                fetching_recipient=t("SELECT * FROM user WHERE account_number=:account_number")
                recipientData=connection.execute(fetching_recipient, {"account_number":account_number}).fetchone()
                recipient=recipientData._asdict()
                if not recipient:
                    return({"message": "Recipient not found!"}), 404
                account_balance=float(recipient["account_balance"])
                new_recipient_account_balance=account_balance + amount
                updating_recipient_account=t("UPDATE user SET account_balance=:new_recipient_account_balance WHERE account_number=:account_number")
                connection.execute(updating_recipient_account, {"new_recipient_account_balance":new_recipient_account_balance, "account_number":account_number})
                fetching_account_user_details=t("SELECT * FROM user WHERE username=:username")
                userRow=connection.execute(fetching_account_user_details, {"username":username}).fetchone()
                user=userRow._asdict()
                if not user:
                    return({"message": "Bank account user not found!"}), 404
                account_balance=float(user["account_balance"])
                new_account_balance=account_balance - amount
                if amount > account_balance:
                    return({"message":"Insufficient fund!"}), 400
                updating_account_user=t("UPDATE user SET account_balance=:new_account_balance WHERE username=:username")
                connection.execute(updating_account_user, {"new_account_balance":new_account_balance, "username":username})
                money_transfer=t("INSERT INTO transaction(amount, user_id, transaction_type, recipient_account_number) VALUES(:amount, :user_id, :transaction_type, :recipient_account_number)")
                connection.execute(money_transfer, {"amount":amount, "user_id":user["id"], "transaction_type":TransactionTypeEnum.transfer.value, "recipient_account_number":account_number})
                connection.commit()
                return f'Transfer of {amount} to {account_number} was successful!, your balance is: {new_account_balance}', 200
    except KeyError as k:
        abort(400, description=f"Missing data, Key Error: {str(k)}")
    except ValueError as V:
        abort(400, description=f"Invalid data, There's a Mistake in Your Value: {str(V)}")
    except SQLAlchemyError as s:
        abort(500, description=f"Database error, Try again!: {str(s)}")
    except Exception as e:
        abort(400, description=f"An error occurred When Trying to Transfer Money, Try again, Thank You!: {str(e)}")
 




if __name__=="__main__":
    port=int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

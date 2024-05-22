# bank_web_application

## register
### Endpoint:  '/register'

### Method: POST

### Payload:
```json
{
    "username":"",
    "password":"",
    "email_address":"",
    "account_number":""
}
```

### Response:
```json
"Status": "201",
{
"message": "Account created successfully!"
}
```
## Login
### Endpoint: '/login'

### Method: POST

### Payload:
```json
{
    "username":"",
    "password":""
}
```
### Response:
```json
"Status":"200"
{
    "Token": ""
}
```
## Fetch all user, only for admin 
### Endpoint: '/user'

### Method: GET

### Response:
```json
"Status":"200"
{
    "user": [
        {
            "Admin": ,
            "account_balance": ,
            "account_number": "",
            "email_address": "",
            "password": "",
            "public_id": "",
            "username": ""
        },
        {
            "Admin": ,
            "account_balance": ,
            "account_number": "",
            "email_address": "",
            "password": "",
            "public_id": "",
            "username": ""
        }
    ]
}
```

## Fetch a user/check user account details

### Endpoint: '/user/public_id'

### Method: GET

### Response:
```json
"status":"",
{
    "user": {
        "Admin": ,
        "account_balance": ,
        "account_number": "",
        "created_at": "",
        "email_address": "",
        "id": 1,
        "password": "",
        "public_id": "",
        "updated_at": "",
        "username": ""
    }
}
```

## Update user details

### Endpoint: '/user/public_id'

### Method: PUT

### Payload:
```json
{
    "username":"",
    "email_address":"",
    "password":""
}
```
### Response:
```json
"status":"200"
{
    "message":"A bank user account details updated successfully!"
}
```
## Promote a user to an Admin

### Endpoint: "/admin/public_id

### Method: PUT

### Payload:
```json
{
    "username":"",
    "email_address":"",
    "password":""
}
```
### Response:
```json
"status":"200"
{
    "message": "A user promoted!"
}
```
## Delete a user account, only for admin 

### Endpoint: '/user/public_id'

### Method: DELETE

### Response:
```json
"status": "200",
{
    "message":"user account deleted!"
}
```
## Deposit

### Endpoint: '/deposit'

### Method: POST

### Payload:
```json
{
    "username":"",
    "amount":,
    "account_number":""
}
```
### Response:
```json
"status":"200",
{
    "deposit of {amount} to {account_number} was successful!, your balance is: {new_account_balance}"
}
```
## Withdraw

### Endpoint: '/withdraw'

### Method: POST

### Payload:
```json
{
    "username":"",
    "amount":,
    "account_number":""
}
```
### Response:
```json
"status":"200",
{
    "Withdraw of {amount} by {username} was successful, your balance is: {new_account_balance}"
}
```
## Transfer

### Endpoint: '/transfer'

### Method: POST

### Payload:
```json
"status":"200"
{
    "account_number":"",
    "amount":,
    "username":""
}
```
### Response:
```json
"status":"200",
{
    "Transfer of {amount} to {account_number} was successful!, your balance is: {new_account_balance}"
}
```
## Get transaction details, only for admin

### Endpoint: "/transaction"

### Method: GET

### Response:
```json
"status":"200"
{
    "Transaction details": [
        {
            "amount": ,
            "created_at": "",
            "id": 1,
            "recipient_account_number":"" ,
            "transaction_type": "",
            "user_id": 1
        },
        {
            "amount": ,
            "created_at": "",
            "id": 2,
            "recipient_account_number":"" ,
            "transaction_type": "",
            "user_id": 
        },
        {
            "amount": ,
            "created_at": "",
            "id": 3,
            "recipient_account_number": "",
            "transaction_type": "",
            "user_id": 
        }
    ]
}
```
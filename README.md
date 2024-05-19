# bank_web_application

## register
### Endpoint:  '/register'

### Method: POST

### Payload:
```json
{
    "name":"",
    "password":"",
    "email_address":"",
    "account_number":"",
    "account_balance":""
}
```

### Response:
```json
"Status": "201",
{
"message": "Account created successfully!"
}
```

## sign_up
### Endpoint: '/recipient'

### method: POST

### Payload:
```json
"recipient_name":"",
"password":"",
"recipient_account__number":"",
"recipient_account_balance":""
```

### Response:
```json
"Status":"201",
{
"message":"Account created successfully!"
}
```
## Login
### Endpoint: '/login'

### Method: POST

### Payload:
```json
"Username": ""
"Password": ""
```
### Response:
```json
"Status":"200"
{
    "Token": ""
}
```
## Fetch all user
### Endpoint: '/user'

### Method: GET

### Response:
```json
"Status":"200"
{
    "user": [
        {
            "account_balance": "",
            "account_number": "",
            "email_address": "",
            "name": "",
            "password": "",
            "public_id": ""
        },
        {
            "account_balance": ,
            "account_number": "",
            "email_address": "",
            "name": "",
            "password": "",
            "public_id": ""
        },
        {
            "account_balance": ,
            "account_number": "",
            "email_address": "",
            "name": "",
            "password": "",
            "public_id": ""
        }
    ]
}
```

## Fetch a user

### Endpoint: '/user/public_id'

### Method: GET

### Response:
```json
"status":"",
{
    "user": {
        "account_balance":,
        "account_number": "",
        "created_at": "",
        "email_address": "",
        "id": ,
        "password": "",
        "public_id": "",
        "updated_at": "",
        "username": ""
    }
}
```

## Update user information

### Endpoint: '/user/public_id'

### Method: PUT

### Payload:
```json
"username":"",
"email_address":"",
"password":""
```
### Response:
```json
"status":"200"
{
    "message":"A bank user account details updated successfully!"
}
```
## Delete a user account

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
"username":"",
"account_number":"",
"amount":""
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
"username":"",
"account_number":"",
"amount":""
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
"amount":"",
"username":"",
"recipient_account_number": "",
"recipient_username":"",
"sender_name":""
```
### Response:
```json
"status":"200",
{
    "Transfer of {amount} to {recipient_account_number} was successful!, your balance is: {new_account_balance}"
}
```

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

### Method: GET

### Login using Username and Password

### Payload:
```json
Username: ""
Password: ""
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

### Reponse:
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

### Enpoint: '/user/public_id'

### Method: GET

### Response:
```json

```
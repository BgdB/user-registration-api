# User registration api

## Running the api

To start the service, in a terminal, run the following command:
```
docker-compose up
```

This will setup the service on `http://localhost:8000`

## Running the tests

To run the unittests, in a terminal, run the following command:
```
docker-compose up tests
```

## Registering a user

The endpoint for registering a new user is: `POST  /register` with a json body in the following format:
```
{
  "email": "email@email.com",
  "password": "Password123!",
}
```
The email should be a valid email format and the password must be at least 8 characters, contain at least one upper character, lower character, digit and special character

## Activate an account
The endpoint for activating an account is: `POST  /activate` with a json body in the following format:
```
{
  "code": "123"  # 4 digit code received
}
```

This endpoint uses basic auth in order to identify the user - so the username and password must be sent in the corresponding headers.
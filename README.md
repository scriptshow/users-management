# users-management
Small Django application to manage (CRUD) users and their bank account data (IBAN)

# Dependencies
Python                              3.7

Django                              2.1.5

django-cors-headers                 2.4.0

djangorestframework                 3.9.0

psycopg2                            2.7.7

social-auth-app-django              3.1.0

# Installation
It's docker based so, all you need is internet connection, a database already configured and run the Dockerfile

# Configuration
Inside the Dockerfile you have the following variables who you must to modify:

ALLOWED_HOSTS -> localhost and 127.0.0.1 are allowed by default, use this to allow an additional host if needed, if not
leave it as empty

POSTGRES_DB_NAME -> DB name in your postgresSQL

POSTGRES_DB_HOST -> DB host where is running your postgreSQL

POSTGRES_DB_PORT -> Port where your postgreSQL is listening

POSTGRES_DB_USERNAME -> Username with write rights on the database given

POSTGRES_DB_PASSWORD -> Password related to the username given

GOOGLE_OAUTH2_KEY -> Google KEY used for the OAUTH2

GOOGLE_OAUTH2_SECRET -> Google Secret KEY used for the OAUTH2

**Important:** You need to grant all access to user in database provided

# Executing
Open a command line into the folder where Dockerfile is present.

Execute the following command to build our container:

`docker build -t usermanagement .`

After the success build, run following command to run our application:

`docker run -p 8000:8000 -p 5432:5432 --name usertest usermanagement`

After successfully ran the tests, if you want to run the application in work mode, you need to modify the Dockerfile
again, removing the comments where its indicated and comment the tests; then, repeat the build and run docker processes

# API Reference

***Authentication***

Method: POST

URL: _/auth/google_oauth2/_

Body: `{
    "access_token": "google_access_token"
}`

Response: `{"token": "django_auth_token"}`

***Get all accounts***

Method: GET

URL: _/accounts/get/all/_

Headers: `{
    "Authorization": "Token django_auth_token"
}`

Response: 
`[
    {
        'id': "integer",
        'first_name': "string",
        'last_name': "string",
        'iban': "string",
        'is_editable': "boolean",
    },    
]`

***Add new account***

Method: POST

URL: _/accounts/add/_

Headers: `{
    "Authorization": "Token django_auth_token"
}`

Body: 
`{
    'first_name': "string",
    'last_name': "string",
    'iban': "string",
}`

Response:
`{
    "status": "ok",
    "message": "created"
}`

***Update account***

Method: PUT

URL: _/accounts/update/_

Headers: `{
    "Authorization": "Token django_auth_token"
}`

Body: 
`[
    {
        'id': "integer",
        'first_name': "string",
        'last_name': "string",
        'iban': "string",
    },    
]`

Response:
`{
    "status": "ok", 
    "message": "updated"
}`

***Delete account***

Method: DELETE

URL: _/accounts/delete/_

Headers: `{
    "Authorization": "Token django_auth_token"
}`

Body: 
`[
    {
        'id': "integer",
        'first_name': "string",
        'last_name': "string",
        'iban': "string",
    },    
]`

Response:
`{
    "status": "ok", 
    "message": "deleted"
}`

***Logout***

Method: POST

URL: _/logout/_

Headers: `{
    "Authorization": "Token django_auth_token"
}`

Response: 
` `

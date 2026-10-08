# JobTrex
JobTrex is a job finder mobile application where employers post job and hire those that applied for the job

Register as an applicant

POST /api/v1/register

{
    "firstname": "your firstname",
    "lastname": "your lastname",
    "email": "your email",
    "password": "your password",
    "role": "applicant",
    "country": "your country"
}

Register as an employer

POST /api/v1/register

{
    "firstname": "your firstname",
    "lastname": "your lastname",
    "email": "your email",
    "password": "your password",
    "role": "employer",
    "country": "your country"
}


User Login

POST /api/v1/login

{
  "email": "your email",
  "password": "your password"
}


User logout

POST /api/v1/logout

Authorization: Bearer #your refresh token


Generating access token

POST /api/v1/refresh

Authorization: Bearer #your refresh token

Forgotten Password

POST /api/v1/forgot-password


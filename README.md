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

{
  "email": "your email"
}

A 5 minute OTP is sent to the email address


Verify OTP

POST /api/v1/verify

{
  "otp": "the otp sent to your email"
}


Reset Password (verify the OTP first)

POST /api/v1/reset

{
  "email": "your email",
  "password": "your new password",
  "confirm_password": "your new password"
}


Post a job (employer)

POST /api/v1/post-job

Authorization: Bearer #your access token

Send as form-data (not JSON)

title: job title
description: job description
location: job location
salary: job salary
picture: job image file


Get my jobs (employer)

GET /api/v1/my-jobs

Authorization: Bearer #your access token

Returns the jobs created by the logged in employer, each with title, description, salary, location and picture


Apply for a job (applicant)

POST /api/v1/apply

Authorization: Bearer #your access token

{
  "job_id": 1
}


Get applicants for a job

GET /api/v1/applicants?job_id=1&page=1&per_page=10

Authorization: Bearer #your access token

job_id is the job you want the applicants for, page defaults to 1 and per_page defaults to 10

Each result has job_id, title, applicants (full name) and status (pending, accepted or rejected)


Employ an applicant (employer)

POST /api/v1/employ

Authorization: Bearer #your access token

{
  "job_id": 1,
  "applicant_id": 2
}

Changes the applicant's status for that job to accepted


Get employed applicants for a job

GET /api/v1/employed?job_id=1&page=1&per_page=10

Authorization: Bearer #your access token

Returns only the applicants whose status is accepted for the job, page defaults to 1 and per_page defaults to 10


Get an uploaded file (profile picture, CV or job image)

GET /uploads/<filepath>

Use the path returned by the API, for example /uploads/jobs/<filename>.jpg


Health check

GET /health


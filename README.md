# JobTrex
JobTrex is a job finder mobile application where employers post job and hire those that applied for the job

## Setup

1. Install Python 3.12+ and PostgreSQL, then create a database
2. Install the dependencies

```
pip install -r requirements.txt
```

3. Create a `.env` file in the project root

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/jobtrex
JWT_SECRET_KEY=a long random secret
MAIL_SERVER=smtp.example.com
SENDER=no-reply@example.com
MAIL_USERNAME=your mail username
MAIL_PASSWORD=your mail password
```

DATABASE_URL and JWT_SECRET_KEY are required, the app will not start without them.

4. Run the app

```
python app.py
```

For production use `gunicorn app:app`

Uploaded files are saved in the `uploads` folder (profile, cv and jobs), the folders are created automatically.

## Authentication and roles

- Access token expires after 15 minutes, refresh token after 30 days
- Send tokens as `Authorization: Bearer <token>`
- Roles: `applicant` and `employer`. Applicants can only apply for jobs, employers can only post jobs and manage the applicants of their own jobs
- Errors and confirmations return JSON with a `msg` field
- Status codes: 400 invalid input, 401 not logged in or invalid credentials, 403 not allowed for your role or not your job, 404 not found, 409 already applied, 413 upload too large (16MB max)

## Endpoints

Register as an applicant

POST /api/v1/register

Send as form-data (not JSON)

```
firstname: your firstname
lastname: your lastname
email: your email
password: your password (at least 6 characters)
role: applicant
country: your country
profile_picture: image file (optional)
cv: cv file, pdf, doc or docx (required)
```

Register as an employer

POST /api/v1/register

Send as form-data (not JSON)

```
firstname: your firstname
lastname: your lastname
email: your email
password: your password (at least 6 characters)
role: employer
country: your country
profile_picture: image file (optional)
```


User Login

POST /api/v1/login

```json
{
  "email": "your email",
  "password": "your password"
}
```

Returns

```json
{
  "msg": "Login successful",
  "role": "applicant",
  "is_verified": false,
  "access_token": "...",
  "refresh_token": "..."
}
```


User logout

POST /api/v1/logout

Authorization: Bearer #your refresh token

Only the refresh token is revoked, the access token stays valid until it expires (15 minutes)


Generating access token

POST /api/v1/refresh

Authorization: Bearer #your refresh token

Returns `{"access_token": "..."}`


Forgotten Password

POST /api/v1/forgot-password

```json
{
  "email": "your email"
}
```

A 5 minute OTP (6 digits) is sent to the email address. The same msg is returned whether the email exists or not. Requesting a new OTP invalidates the previous one, and expired OTPs are deleted automatically.


Verify OTP

POST /api/v1/verify

```json
{
  "otp": "the otp sent to your email",
  "email": "your email"
}
```

`email` is optional for now but you should always send it. After verifying you have 5 minutes to reset the password.


Reset Password (verify the OTP first)

POST /api/v1/reset

```json
{
  "email": "your email",
  "password": "your new password",
  "confirm_password": "your new password"
}
```

The password must be at least 6 characters. The OTP can only be used once, request a new one to reset again.


Post a job (employer)

POST /api/v1/post-job

Authorization: Bearer #your access token

Send as form-data (not JSON)

```
title: job title
description: job description
location: job location
salary: job salary (a number)
picture: job image file
```


Get my jobs (employer)

GET /api/v1/my-jobs

Authorization: Bearer #your access token

Returns the jobs created by the logged in employer, each with id, title, description, salary, location and picture (full image url). Use the id as the job_id in the other endpoints.


Apply for a job (applicant)

POST /api/v1/apply

Authorization: Bearer #your access token

```json
{
  "job_id": 1
}
```

Returns 404 if the job does not exist and 409 if you already applied


Get applicants for a job (employer)

GET /api/v1/applicants?job_id=1&page=1&per_page=10

Authorization: Bearer #your access token

job_id is the job you want the applicants for (it must be your own job), page defaults to 1 and per_page defaults to 10

Each result has job_id, title, applicant_id, applicants (full name) and status (pending, accepted or rejected)


Employ an applicant (employer)

POST /api/v1/employ

Authorization: Bearer #your access token

```json
{
  "job_id": 1,
  "applicant_id": 2
}
```

applicant_id comes from the applicants endpoint. Changes the applicant's status for that job to accepted. The job must be yours.


Get employed applicants for a job (employer)

GET /api/v1/employed?job_id=1&page=1&per_page=10

Authorization: Bearer #your access token

Returns only the applicants whose status is accepted for your job, page defaults to 1 and per_page defaults to 10. Returns an empty list when nobody is employed yet.


Browse jobs (any logged in user)

GET /api/v1/jobs?page=1&per_page=10&search=developer&location=lagos

Authorization: Bearer #your access token

Returns the newest jobs first, each with id, title, description, salary, location, picture (full image url) and employer (full name). search matches the job title and location matches the job location, both are optional. Returns an empty list when nothing matches.


Get a job

GET /api/v1/job?job_id=1

Authorization: Bearer #your access token

Returns one job with id, title, description, salary, location, picture and employer. Returns 404 if the job does not exist.


My applications (applicant)

GET /api/v1/my-applications?page=1&per_page=10

Authorization: Bearer #your access token

Returns the jobs you applied for, newest first, each with job_id, title, location, salary and status (pending, accepted or rejected)


Withdraw an application (applicant)

DELETE /api/v1/withdraw?job_id=1

Authorization: Bearer #your access token

Removes your application for the job. Returns 404 if you did not apply for it.


Reject an applicant (employer)

POST /api/v1/reject

Authorization: Bearer #your access token

```json
{
  "job_id": 1,
  "applicant_id": 2
}
```

Changes the applicant's status for that job to rejected and sends the applicant an email. The job must be yours.


Edit a job (employer)

POST /api/v1/edit-job

Authorization: Bearer #your access token

Send as form-data (not JSON). Only job_id is required, send only the fields you want to change.

```
job_id: the job id
title: new job title
description: new job description
location: new job location
salary: new job salary (a number)
picture: new job image file
```

The job must be yours.


Delete a job (employer)

DELETE /api/v1/delete-job?job_id=1

Authorization: Bearer #your access token

Deletes the job and all its applications. The job must be yours.


Get an applicant's profile and CV (employer)

GET /api/v1/applicant-profile?job_id=1&applicant_id=2

Authorization: Bearer #your access token

Returns the profile of an applicant who applied for your job: id, firstname, lastname, email, role, country, profile_picture, cv (full urls) and is_verified. Open the cv url with your access token, see the uploads endpoint below.


Get my profile

GET /api/v1/profile

Authorization: Bearer #your access token

Returns your id, firstname, lastname, email, role, country, profile_picture, cv (full urls, null if none) and is_verified


Update my profile

POST /api/v1/update-profile

Authorization: Bearer #your access token

Send as form-data (not JSON). Send only the fields you want to change.

```
firstname: your firstname
lastname: your lastname
country: your country
profile_picture: new image file
cv: new cv file, pdf, doc or docx (applicants only)
```


Change my password

POST /api/v1/change-password

Authorization: Bearer #your access token

```json
{
  "old_password": "your current password",
  "new_password": "your new password",
  "confirm_password": "your new password"
}
```

The new password must be at least 6 characters


Send email verification

POST /api/v1/send-verification

Authorization: Bearer #your access token

Sends a link to your email address that is valid for 24 hours. Returns 400 if your email is already verified.


Verify email

GET /api/v1/verify-email?token=<token from the email link>

No token needed, the user opens the link from the email. Sets is_verified to true.


Email notifications

- The employer gets an email when an applicant applies for their job
- The applicant gets an email when they are employed or rejected


Get an uploaded file (profile picture, CV or job image)

GET /uploads/<filepath>

Use the path returned by the API, for example /uploads/jobs/<filename>.jpg

Profile pictures and job images are public. Files in /uploads/cv/ need an access token (`Authorization: Bearer #your access token`)


Health check

GET /health

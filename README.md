# S3 Upload Site

This is a simple Flask application that authenticates users using Okta Primary Authentication and allows uploading files to an Amazon S3 bucket. Files can be uploaded by dragging and dropping them onto the page and are displayed in a list with the ability to delete them.

## Setup

1. Create a Python virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with the following variables:

```
SECRET_KEY=change-me
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
S3_BUCKET=your-bucket
OKTA_DOMAIN=your-okta-domain
```

3. Run the application:

```bash
python app.py
```

Visit `http://localhost:5000` to log in and upload files.

## Features

- Okta Primary Authentication using the `/api/v1/authn` endpoint
- Drag & Drop multiple file upload
- Automatic upload when files are dropped
- List existing files in the S3 bucket
- Delete files via the trash icon

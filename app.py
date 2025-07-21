from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import boto3
import os
import requests
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "changeme")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET")

OKTA_DOMAIN = os.getenv("OKTA_DOMAIN")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def is_logged_in():
    return "user" in session


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not OKTA_DOMAIN:
            return render_template("login.html", error="Okta domain not configured")
        resp = requests.post(
            f"https://{OKTA_DOMAIN}/api/v1/authn",
            json={"username": username, "password": password},
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        if resp.status_code == 200 and resp.json().get("status") == "SUCCESS":
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    if not is_logged_in():
        return redirect(url_for("login"))
    query = request.args.get("q", "")
    objects = s3.list_objects_v2(Bucket=S3_BUCKET)
    files = [obj["Key"] for obj in objects.get("Contents", [])]
    if query:
        files = [f for f in files if query.lower() in f.lower()]
    return render_template("index.html", files=files, query=query)


@app.route("/upload", methods=["POST"])
def upload():
    if not is_logged_in():
        return jsonify({"error": "unauthorized"}), 401
    uploaded_files = request.files.getlist("files")
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        if filename:
            s3.upload_fileobj(file, S3_BUCKET, filename)
    return jsonify({"success": True})


@app.route("/delete/<path:filename>", methods=["POST"])
def delete_file(filename):
    if not is_logged_in():
        return jsonify({"error": "unauthorized"}), 401
    s3.delete_object(Bucket=S3_BUCKET, Key=filename)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

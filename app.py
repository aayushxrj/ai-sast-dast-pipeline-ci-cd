import os
import subprocess
import pickle
import hashlib
import jwt
import requests
from flask import Flask, request, make_response

app = Flask(__name__)

# 🔓 Hardcoded secret key (Gitleaks, Semgrep)
SECRET_KEY = "supersecret123"

# 🔓 Hardcoded credentials (Gitleaks)
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

@app.route("/dangerous", methods=["GET"])
def dangerous():
    # ❗ Use of eval (Bandit, Semgrep)
    code = request.args.get("code")
    return str(eval(code))  # ⚠️ Arbitrary code execution

@app.route("/exec", methods=["GET"])
def exec_cmd():
    # ❗ Use of subprocess with unsanitized input (Bandit)
    cmd = request.args.get("cmd")
    return subprocess.check_output(cmd, shell=True).decode()  # ⚠️ Shell injection

@app.route("/pickle", methods=["POST"])
def unpickle_data():
    # ❗ Insecure deserialization (Bandit)
    data = request.data
    return str(pickle.loads(data))  # ⚠️ Arbitrary code execution

@app.route("/jwt", methods=["GET"])
def insecure_jwt():
    # ❗ Insecure JWT with 'none' algorithm (Semgrep)
    payload = {"user": "admin"}
    token = jwt.encode(payload, key=None, algorithm="none")
    return token

@app.route("/md5", methods=["POST"])
def weak_hash():
    # ❗ Weak hash function (Bandit)
    password = request.form["password"]
    return hashlib.md5(password.encode()).hexdigest()  # ⚠️ Weak hashing

@app.route("/ssrf", methods=["GET"])
def ssrf():
    # ❗ SSRF vulnerability (Semgrep)
    url = request.args.get("url")
    response = requests.get(url)  # ⚠️ SSRF
    return response.text

    
@app.route("/sql", methods=["GET"])
def sql_injection():
    # ❗ SQL Injection vulnerability (for SAST/DAST)
    username = request.args.get("username")
    query = f"SELECT * FROM users WHERE username = '{username}'"  # ⚠️ SQL Injection
    # Simulate execution (do not actually run this in production)
    return f"Executed query: {query}"

@app.route("/readfile", methods=["GET"])
def read_file():
    # ❗ Path traversal vulnerability (for SAST/DAST)
    filename = request.args.get("file")
    with open(filename, "r") as f:  # ⚠️ Path traversal
        content = f.read()
    return content
    
@app.route("/sql", methods=["GET"])
def sql_injection():
    # ❗ SQL Injection vulnerability (for SAST/DAST)
    username = request.args.get("username")
    query = f"SELECT * FROM users WHERE username = '{username}'"  # ⚠️ SQL Injection
    # Simulate execution (do not actually run this in production)
    return f"Executed query: {query}"

@app.route("/readfile", methods=["GET"])
def read_file():
    # ❗ Path traversal vulnerability (for SAST/DAST)
    filename = request.args.get("file")
    with open(filename, "r") as f:  # ⚠️ Path traversal
        content = f.read()
    return content


if __name__ == "__main__":
    app.run(debug=True)

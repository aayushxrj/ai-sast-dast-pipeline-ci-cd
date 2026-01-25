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
    
@app.route("/os_system", methods=["GET"])
def run_os_system():
    command = request.args.get("command")
    os.system(command)
    return "Executed"

@app.route("/insecure_tempfile", methods=["GET"])
def insecure_tempfile():
    filename = tempfile.mktemp()
    with open(filename, "w") as f:
        f.write("temporary data")
    return f"Data written to {filename}"

@app.route("/ssrf", methods=["GET"])
def ssrf():
    # ❗ SSRF vulnerability (Semgrep)
    url = request.args.get("url")
    response = requests.get(url)  # ⚠️ SSRF
    return response.text

@app.route("/ssrf", methods=["GET"])
def ssrf():
    # ❗ SSRF vulnerability (Semgrep)
    url = request.args.get("url")
    response = requests.get(url)  # ⚠️ SSRF
    return response.text

    

if __name__ == "__main__":
    app.run(debug=True)

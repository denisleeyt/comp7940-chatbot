from flask import Flask, request
import subprocess
import hmac
import hashlib

app = Flask(__name__)

GITHUB_SECRET = "your_github_webhook_secret"

def verify_signature(payload, signature, secret):
    calculated_signature = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(calculated_signature, signature)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_data()
    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_signature(payload, signature, GITHUB_SECRET):
        return "Invalid signature", 400

    subprocess.Popen(["/home/ubuntu/start.sh"])
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from services.webhook_service import verify_webhook_signature


# Load environment variables from project .env
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def receive_webhook():

    secret = os.getenv("WEBHOOK_SECRET", "")

    signature = request.headers.get(
        "X-Webhook-Signature",
        ""
    )

    # Validate HMAC signature
    if not secret or not verify_webhook_signature(
        request.get_data(),
        signature,
        secret
    ):
        return jsonify({
            "error": "Invalid signature"
        }), 401

    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({
            "error": "Invalid JSON payload"
        }), 400

    print("Webhook received:", payload)

    return jsonify({
        "message": "Webhook received successfully"
    }), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )

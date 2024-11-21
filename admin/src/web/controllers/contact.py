import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from src.core.module.contact import ContactMessageForm

load_dotenv()
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")


contact_bp = Blueprint("contact_bp", __name__, url_prefix="/api/contact")


def verify_recaptcha(recaptcha_response):
    """Verify reCAPTCHA response with Google's API"""
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": RECAPTCHA_SECRET_KEY, "response": recaptcha_response}

    response = requests.post(verify_url, data=payload, timeout=10)
    result = response.json()

    return result.get("success", False)


@contact_bp.route("/message", methods=["POST"])
def contact():
    print(request.get_json())
    try:
        data = request.get_json()
        recaptcha_response = data.get("recaptchaToken")
        if not recaptcha_response:
            return jsonify({"message": "reCAPTCHA verification required"}), 410

        if not verify_recaptcha(recaptcha_response):
            return jsonify({"message": "Invalid reCAPTCHA"}), 411
        
        # TODO: Validate with WTForms
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        print(f"Received message from {name} ({email}): {message}")

        return jsonify({"message": "Message sent successfully"}), 200

    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

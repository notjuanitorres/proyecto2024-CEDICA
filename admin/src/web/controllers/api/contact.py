import os
import requests
from flask import Blueprint, request, jsonify
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from src.core.module.contact import ContactMessageForm
from src.core.module.contact.mappers import ContactMapper
from src.core.module.contact.repositories import ContactRepository
from src.core.module.contact.models import MessageStateEnum

load_dotenv()
CAPTCHA_SECRET_KEY = os.getenv("CAPTCHA_SECRET_KEY")

csrf = CSRFProtect()

contact_api_bp = Blueprint("contact_api_bp", __name__, url_prefix="/contact")

def verify_recaptcha(recaptcha_response):
    """Verify reCAPTCHA response with Google's API"""
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": CAPTCHA_SECRET_KEY, "response": recaptcha_response}

    response = requests.post(verify_url, data=payload, timeout=10)
    result = response.json()

    return result.get("success", False)


@contact_api_bp.route("/message", methods=["POST"])
@csrf.exempt
def contact():
    try:
        data = request.get_json()
        recaptcha_response = data.get("recaptchaToken")
        if not recaptcha_response:
            return jsonify({"message": "reCAPTCHA verification required"}), 410

        if not verify_recaptcha(recaptcha_response):
            return jsonify({"message": "Invalid reCAPTCHA"}), 411
        
        data = {
            "name": data.get("name"),
            "email": data.get("email"),
            "message": data.get("message"),
        }

        message_form = ContactMessageForm(data=data)
        if not message_form.validate_on_submit():
            return jsonify({"errors": message_form.errors}), 201

        data["status"] = MessageStateEnum.PENDING
        new_message = ContactRepository().add_message(ContactMapper.to_entity(data))
        print(new_message)

        #print(f"Received message from {name} ({email}): {message}")

        return jsonify({"message": "Message sent successfully"}), 200

    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500


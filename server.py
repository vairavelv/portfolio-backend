from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
CORS(app)

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

@app.post("/send")
def send_mail():
    try:
        data = request.json

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        full_message = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Message:
{message}
"""

        msg = MIMEText(full_message)
        msg["Subject"] = "New Contact Form Message"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        return jsonify({"success": True}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False}), 500


@app.get("/")
def home():
    return "Backend Running ❤️", 200


if __name__ == "__main__":
    app.run(port=5000)

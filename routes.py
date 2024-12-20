import logging
from flask import render_template, request, jsonify
from flask import current_app as app
from models.contact import ContactMessage
from models.models import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_routes(app):
    @app.route("/")
    def home_route():
        return render_template("home.html")

    @app.route("/api/contact", methods=["POST"])
    def contact_route():
        try:
            data = request.json
            name = data.get("name")
            email = data.get("email")
            message = data.get("message")

            if not all([name, email, message]):
                return jsonify({"error": "All fields are required"}), 400

            contact_message = ContactMessage(
                name=name,
                email=email,
                message=message
            )

            db.session.add(contact_message)
            db.session.commit()

            return jsonify({"message": "Message sent successfully"}), 200
        except Exception as e:
            logger.error(f"Error in contact route: {str(e)}")
            return jsonify({"error": "An error occurred while sending the message"}), 500
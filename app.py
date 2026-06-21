"""
Application entry point.
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from database.mongo_client import Db
from routes.tracking import bpTracking
from routes.users import bpUsers
from routes.products import bpProducts


def create_app():
    """
    Creates flask app
    """
    app = Flask(__name__)
    CORS(app)

    @app.route("/health", methods=["GET"])
    def health():
        try:
            db = Db()
            db.client.admin.command("ping")
            return jsonify({
                "status": "ok",
                "database": "connected"
            }), 200
        except Exception as error:
            return jsonify({
                "status": "error",
                "database": str(error)
            }), 500

    app.register_blueprint(bpTracking)
    app.register_blueprint(bpUsers)
    app.register_blueprint(bpProducts)

    return app

if __name__ == "__main__":
    _app = create_app()
    port = int(os.environ.get("PORT", 5000))
    _app.run(host="0.0.0.0", port=port, debug=True)

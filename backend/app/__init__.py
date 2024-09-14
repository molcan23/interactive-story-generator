from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allows cross-origin requests

    from .routes import story_bp
    app.register_blueprint(story_bp)

    return app

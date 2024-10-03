from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Import other modules from your app directory here
from . import routes
from . import utils
# from . import prompt_templates
# from . import backhand_variables

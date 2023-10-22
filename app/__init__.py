from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

from app import routes
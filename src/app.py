from flask import Flask
import os
from dotenv import load_dotenv

# Application initializations
app = Flask(__name__)

load_dotenv()
# settings
app.secret_key = os.getenv('secret_key')

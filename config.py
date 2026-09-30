import os
from dotenv import load_dotenv

# Load variables from .env file into the system environment
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Later on GCP, Cloud Run will securely inject DATABASE_URL into the environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Required for things like session management and form security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')

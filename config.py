import os
from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / 'secret.env'
load_dotenv(dotenv_path=env_path)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    BRAND = os.environ.get('BRAND') or 'My Brand'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_duper_secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'db/users.db')
    SQLALCHEMY_BINDS = {
        'my_data': os.environ.get('SQLALCHEMY_BIND_MY_DATA') or "sqlite:///" + os.path.join(basedir, "db/my_data.db")
    }
    IMG_FILE_DIR = os.environ.get('IMG_FILE_DIR') or os.path.join(basedir, "db/default/img")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    AUTHORITY = f"https://login.microsoftonline.com/{os.environ.get('TENANT_ID')}"
    REDIRECT_PATH = os.environ.get('REDIRECT_PATH') or '/getAToken'
    ENDPOINT = 'https://graph.microsoft.com/v1.0/users'
    SCOPE = ["User.ReadBasic.All"]

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    BRAND = os.environ.get('BRAND') or 'My Brand'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'db/users.db')
    SQLALCHEMY_BINDS = {
        'my_data': os.environ.get('SQLALCHEMY_BIND_MY_DATA') or "sqlite:///" + os.path.join(basedir, "db/my_data.db")
    }
    IMG_FILE_DIR = os.environ.get('IMG_FILE_DIR') or os.path.join(basedir, "db/img")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


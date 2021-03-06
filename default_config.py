import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
SECRET_KEY = os.environ["APP_SECRET_KEY"]
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
SECURITY_CONFIRMABLE = False
SECURITY_USER_IDENTITY_ATTRIBUTES = ['username']
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = os.environ["PASSWORD_SALT"]
SECURITY_LOGIN_URL = "/login_admin"
SECURITY_LOGOUT_URL = "/logout_admin"
SECURITY_MSG_USER_DOES_NOT_EXIST = ('Invalid credentials!', 'error')
SECURITY_MSG_INVALID_PASSWORD = ('Invalid credentials!', 'error')
SECURITY_POST_LOGIN_VIEW = "/admin"

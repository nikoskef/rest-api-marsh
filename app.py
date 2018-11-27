from flask import Flask, jsonify
import os
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv

from ma import ma
from db import db
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.room import Room, RoomList, RoomCreate
from libs.strings import gettext

from resources.category import Category, CategoryList

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_admin_to_jwt(identity):
    if identity in os.environ["ADMINS"].split(','):
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": gettext("token_expired"),
        "error": gettext("token_expired_error")
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": gettext("token_invalid"),
        "error": gettext("token_invalid_error")
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": gettext("token_missing"),
        "error": gettext("token_missing_error")
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": gettext("token_revoked"),
        "error": gettext("token_revoked_error")
    }), 401


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Category, "/category/<string:name>")
api.add_resource(CategoryList, "/categories")
api.add_resource(Room, '/room/<int:_id>')
api.add_resource(RoomCreate, '/room/create')
api.add_resource(RoomList, '/rooms')
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)

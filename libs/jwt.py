import os

from flask import jsonify
from flask_jwt_extended import JWTManager

from libs.strings import gettext
from blacklist import BLACKLIST


def jwt_properties(app):

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
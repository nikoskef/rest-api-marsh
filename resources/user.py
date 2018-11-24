from flask import request
from flask_restful import Resource
from passlib.hash import pbkdf2_sha512
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from libs.strings import gettext
from libs.admin import admin_required

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"message": gettext("user_username_exists")}, 400

        if UserModel.find_by_email(user.email):
            return {"message": gettext("user_email_exists")}, 400

        user.save_to_db()

        return {"message": gettext("user_created")}, 201


class User(Resource):
    @classmethod
    @admin_required
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return user_schema.dump(user), 200

    @classmethod
    @admin_required
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user.delete_from_db()
        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))

        user = UserModel.find_by_username(user_data.username)

        # this is what the `authenticate()` function did in security.py
        if user and pbkdf2_sha512.verify(user_json['password'], user.password):
            # identity= is what the identity() function did in security.py—now stored in the JWT
            access_token = create_access_token(identity=user.username, fresh=True)
            refresh_token = create_refresh_token(user.username)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": gettext("user_invalid_credentials")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

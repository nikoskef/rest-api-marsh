import re

from marshmallow import post_load, validates_schema, ValidationError, validates, pre_dump
from flask_security.utils import hash_password

from libs.strings import gettext
from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation", "register_on", "active", "roles")

    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confirmation = [user.most_recent_confirmation]
        return user

    @post_load(pass_original=True)
    def hash_password(self, data, original_data):
        password = original_data.get('password')
        data['password'] = hash_password(password)
        return data

    @validates("email")
    def validate_email(self, data):
        email_address_matcher = re.compile("^[a-z]+[\w.-]+@([\w-]+\.)+[\w]+$")
        valid_email = True if email_address_matcher.match(data) else False
        if not valid_email:
            raise ValidationError(gettext("user_email_validation_error"), ['email'])

    @validates_schema
    def validate_password(self, data):
        if len(data['password']) < 8 or len(data['password']) > 30:
            raise ValidationError(gettext("user_password_validation_error"), ["password"])

import re

from marshmallow import post_load, validates_schema, ValidationError, validates
from passlib.hash import pbkdf2_sha512

from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", )

    @post_load(pass_original=True)
    def hash_password(self, data, original_data):
        password = original_data.get('password')
        data['password'] = pbkdf2_sha512.hash(password)
        return data

    @validates("email")
    def validate_email(self, data):
        email_address_matcher = re.compile("^[a-z]+[\w.-]+@([\w-]+\.)+[\w]+$")
        valid_email = True if email_address_matcher.match(data) else False
        if not valid_email:
            raise ValidationError('Invalid Email', 'email')

    @validates_schema
    def validate_password(self, data):
        if len(data['password']) < 8 or len(data['password']) > 30:
            raise ValidationError('Password must be between 8-30 characters', 'password')

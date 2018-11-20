from marshmallow import post_load, validates_schema, ValidationError
from passlib.hash import pbkdf2_sha512

from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)

    @post_load(pass_original=True)
    def hash_password(self, data, original_data):
        password = original_data.get('password')
        data['password'] = pbkdf2_sha512.hash(password)
        return data

    @validates_schema
    def validate_password(self, data):
        if len(data['password']) < 4:
            raise ValidationError('Password must be more than 3 characters', 'password')

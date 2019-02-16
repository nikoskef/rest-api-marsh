from flask import Flask, jsonify, url_for
import os
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
#from flask_uploads import configure_uploads, patch_request_class
from dotenv import load_dotenv
from flask_admin import Admin

from admin.modelview import MyModelView
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers
from flask_security.forms import LoginForm

from wtforms import StringField
from wtforms.validators import InputRequired


from ma import ma
from db import db
from blacklist import BLACKLIST


from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.room import Room, RoomList, RoomCreate
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.category import Category, CategoryList
from resources.company import Company, CompanyList
from models.user import UserModel
from models.company import CompanyModel
from models.room import RoomModel
from models.roles import Role
from models.category import CategoryModel
from models.confirmation import ConfirmationModel

from admin.confirmation import ConfirmationView
from admin.user import UserView
from admin.room import RoomView
from libs.strings import gettext


app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")


class ExtendedLoginForm(LoginForm):
    email = StringField('Username', [InputRequired()])


user_datastore = SQLAlchemyUserDatastore(db, UserModel, Role)
security = Security(app, user_datastore, login_form=ExtendedLoginForm)

api = Api(app)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


@app.before_first_request
def create_tables():
    db.create_all()

    # user_datastore.find_or_create_role(name='superuser', description='Administrator')
    # user_datastore.add_role_to_user(os.environ["ADMINS_EMAIL"], 'superuser')
    #
    # db.session.commit()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)
admin = Admin(
    app,
    name='Admin',
    base_template='my_master.html',
    template_mode='bootstrap3'
)


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
api.add_resource(Company, "/company", "/company/<string:name>")
api.add_resource(CompanyList, "/companies")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/user_confirmation/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")


admin.add_view(UserView(UserModel, db.session))
admin.add_view(RoomView(RoomModel, db.session))
admin.add_view(MyModelView(CategoryModel, db.session))
admin.add_view(ConfirmationView(ConfirmationModel, db.session))
admin.add_view(MyModelView(CompanyModel, db.session))
admin.add_view(MyModelView(Role, db.session))


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)

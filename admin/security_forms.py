from flask import url_for
from flask_admin import Admin
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers
from flask_security.forms import LoginForm
from wtforms import StringField
from wtforms.validators import InputRequired
from models.user import UserModel
from models.roles import Role
from admin.views import admin_add_view


def create_form(db, app):

    class ExtendedLoginForm(LoginForm):
        email = StringField('Username', [InputRequired()])

    user_datastore = SQLAlchemyUserDatastore(db, UserModel, Role)
    security = Security(app, user_datastore, login_form=ExtendedLoginForm)

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    admin = Admin(
        app,
        name='Admin',
        base_template='my_master.html',
        template_mode='bootstrap3'
    )

    admin_add_view(admin, db)

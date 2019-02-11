from admin.modelview import MyModelView
from flask_security.utils import hash_password
from passlib.hash import pbkdf2_sha512


class UserView(MyModelView):
    column_exclude_list = ['password', ]
    column_searchable_list = ['username', 'email']

    def _on_model_change(self, form, model, is_created):
        if not pbkdf2_sha512.identify(model.password):
            model.password = hash_password(model.password)

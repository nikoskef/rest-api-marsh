from admin.modelview import MyModelView
from models.company import CompanyModel
from models.room import RoomModel
from models.category import CategoryModel
from models.confirmation import ConfirmationModel
from models.user import UserModel

from models.roles import Role

from admin.confirmation import ConfirmationView
from admin.user import UserView
from admin.room import RoomView


def admin_add_view(admin, db):
    admin.add_view(UserView(UserModel, db.session))
    admin.add_view(RoomView(RoomModel, db.session))
    admin.add_view(MyModelView(CategoryModel, db.session))
    admin.add_view(ConfirmationView(ConfirmationModel, db.session))
    admin.add_view(MyModelView(CompanyModel, db.session))
    admin.add_view(MyModelView(Role, db.session))

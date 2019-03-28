from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.room import Room, RoomList, RoomCreate
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.category import Category, CategoryList
from resources.company import Company, CompanyList


def add_resource(api):
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
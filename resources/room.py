from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required

from libs.admin import admin_required
from models.company import CompanyModel
from models.room import RoomModel
from models.category import CategoryModel
from schemas.room import RoomSchema
from libs.strings import gettext

room_schema = RoomSchema()
room_list_schema = RoomSchema(many=True)


class Room(Resource):
    @classmethod
    @jwt_required
    def get(cls, _id: int):
        room = RoomModel.find_by_id(_id)
        if room:
            return room_schema.dump(room), 200
        return {"message": gettext("room_not_found")}, 404

    @classmethod
    @admin_required
    def delete(cls, _id: int):
        room = RoomModel.find_by_id(_id)
        if room:
            room.delete_from_db()
            return {"message": gettext("room_deleted")}, 200
        return {"message": gettext("room_not_found")}, 404


class RoomList(Resource):
    @classmethod
    def get(cls):
        return {"rooms": room_list_schema.dump(RoomModel.get_all_rooms())}, 200


class RoomCreate(Resource):
    @classmethod
    @admin_required
    def post(cls):
        room_json = request.get_json()
        print(room_json)
        room = room_schema.load(room_json)

        category = CategoryModel.find_by_id(room_json["category_id"])
        if not category:
            return {"message": gettext("room_error_inserting_no_category")}, 400

        company = CompanyModel.find_by_id(room_json["company_id"])
        if not company:
            return {"message": gettext("room_error_inserting_no_company")}, 400

        room_exist = RoomModel.find_by_name_company(room_json["name"], room_json["company_id"])
        if room_exist:
            return {"message": gettext("room_name_company_exists").format(room_json['name'], room_json['company_id'])}, 400

        try:
            room.save_to_db()
        except:
            return {"message": gettext("room_error_inserting")}, 500

        return {"message": gettext("room_created")}, 201
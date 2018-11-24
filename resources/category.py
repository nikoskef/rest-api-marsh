from flask_restful import Resource
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_claims

from libs.admin import admin_required
from models.category import CategoryModel
from schemas.category import CategorySchema
from libs.strings import gettext

category_schema = CategorySchema()
category_list_schema = CategorySchema(many=True)


class Category(Resource):
    @classmethod
    @jwt_required
    def get(cls, name: str):
        category = CategoryModel.find_by_name(name)
        if category:
            return category_schema.dump(category), 200
        return {"message": gettext("category_not_found")}, 404

    @classmethod
    @admin_required
    def post(cls, name: str):
        if CategoryModel.find_by_name(name):
            return {"message": gettext("category_already_exists").format(name)}, 400

        category = CategoryModel(name=name)
        try:
            category.save_to_db()
        except:
            return {"message": gettext("category_error_inserting")}, 500

        return category_schema.dump(category), 201

    @classmethod
    @admin_required
    def delete(cls, name: str):
        category = CategoryModel.find_by_name(name)
        if category:
            try:
                category.delete_from_db()
                return {"message": gettext("category_deleted")}, 200
            except:
                return{"message": gettext("category_not_empty").format(name)}, 400
        return {"message": gettext("category_not_found")}, 404


class CategoryList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {"categories": category_list_schema.dump(CategoryModel.find_all())}, 200

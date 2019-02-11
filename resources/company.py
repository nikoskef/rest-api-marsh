from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request

from libs.admin import admin_required
from models.company import CompanyModel
from schemas.company import CompanySchema
from libs.strings import gettext

company_schema = CompanySchema()
company_list_schema = CompanySchema(many=True)


class Company(Resource):
    @classmethod
    @jwt_required
    def get(cls, name: str):
        company = CompanyModel.find_by_name(name)
        if company:
            return company_schema.dump(company), 200
        return {"message": gettext("category_not_found")}, 404

    @classmethod
    @admin_required
    def post(cls):
        company_json = request.get_json()
        company = company_schema.load(company_json)

        if CompanyModel.find_by_name(company_json['name']):
            return {"message": gettext("category_already_exists").format(company_json['name'])}, 400

        try:
            company.save_to_db()
        except:
            return {"message": gettext("category_error_inserting")}, 500

        return company_schema.dump(company), 201

    @classmethod
    @admin_required
    def delete(cls, name: str):
        category = CompanyModel.find_by_name(name)
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
        return {"categories": company_list_schema.dump(CompanyModel.find_all())}, 200

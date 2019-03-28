from flask import Flask, jsonify
from flask_restful import Api
from marshmallow import ValidationError
#from flask_uploads import configure_uploads, patch_request_class
from dotenv import load_dotenv

from admin.security_forms import create_form
from libs.jwt import jwt_properties
from ma import ma
from db import db
from resources.resourcers import add_resource


app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")


api = Api(app)


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


jwt_properties(app)
add_resource(api)
create_form(db, app)


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)

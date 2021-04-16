from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy

from shared import db
from database.AlchemyDataBaseModels import UserModel, PetModel
from database.UserDBMethodsAlchemy import UserDBMethodsAlchemy
from database.PetDbMethodsAlchemy import PetDbMethodsAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
db.init_app(app)

user_get_args = reqparse.RequestParser()
user_get_args.add_argument("Username", type=str, help="username of user is required", required=True)
user_get_args.add_argument("Password", type=str, help="password of user is required", required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("Name", type=str, help="Name of user is required", required=True)
user_put_args.add_argument("Username", type=str, help="username of user is required", required=True)
user_put_args.add_argument("Password", type=str, help="password of user is required", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("Name", type=str)
user_update_args.add_argument("Username", type=str, help="username of user is required")
user_update_args.add_argument("Password", type=str, help="password of user is required")
user_update_args.add_argument("New_Password", type=str, help="new password of user is required")

user_resources_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'password': fields.String,
}


class User(Resource):
    user_db_methods = UserDBMethodsAlchemy(db, UserModel)

    @marshal_with(user_resources_fields)
    def get(self):
        args = user_get_args.parse_args()
        result = self.user_db_methods.login(username=args['Username'], password=args['Password'])
        if not result:
            abort(404, message="No password and username match found")
        return result, 200

    @marshal_with(user_resources_fields)
    def put(self):
        args = user_put_args.parse_args()
        result = self.user_db_methods.get_by_username(username=args['Username'])
        if result:
            abort(409, message="Can't use this username")
        args = user_put_args.parse_args()
        user = UserModel(username=args['Username'], password=args['Password'], name=args['Name'])
        self.user_db_methods.put(user)
        return user, 201

    @marshal_with(user_resources_fields)
    def patch(self):
        args = user_update_args.parse_args()
        result = self.user_db_methods.login(username=args['Username'], password=args['Password'])
        if not result:
            abort(404, message="Could not find user, so cannot update")
        if args['Name']:
            result.name = args['Name']
        if args['Password']:
            result.views = args['Password']
        self.user_db_methods.update(result)
        return result, 201


pet_get_args = reqparse.RequestParser()
pet_get_args.add_argument("Name", type=str, help="Name of user is required", required=True)
pet_get_args.add_argument("User_Id", type=int, help="missing user, who is this pet belong to?", required=True)

pet_put_args = reqparse.RequestParser()
pet_put_args.add_argument("Name", type=str, help="Name of user is required", required=True)
pet_put_args.add_argument("Type", type=str, help="type of animal is required", required=True)
pet_put_args.add_argument("User_Id", type=int, help="missing user, who is this pet belong to?", required=True)

pet_update_args = reqparse.RequestParser()
pet_update_args.add_argument("Name", type=str)
pet_update_args.add_argument("Type", type=str, help="type of animal is required")

pet_resources_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String
}


class Pet(Resource):
    pet_db_methods = PetDbMethodsAlchemy(db, PetModel)

    @marshal_with(pet_resources_fields)
    def get(self, pet_id):
        result = self.pet_db_methods.get(pet_id)
        if not result:
            abort(404, message="No pet found with that id")
        return result, 200

    @marshal_with(pet_resources_fields)
    def put(self):
        args = pet_put_args.parse_args()
        name = args["Name"]
        user_id = args["User_Id"]
        result = self.pet_db_methods.get_name_user(name, user_id)
        if result:
            abort(409, message=f"this user already has {name} as pet")
        pet = PetModel(name=name, type=args["Type"], user_id=user_id)
        self.pet_db_methods.put(pet)
        return pet, 201

    @marshal_with(pet_resources_fields)
    def patch(self, pet_id):
        args = pet_update_args.parse_args()
        result = self.pet_db_methods.get(pet_id)
        if not result:
            abort(404, message="Could not find pet, so cannot update")
        if args['Name']:
            result.name = args['Name']
        if args['Type']:
            result.views = args['Type']
        self.pet_db_methods.update(result)
        return result, 201

    def delete(self, id):
        result = self.pet_db_methods.get(id)
        if not result:
            abort(404, message="Could not find pet, so cannot delete")
        self.pet_db_methods.delete(id)
        return 200


class PetsByUser(Resource):
    pet_db_methods = PetDbMethodsAlchemy(db, PetModel)

    @marshal_with(pet_resources_fields)
    def get(self, user_id):
        result = self.pet_db_methods.get_by_userid(user_id)
        return result, 200


api.add_resource(User, "/users/")
api.add_resource(Pet, '/pets/', endpoint="post")
api.add_resource(Pet, '/pets/<id>', endpoint="get,patch,delete")
api.add_resource(PetsByUser, '/pets/user/<user_id>', endpoint="get_userid")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
    # app.run()

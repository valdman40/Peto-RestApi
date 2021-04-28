import flask
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_mysqldb import MySQL
# from flask_sqlalchemy import SQLAlchemy
from mysql.connector import Error

from database.Models import PetModel, UserModel
from shared import db
from database.UserDBMethodsAlchemy import UserDBMethodsAlchemy
from database.PetDbMethodsAlchemy import PetDbMethodsAlchemy

app = Flask(__name__)
api = Api(app)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'petodb'
app.config['MYSQL_HOST'] = '34.90.42.143'
app.config['MYSQL_DB'] = 'petodb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
db.init_app(app)


# this is just for testing:
@app.route('/')
def home():
    return "App Works!!!"


# ~~~~~~~~~~~~~~~~

user_get_args = reqparse.RequestParser()
user_get_args.add_argument("Username", type=str, help="username of user is required", required=True)
user_get_args.add_argument("Password", type=str, help="password of user is required", required=True)

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("Username", type=str, help="username of user is required", required=True)
user_post_args.add_argument("Password", type=str, help="password of user is required", required=True)

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
    user_db_methods = UserDBMethodsAlchemy(mysql)

    # log in
    # @marshal_with(user_resources_fields)
    # def get(self):
    #     args = user_get_args.parse_args()
    #     try:
    #         result = self.user_db_methods.login(username=args['Username'], password=args['Password'])
    #         if not result:
    #             abort(404, message="No password and username match found")
    #         return result, 200
    #     except Error as error:
    #         return abort(404, message=error.msg)

    # log in - Was moved to a post method
    def post(self):
        args = user_get_args.parse_args()
        try:
            result = self.user_db_methods.login(username=args['Username'], password=args['Password'])
            if not result:
                abort(404, message="No password and username match found")
            return result, 200
        except Error as error:
            return abort(404, message=error.msg)

    # add a user
    @marshal_with(user_resources_fields)
    def put(self):
        args = user_put_args.parse_args()
        try:
            result = self.user_db_methods.get_by_username(username=args['Username'])
            if result:
                abort(409, message="Can't use this username")
            # username is valid, so now we need to insert it into our database
            args = user_put_args.parse_args()
            user = UserModel(username=args['Username'], password=args['Password'], name=args['Name'])
            answer = self.user_db_methods.put(user)
            if answer:
                return answer, 200
            else:
                abort(409, message=answer)
        except Error as error:
            return abort(404, message=error.msg)

    # change password, something else?
    @marshal_with(user_resources_fields)
    def patch(self):
        args = user_update_args.parse_args()
        try:
            result = self.user_db_methods.login(username=args['Username'], password=args['Password'])
            if not result:
                abort(404, message="Could not find user, so cannot update")
            # if args['Name'] :
            #     result[0].name = args['Name']
            # update name? no 'new name' field is sent in json
            if args['New_Password']:
                user = UserModel(username=result[0]['username'], id=result[0]['id'])
                # result.views = args['Password']
                result = self.user_db_methods.update(user, args['New_Password'])
                return result, 201
        except Error as error:
            return abort(404, message=error.msg)


pet_get_args = reqparse.RequestParser()
pet_get_args.add_argument("Name", type=str, help="Name of user is required", required=True)
pet_get_args.add_argument("User_Id", type=int, help="missing user, who is this pet belong to?", required=True)

pet_put_args = reqparse.RequestParser()
pet_put_args.add_argument("Name", type=str, help="Name of pet is required", required=True)
pet_put_args.add_argument("Type", type=str, help="type of animal is required", required=True)
pet_put_args.add_argument("User_Id", type=int, help="missing user, who is this pet belong to?", required=True)

pet_update_args = reqparse.RequestParser()
pet_update_args.add_argument("User_Id", type=int, help="missing user, who is this pet belong to?", required=True)
pet_update_args.add_argument("Id", type=int, help="missing pet_id, which pet are you referring to?", required=True)
pet_update_args.add_argument("Name", type=str)
pet_update_args.add_argument("Type", type=str, help="type of animal is required")

pet_delete_args = reqparse.RequestParser()
pet_delete_args.add_argument("Id", type=str, help="Name of user is required", required=True)
pet_delete_args.add_argument("User_Id", type=int, help="missing user, who is this pet belong to?", required=True)
pet_resources_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String,
    'user_id': fields.Integer
}


class Pet(Resource):
    pet_db_methods = PetDbMethodsAlchemy(mysql)

    # Return pet by id
    @marshal_with(pet_resources_fields)
    def get(self, id):
        try:
            result = self.pet_db_methods.get(id)
            if not result:
                abort(404, message="No pet found with that id")
            return result, 200
        except Error as error:
            return abort(404, message=error.msg)

    # add a new pet
    @marshal_with(pet_resources_fields)
    def put(self):
        args = pet_put_args.parse_args()
        name = args["Name"]
        user_id = args["User_Id"]
        # we also need to verify User_ID is in DB
        try:
            result = self.pet_db_methods.get_name_user(name, user_id)
            if result:
                abort(409, message=f"this user already has {name} as pet")
            pet = PetModel(name=name, type=args["Type"], id=user_id, user_id=user_id)
            self.pet_db_methods.put(pet)
            return pet, 201
        except Error as error:
            return abort(404, message=error.msg)

    @marshal_with(pet_resources_fields)
    def patch(self):
        args = pet_update_args.parse_args()
        result = self.pet_db_methods.get(args['Id'])
        try:
            if not result:
                abort(404, message="Could not find pet, so cannot update")
            if args['Name'] and args['Type']:
                return self.pet_db_methods.update_name_and_type(result, args), 201

            elif args['Type']:
                return self.pet_db_methods.update_type(result, args), 201
            elif args['Name']:
                return self.pet_db_methods.update_name(result, args), 201
            else:
                return abort(404, message="no data for modification")
        except Error as error:
            return abort(404, message=error.msg)

    def delete(self):
        args = pet_delete_args.parse_args()
        id = args['Id']
        try:
            result = self.pet_db_methods.get(id)
            if not result:
                abort(404, message="Could not find pet, so cannot delete")
            self.pet_db_methods.delete(id)
            return 200
        except Error as error:
            return abort(404, message=error.msg)


class PetsByUser(Resource):

    ## NOT YET IMPLEMNTED - maybe we should add another table user id,pet id ?
    pet_db_methods = PetDbMethodsAlchemy(db)

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

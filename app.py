from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_mysqldb import MySQL
from mysql.connector import Error
from database.Models import PetModel, UserModel, MealsModel
from shared import db
from database.UserDBMethodsMySQL import UserDBMethodsMySQL
from database.PetDbMethodsMySQL import PetDbMethodsMySQL
from database.MealsDbMethosMySQL import MealsDbMethodsMySQL
import json
import requests

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


user_login_args = reqparse.RequestParser()
user_login_args.add_argument("Username", type=str, help="username of user is required", required=True)
user_login_args.add_argument("Password", type=str, help="password of user is required", required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("Name", type=str, help="Name of user is required", required=True)
user_put_args.add_argument("Username", type=str, help="username of user is required", required=True)
user_put_args.add_argument("Password", type=str, help="password of user is required", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("Name", type=str, help="Name of user is required", required=True)
user_update_args.add_argument("Username", type=str, help="username of user is required", required=True)
user_update_args.add_argument("New_Password", type=str, help="password of user is required", required=True)

user_resources_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'password': fields.String,
}


class User(Resource):
    user_db_methods = UserDBMethodsMySQL(mysql)

    def get(self, id):
        try:
            result = self.user_db_methods.get(id=id)
            if not result:
                abort(404, message="No user by that id")
            return result, 200
        except Error as error:
            return abort(400, message=error.msg)

    # login
    def post(self):
        args = user_login_args.parse_args()
        try:
            result = self.user_db_methods.login(username=args['Username'], password=args['Password'])
            if not result:
                abort(404, message="No password and username match found")
            return result, 200
        except Error as error:
            return abort(400, message=error.msg)

    # add a user
    @marshal_with(user_resources_fields)
    def put(self):
        args = user_put_args.parse_args()
        try:
            result = self.user_db_methods.get_by_username(username=args['Username'])
            if result:
                abort(409, message="Can't use this username")
            # username is valid, so now we need to insert it into our database
            user = UserModel(username=args['Username'], password=args['Password'], name=args['Name'])
            user = self.user_db_methods.put(user)
            if user:
                return user, 200
            else:
                abort(409, message=user)
        except Error as error:
            return abort(404, message=error.msg)

    def patch(self, id):
        args = user_update_args.parse_args()
        try:
            user_with_changes = UserModel(name=args['Name'], username=args['Username'], password=args['New_Password'],
                                          id=id)
            result = self.user_db_methods.update(user_with_changes)
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
# pet_delete_args.add_argument("User_Id", type=int, help="missing user, who is this pet belong to?", required=True)
pet_resources_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String,
    'user_id': fields.Integer
}


class Pet(Resource):
    pet_db_methods = PetDbMethodsMySQL(mysql)

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
        try:
            result = self.pet_db_methods.get_name_user(name, user_id)
            if result:
                abort(409, message=f"this user already has {name} as pet")
            newPet = PetModel(name=name, type=args["Type"], user_id=user_id)
            newPet.id = self.pet_db_methods.put(newPet)
            return newPet, 201
        except Error as error:
            return abort(404, message=error.msg)

    # delete pet by id
    def delete(self, id):
        try:
            pet = self.pet_db_methods.get(id)
            if not pet:
                abort(404, message="Could not find pet, so cannot delete")
            self.pet_db_methods.delete(id)
            return 200
        except Error as error:
            return abort(404, message=error.msg)


meal_delete_args = reqparse.RequestParser()
meal_delete_args.add_argument("Id", type=int, required=True)
meal_resources_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'amount': fields.Integer,
    'time': fields.String,
    'type': fields.String,
    'pet_id': fields.Integer
}


class PetsByUser(Resource):
    pet_db_methods = PetDbMethodsMySQL(mysql)

    def get(self, user_id):
        user_pets = self.pet_db_methods.get_by_userid(user_id)
        return user_pets, 200


# pet_id -> amount in grams to feed
feeding_requests = dict()

pet_feed_args = reqparse.RequestParser()
pet_feed_args.add_argument("Amount", type=int, help="Amount of food in grams is required", required=True)


class PetFeeder(Resource):
    pet_db_methods = PetDbMethodsMySQL(mysql)

    def put(self, id):
        # pet = self.pet_db_methods.get(id)
        args = pet_feed_args.parse_args()
        amount = args["Amount"]
        feeding_requests[id] = amount
        print("feeding_requests", feeding_requests)

    def get(self, id):
        if id in feeding_requests:
            amount: int = feeding_requests[id]
            feeding_requests.pop(id)
            return amount


meal_args = reqparse.RequestParser()
meal_args.add_argument("name", type=str, help="Name is required", required=True)
meal_args.add_argument("amount", type=int, help="Amount of food in grams is required", required=True)
meal_args.add_argument("time", type=str, help="Time is required", required=True)
meal_args.add_argument("repeat_daily", type=bool, help="repeat_daily is required", required=True)


# meal_args.add_argument("name", type=str, help="Name is required")
# meal_args.add_argument("amount", type=int, help="Amount of food in grams is required")
# meal_args.add_argument("time", type=str, help="Time is required")
# meal_args.add_argument("type", type=bool, help="Type is required")


class MealManager(Resource):
    meals_methods = MealsDbMethodsMySQL(mysql)

    # Return meals by pet_id
    def get(self, pet_id):
        try:
            result = self.meals_methods.get_by_pet_id(pet_id)
            if not result:
                abort(404, message="No meals found with that pet_id")
            result = json.loads(json.dumps(result, indent=4, sort_keys=True, default=str))
            return result, 200
        except Error as error:
            return abort(404, message=error.msg)

    def patch(self, id):
        args = meal_args.parse_args()
        try:
            meal_after_changes = MealsModel(name=args['name'], amount=args['amount'], time=args['time'],
                                            repeat_daily=args['repeat_daily'], id=id)
            self.meals_methods.update(meal_after_changes)
            return 201
        except Error as error:
            return abort(404, message=error.msg)

    def put(self, pet_id):
        args = meal_args.parse_args()
        try:
            new_meal = MealsModel(name=args['name'], amount=args['amount'], time=args['time'],
                                  repeat_daily=args['repeat_daily'], pet_id=pet_id)
            meal_id = self.meals_methods.put(new_meal)
            return meal_id, 200
        except Error as error:
            return abort(404, message=error.msg)

    def delete(self, id):
        try:
            pet = self.meals_methods.get(id)
            if not pet:
                abort(404, message="Could not find meal, so cannot delete")
            self.meals_methods.delete(id)
            return 200
        except Error as error:
            return abort(404, message=error.msg)


notification_args = reqparse.RequestParser()
notification_args.add_argument("to")
notification_args.add_argument("title")
notification_args.add_argument("body")

user_notification_args = reqparse.RequestParser()
user_notification_args.add_argument("push_notification_token")


class PushNotification(Resource):
    user_db_methods = UserDBMethodsMySQL(mysql)
    pet_db_methods = PetDbMethodsMySQL(mysql)

    def put(self, pet_id):
        args = notification_args.parse_args()
        url = "https://exp.host/--/api/v2/push/send"
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            result = self.pet_db_methods.get_token(id=pet_id)
            data = {'to': result['push_notification_token'], 'title': args['title'], 'sound': 'default',
                    'body': args['body']}
            requests.post(url, data=json.dumps(data), headers=headers)
            return 200
        except Error as error:
            return abort(404, message=error.msg)

    def patch(self, user_id):
        args = user_notification_args.parse_args()
        try:
            result = self.user_db_methods.update_token(args['push_notification_token'], user_id)
            return result, 200
        except Error as error:
            return abort(404, message=error.msg)


api.add_resource(User, "/users/")
api.add_resource(User, "/users/<id>", endpoint="user_patch")
api.add_resource(Pet, '/pets/', endpoint="pet_post")
api.add_resource(Pet, '/pets/<id>', endpoint="pet_get,patch,delete")
api.add_resource(PetsByUser, '/pets/user/<user_id>')
api.add_resource(PetFeeder, '/pets/feed/<id>')
api.add_resource(MealManager, '/meal/pet/<pet_id>', endpoint="meal_get")
api.add_resource(MealManager, '/meal/<id>', endpoint="meal_patch")
api.add_resource(MealManager, '/meal/pet/<pet_id>', endpoint="meal_put")
api.add_resource(MealManager, '/meal/', endpoint="meal_ delete,insert,get")
api.add_resource(PushNotification, '/push/<pet_id>')
api.add_resource(PushNotification, '/push/<user_id>', endpoint="update_token")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
    # app.run()

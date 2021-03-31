from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

from shared import db
from database.AlchemyDataBaseModels import UserModel
from database.UserDBMethodsAlchemy import UserDBMethodsAlchemy

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
user_update_args.add_argument("name", type=str, help="Name of user is required")
user_update_args.add_argument("username", type=str, help="username of user is required")
user_update_args.add_argument("password", type=str, help="password of user is required")

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
        print(args)
        result = self.user_db_methods.get(username=args['Username'], password=args['Password'])
        if not result:
            abort(404, message="No password and username match found")
        return result, 200

    @marshal_with(user_resources_fields)
    def put(self):
        args = user_put_args.parse_args()
        result = self.user_db_methods.get(username=args['Username'], password=args['Password'])
        if result:
            abort(409, message="Can't use this username")
        args = user_put_args.parse_args()
        user = UserModel(username=args['Username'], password=args['Password'], name=args['Name'])
        self.user_db_methods.put(user)
        return user, 201

    # @marshal_with(user_resources_fields)
    # def patch(self, video_id):
    #     result = self.user_db_methods.get(video_id=video_id)
    #     if not result:
    #         abort(404, message="could not find video with that id, so cannot update")
    #     args = user_update_args.parse_args()
    #     if args['name']:
    #         result.name = args['name']
    #     if args['views']:
    #         result.views = args['views']
    #     if args['likes']:
    #         result.views = args['likes']
    #     self.user_db_methods.update(result)
    #     return result, 201


api.add_resource(User, "/users")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
    # app.run()

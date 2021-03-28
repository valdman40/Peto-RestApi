from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

from shared import db
from database.AlchemyDataBaseModels import VideoModel
from database.VideoDBMethodsAlchemy import VideoDBMethodsAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
db.init_app(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of video is required", required=True)

video_resources_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
}


class Video(Resource):
    video_db_methods = VideoDBMethodsAlchemy(db, VideoModel)

    @marshal_with(video_resources_fields)
    def get(self, video_id):
        result = self.video_db_methods.get(video_id=video_id)
        if not result:
            abort(404, message="could not find video with that id")
        return result, 200

    @marshal_with(video_resources_fields)
    def put(self, video_id):
        result = self.video_db_methods.get(video_id=video_id)
        if result:
            abort(409, message="video with that id already exist")
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        self.video_db_methods.put(video)
        return video, 201


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)

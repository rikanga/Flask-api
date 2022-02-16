from os import name
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Jesus is lord'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help="Name of video is required", required=True)
video_put_args.add_argument('views', type=int, help="Views of video is required", required=True)
video_put_args.add_argument('likes', type=int, help="Likes on video is required", required=True)

video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument('name', type=str, help="Name of video")
video_patch_args.add_argument('likes', type=int, help="likes of video")
video_patch_args.add_argument('views', type=int, help="views on video")

videos = {}

def abort_video_not_found(video_id):
    if video_id not in videos:
        abort(404, message="Video not find ...")

def abort_video_exit(video_id):
    if video_id in videos:
        abort(407, message="Video already exist whith that ID...")

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views  = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'name = {self.name}, views = {self.views}, likes = {self.likes}'

#db.create_all()

resource_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
}

class Videos(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=int(video_id)).first()
        if not result:
            abort(404, message='Could not find video id. Try others please...')
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        video_exist = VideoModel.query.filter_by(id=int(video_id)).first()
        if video_exist is not None:
            abort(409, message="Video already taken...")
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], likes=args['likes'], views=args['views'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        result = VideoModel.query.filter_by(id=int(video_id)).first()
        args = video_patch_args.parse_args()
        if not result:
            abort(404, message="Could not find video with that id ...")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        #db.session.add(result)
        db.session.commit()
        
        return result
    
    def delete(self, video_id):
        abort_video_not_found(video_id)
        del videos[video_id]
        return '', 204

api.add_resource(Videos, "/video/<int:video_id>")
#api.add_resource(HelloWorld, "/name/<string:name>")

#print(videos)
if __name__ == '__main__':
    app.run(debug=True)
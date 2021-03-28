from database.VideoDBMethodsAbstract import VideoDBMethodsAbstract


class VideoDBMethodsAlchemy(VideoDBMethodsAbstract):
    def __init__(self, db, model):
        super().__init__(db, model)
        self.db = db
        self.model = model

    def get(self, video_id):
        return self.model.query.filter_by(id=video_id).first()

    def put(self, video):
        self.db.session.add(video)
        self.db.session.commit()
        pass

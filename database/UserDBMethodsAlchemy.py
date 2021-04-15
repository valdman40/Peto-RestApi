from database.IUserDbMethods import IUserDbMethods


class UserDBMethodsAlchemy(IUserDbMethods):

    def __init__(self, db, model):
        super().__init__(db, model)
        self.db = db
        self.model = model

    def login(self, username, password):
        return self.model.query.filter_by(username=username, password=password).first()

    def get_by_username(self, username):
        return self.model.query.filter_by(username=username).first()

    def put(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def update(self, user):
        local_object = self.db.session.merge(user)
        self.db.session.add(local_object)
        self.db.session.commit()

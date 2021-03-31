from database.UserDBMethodsAbstract import UserDBMethodsAbstract


class UserDBMethodsAlchemy(UserDBMethodsAbstract):
    def __init__(self, db, model):
        super().__init__(db, model)
        self.db = db
        self.model = model

    def get(self, username, password):
        return self.model.query.filter_by(username=username, password=password).first()

    def put(self, user):
        self.db.session.add(user)
        self.db.session.commit()
        pass

    def update(self, user):
        self.db.session.commit()
        pass

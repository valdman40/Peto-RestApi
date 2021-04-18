from database.IPetDbMethods import IPetDbMethods


class PetDbMethodsAlchemy(IPetDbMethods):

    def __init__(self, db):
        super().__init__(db)
        self.session = db

    def get(self, id):
        pass
        #return self.model.query.filter_by(id=id).first()

    def get_name_user(self, name, user_id):
        pass
        #return self.model.query.filter_by(name=name, user_id=user_id).first()

    def get_by_userid(self, user_id):
        pass
        #return self.model.query.filter_by(user_id=user_id).all()

    def put(self, pet):
        pass
        # self.db.session.add(pet)
        # self.db.session.commit()

    def update(self, pet):
        pass
        # local_object = self.db.session.merge(pet)
        # self.db.session.add(local_object)
        # self.db.session.commit()

    def delete(self, id):
        pass
        # self.model.query.filter_by(id=id).delete()
        # self.db.session.commit()

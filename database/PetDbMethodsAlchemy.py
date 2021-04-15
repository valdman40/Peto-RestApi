from database.IPetDbMethods import IPetDbMethods


class PetDbMethodsAlchemy(IPetDbMethods):

    def __init__(self, db, model):
        super().__init__(db, model)
        self.db = db
        self.model = model

    def get(self, id):
        return self.model.query.filter_by(id=id).first()

    def get_name_user(self, name, user_id):
        return self.model.query.filter_by(name=name, user_id=user_id).first()

    def put(self, pet):
        self.db.session.add(pet)
        self.db.session.commit()

    def update(self, pet):
        local_object = self.db.session.merge(pet)
        self.db.session.add(local_object)
        self.db.session.commit()

    def delete(self, id):
        self.model.query.filter_by(id=id).delete()
        self.db.session.commit()

from database.IPetDbMethods import IPetDbMethods
from mysql.connector import Error

class PetDbMethodsAlchemy(IPetDbMethods):

    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def get(self, id):
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT * FROM petodb.pets WHERE id = %s", (id,))
            answer = cursor.fetchall()
            return answer


    def get_name_user(self, name, user_id):
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT * FROM petodb.pets WHERE name = %s AND user_id = %s", (name,user_id))
            answer = cursor.fetchall()
            return answer
        #return self.model.query.filter_by(name=name, user_id=user_id).first()

    def get_by_userid(self, user_id):
        pass
        #return self.model.query.filter_by(user_id=user_id).all()

    def put(self, pet):
        cursor = self.db.connection.cursor()
        cursor.execute("INSERT INTO `petodb`.`pets` (`id`, `name`, `type`, `user_id`) VALUES (%s, %s, %s,%s);",(pet.id,pet.name,pet.type,pet.user_id))
        self.db.connection.commit()
        answer = self.get(pet.id)
        return answer

    def update(self, pet):
        pass
        # local_object = self.db.session.merge(pet)
        # self.db.session.add(local_object)
        # self.db.session.commit()

    def delete(self, id):
        pass
        # self.model.query.filter_by(id=id).delete()
        # self.db.session.commit()

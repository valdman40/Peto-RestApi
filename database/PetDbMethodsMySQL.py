from database.IPetDbMethods import IPetDbMethods
from mysql.connector import Error

from database.Models import PetModel


def is_valid_str(name):
    return True


def is_valid_type(type):
    return True


class PetDbMethodsMySQL(IPetDbMethods):

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
        cursor.execute("SELECT * FROM petodb.pets WHERE name = %s AND user_id = %s", (name, user_id))
        answer = cursor.fetchall()
        return answer

    # return self.model.query.filter_by(name=name, user_id=user_id).first()

    def get_by_userid(self, user_id):
        pass
        # return self.model.query.filter_by(user_id=user_id).all()

    def put(self, pet):
        cursor = self.db.connection.cursor()
        cursor.execute("INSERT INTO `petodb`.`pets` (`id`, `name`, `type`, `user_id`) VALUES (%s, %s,%s);",
                       (pet.name, pet.type, pet.user_id))
        self.db.connection.commit()
        answer = self.get(pet.id)
        return answer

    # def update(self, old_pet_data, new_pet_data):
    #     old_pet = PetModel(id=old_pet_data[0]['id'], name=old_pet_data[0]['name'],
    #                        type=old_pet_data[0]['type'], user_id=old_pet_data[0]['user_id'])
    #     new_pet = PetModel(name=new_pet_data['Name'], type=new_pet_data['Type'],
    #                        id=old_pet_data[0]['id'], user_id=old_pet_data[0]['user_id'])
    #     valid_name = is_valid_str(new_pet.name)
    #     valid_type = is_valid_type(new_pet.type)
    #     if valid_name and valid_type:
    #         if old_pet.name != new_pet.name and old_pet.type != new_pet.type:
    #             # change name and type
    #             cursor = self.db.connection.cursor()
    #             cursor.execute("UPDATE `petodb`.`pets` SET `name` = %s, `type` = %s WHERE (`id` = %s);",
    #                            (new_pet.name, new_pet.type, new_pet.id,))
    #             self.db.connection.commit()
    #             return self.get(new_pet_data.id)
    #         elif old_pet.name != new_pet.name:
    #             # change name
    #             cursor = self.db.connection.cursor()
    #             cursor.execute("UPDATE `petodb`.`pets` SET `name` = %s, `type` = %s WHERE (`id` = %s);",
    #                            (new_pet.name, new_pet.id,))
    #             self.db.connection.commit()
    #             return self.get(new_pet_data.id)
    #         else:
    #         # change Type
    #         cursor = self.db.connection.cursor()
    #         cursor.execute("UPDATE `petodb`.`pets` SET `type` = %s WHERE (`id` = %s);",
    #                        (new_pet.type, new_pet.id,))
    #         self.db.connection.commit()
    #         return self.get(new_pet_data.id)
    #     else:
    #         raise Error(msg="type or name is not valid")
    #
    #     # local_object = self.db.session.merge(pet)
    #     # self.db.session.add(local_object)
    #     # self.db.session.commit()

    def delete(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM `petodb`.`pets` WHERE (`id` = %s);",
                       (id,))
        self.db.connection.commit()
        pass
        # self.model.query.filter_by(id=id).delete()
        # self.db.session.commit()

    def update_name_and_type(self, old_pet_data, new_pet_data):
        new_pet = PetModel(name=new_pet_data['Name'], type=new_pet_data['Type'],
                           id=old_pet_data[0]['id'], user_id=old_pet_data[0]['user_id'])
        valid_name = is_valid_str(new_pet.name)
        valid_type = is_valid_type(new_pet.type)
        if valid_name and valid_type:
            cursor = self.db.connection.cursor()
            cursor.execute("UPDATE `petodb`.`pets` SET `name` = %s, `type` = %s WHERE (`id` = %s);",
                           (new_pet.name, new_pet.type, new_pet.id,))
            self.db.connection.commit()
            return self.get(new_pet.id)

    def update_name(self, old_pet_data, new_pet_data):
        new_pet = PetModel(name=new_pet_data['Name'], type=new_pet_data['Type'],
                           id=old_pet_data[0]['id'], user_id=old_pet_data[0]['user_id'])
        valid_name = is_valid_str(new_pet.name)
        if valid_name:
            cursor = self.db.connection.cursor()
            cursor.execute("UPDATE `petodb`.`pets` SET `name` = %s WHERE (`id` = %s);",
                           (new_pet.name, new_pet.id,))
            self.db.connection.commit()
            return self.get(new_pet.id)

    def update_type(self, old_pet_data, new_pet_data):
        new_pet = PetModel(name=new_pet_data['Name'], type=new_pet_data['Type'],
                           id=old_pet_data[0]['id'], user_id=old_pet_data[0]['user_id'])
        valid_name = is_valid_str(new_pet.name)
        if valid_name:
            cursor = self.db.connection.cursor()
            cursor.execute("UPDATE `petodb`.`pets` SET `type` = %s WHERE (`id` = %s);",
                           (new_pet.type, new_pet.id,))
            self.db.connection.commit()
            return self.get(new_pet.id)

from database.IPetDbMethods import IPetDbMethods
from mysql.connector import Error

from database.Models import PetModel


class PetDbMethodsMySQL(IPetDbMethods):

    def update_name(self, pet):
        pass

    def update_name_and_type(self, pet):
        pass

    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def get(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.pets WHERE id = %s", [id])
        pet = cursor.fetchone()
        return pet

    def get_name_user(self, name, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.pets WHERE name = %s AND user_id = %s", [name, user_id])
        pet = cursor.fetchone()
        return pet

    def get_by_userid(self, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.pets WHERE user_id = %s", [user_id])
        pets = cursor.fetchall()
        return pets

    def put(self, pet):
        cursor = self.db.connection.cursor()
        pet: PetModel = cursor.execute("INSERT INTO petodb.pets (name, type, user_id) VALUES (%s, %s, %s)",
                                       [pet.name, pet.daily_repeat, pet.user_id])
        self.db.connection.commit()
        # we return the id that was inserted
        return cursor.lastrowid

    def delete(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM petodb.pets WHERE id = %s;", [id])
        self.db.connection.commit()

    # def update_name_and_type(self, old_pet_data, new_pet_data):
    #     new_pet = PetModel(name=new_pet_data['Name'], type=new_pet_data['Type'],
    #                        id=old_pet_data[0]['id'], user_id=old_pet_data[0]['user_id'])
    #     valid_name = is_valid_str(new_pet.name)
    #     valid_type = is_valid_type(new_pet.type)
    #     if valid_name and valid_type:
    #         cursor = self.db.connection.cursor()
    #         cursor.execute("UPDATE `petodb`.`pets` SET `name` = %s, `type` = %s WHERE (`id` = %s);",
    #                        (new_pet.name, new_pet.type, new_pet.id,))
    #         self.db.connection.commit()
    #         return self.get(new_pet.id)
    #
    # def update_name(self, old_pet_data, new_pet_data):
    #     new_pet = PetModel(name=new_pet_data['Name'], type=new_pet_data['Type'],
    #                        id=old_pet_data[0]['id'], user_id=old_pet_data[0]['user_id'])
    #     valid_name = is_valid_str(new_pet.name)
    #     if valid_name:
    #         cursor = self.db.connection.cursor()
    #         cursor.execute("UPDATE `petodb`.`pets` SET `name` = %s WHERE (`id` = %s);",
    #                        (new_pet.name, new_pet.id,))
    #         self.db.connection.commit()
    #         return self.get(new_pet.id)
    #
    # def update_type(self, old_pet_data, new_pet_data):
    #     new_pet = PetModel(name=new_pet_data['Name'], type=new_pet_data['Type'],
    #                        id=old_pet_data[0]['id'], user_id=old_pet_data[0]['user_id'])
    #     valid_name = is_valid_str(new_pet.name)
    #     if valid_name:
    #         cursor = self.db.connection.cursor()
    #         cursor.execute("UPDATE `petodb`.`pets` SET `type` = %s WHERE (`id` = %s);",
    #                        (new_pet.type, new_pet.id,))
    #         self.db.connection.commit()
    #         return self.get(new_pet.id)

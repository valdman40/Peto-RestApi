from database.IPetDbMethods import IPetDbMethods
from mysql.connector import Error

from database.Models import PetModel


class PetDbMethodsMySQL(IPetDbMethods):
    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def get(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.pets WHERE id = %s", [id])
        pet = cursor.fetchone()
        return pet

    def get_token(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT push_notification_token FROM (Select user_id from petodb.pets where id = %s) as k " +
                       "LEFT JOIN petodb.users ON users.id = k.user_id;", [id])
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
        pet: PetModel = cursor.execute(
            "INSERT INTO petodb.pets (name, type, user_id, machine_id) VALUES (%s, %s,%s, %s)",
            [pet.name, pet.type, pet.user_id, pet.machine_id])
        self.db.connection.commit()
        # we return the id that was inserted
        return cursor.lastrowid

    def delete(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM petodb.pets WHERE id = %s;", [id])
        self.db.connection.commit()

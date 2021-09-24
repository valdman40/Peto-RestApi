from database.IMealsHistoryMethods import IMealsHistoryMethods
from mysql.connector import Error


class MealsHistoryDbMethodsMySQL(IMealsHistoryMethods):
    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def get_by_pet_id(self, pet_id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.meals_history WHERE pet_id = %s", [pet_id])
        meals = cursor.fetchall()
        return meals

    def get(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.meals_history WHERE id = %s", [id])
        pet = cursor.fetchone()
        return pet

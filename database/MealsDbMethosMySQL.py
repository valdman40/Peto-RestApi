from database.IMealsMethods import IMealsMethods
from mysql.connector import Error

from database.Models import MealsModel


class MealsDbMethodsMySQL(IMealsMethods):

    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def update(self, meal: MealsModel):
        cursor = self.db.connection.cursor()
        cursor.execute("UPDATE meals SET name = %s, amount = %s, time= %s WHERE id = %s"
                       , [meal.name, meal.amount, meal.time, meal.id])
        self.db.connection.commit()
        return meal

    def get_by_pet_id(self, pet_id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.meals WHERE pet_id = %s", [pet_id])
        meals = cursor.fetchall()
        return meals

    def get(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.meals WHERE pet_id = %s", [id])
        pet = cursor.fetchone()
        return pet

    def put(self, meal):
        cursor = self.db.connection.cursor()
        meal: MealsModel = cursor.execute(
            "INSERT INTO petodb.meals (name, amount,time, repeat_daily, pet_id) VALUES (%s, %s, %s,%s, %s)",
            [meal.name, meal.amount, meal.time, meal.daily_repeat, meal.pet_id])
        self.db.connection.commit()
        return cursor.lastrowid

    def delete(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM petodb.feedingSchedules WHERE id = %s;", [id])
        self.db.connection.commit()

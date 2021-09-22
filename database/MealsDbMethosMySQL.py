from database.IMealsMethods import IMealsMethods
from mysql.connector import Error

from database.Models import MealsModel, MealSummaryModel


class MealsDbMethodsMySQL(IMealsMethods):

    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def update(self, meal: MealsModel):
        cursor = self.db.connection.cursor()
        cursor.execute("UPDATE meals SET name = %s, amount = %s, time= %s, repeat_daily= %s WHERE id = %s"
                       , [meal.name, meal.amount, meal.time, meal.repeat_daily, meal.id])
        self.db.connection.commit()
        return meal

    def get_by_pet_id(self, pet_id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.meals WHERE pet_id = %s", [pet_id])
        meals = cursor.fetchall()
        return meals

    def get(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.meals WHERE id = %s", [id])
        pet = cursor.fetchone()
        return pet

    def put(self, meal):
        cursor = self.db.connection.cursor()
        meal: MealsModel = cursor.execute(
            "INSERT INTO petodb.meals (name, amount,time, repeat_daily, pet_id) VALUES (%s, %s, %s,%s, %s)",
            [meal.name, meal.amount, meal.time, meal.repeat_daily, meal.pet_id])
        self.db.connection.commit()
        return cursor.lastrowid

    def delete(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("DELETE FROM petodb.meals WHERE id = %s;", [id])
        self.db.connection.commit()

    def insertPostMeal(self, pet_id, meal):
        cursor = self.db.connection.cursor()
        meal: MealSummaryModel = cursor.execute(
            "INSERT INTO petodb.meals_history (pet_id, name,time, pet_started_eating,pet_finished_eating,amount_given,amount_eaten) VALUES (%s, %s, %s,%s, %s,%s,%s)",
            [pet_id, meal.name, meal.mealTime, meal.petStartedEating, meal.petFinishedEating, meal.amountGiven,
             meal.amountEaten])
        self.db.connection.commit()
        # return cursor.lastrowid

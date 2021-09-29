from database.IPetHelathRateMethods import IPetHelathRateMethods
from mysql.connector import Error
from datetime import datetime

from database.Models import PetHealthModel
from flask_mysqldb import MySQL


class PetHealthRateDbMethodsMySQL(IPetHelathRateMethods):
    def __init__(self, db):
        super().__init__(db)
        self.db: MySQL = db

    def put(self, pet_health):
        cursor = self.db.connection.cursor()
        pet_health: PetHealthModel = cursor.execute(
            "INSERT INTO petodb.pet_rating_health (rate, pet_id, date) VALUES (%s, %s,%s)",
            [pet_health.rate, pet_health.pet_id, pet_health.date])
        self.db.connection.commit()
        # we return the id that was inserted
        return cursor.lastrowid

    def get_today(self, pet_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT * FROM petodb.pet_rating_health WHERE pet_id = %s and date(date) = CURDATE()", [pet_id])
        pet_health = cursor.fetchone()
        return pet_health

    def update(self, pet_health: PetHealthModel):
        cursor = self.db.connection.cursor()
        cursor.execute("UPDATE pet_rating_health SET rate = %s WHERE id = %s", [pet_health['rate'], pet_health['id']])
        self.db.connection.commit()
        return pet_health

    def get(self, pet_id):
        cursor = self.db.connection.cursor()
        query = "Select a.pet_id, amount_given, amount_eaten, a.date, coalesce(rate, 5) as rate from " \
                "(SELECT SUM(amount_given) as amount_given,SUM(amount_eaten) as amount_eaten, Date(time) as date, " \
                f"pet_id FROM petodb.meals_history where pet_id = {pet_id} group by date, pet_id) as a " \
                "left join " \
                f"(Select * from petodb.pet_rating_health where pet_id = {pet_id}) as b " \
                "on a.date = b.date order by pet_id, a.date"
        cursor.execute(query)
        graph = cursor.fetchall()
        return graph

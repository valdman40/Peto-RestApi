from database.IMachineMethods import IMachineMethods
from mysql.connector import Error


class MachineDbMethodsMySQL(IMachineMethods):
    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def get(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM petodb.machines WHERE id = %s", [id])
        machine = cursor.fetchone()
        return machine

    def update(self, id, pet_id):
        cursor = self.db.connection.cursor()
        cursor.execute("UPDATE machines SET pet_id = %s WHERE id = %s", [pet_id, id])
        self.db.connection.commit()
        return pet_id

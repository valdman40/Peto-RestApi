from database.IUserDbMethods import IUserDbMethods
from mysql.connector import Error
from database.Models import UserModel


class UserDBMethodsMySQL(IUserDbMethods):

    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def get(self, id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (id))
        user = cursor.fetchone()
        return user

    def login(self, username, password):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s and password = %s", (username, password))
        user = cursor.fetchone()
        return user

    def get_by_username(self, username):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        return user

    def put(self, user: UserModel):
        cursor = self.db.connection.cursor()
        cursor.execute("INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
                       (user.name, user.username, user.password,))
        self.db.connection.commit()
        return user

    # def update(self, user: UserModel):
    #     try:
    #         cursor = self.db.connection.cursor()
    #         cursor.execute("UPDATE Users SET password = %s, username = %s WHERE (id = %s);"
    #                        , (user.password, user.username, user.id,))
    #         self.db.connection.commit()
    #         return user
    #     except Error as error:
    #         return error
    def update(self, user: UserModel):
        cursor = self.db.connection.cursor()
        cursor.execute("UPDATE users SET password = %s, username = %s, name= %s WHERE id = %s"
                       , [user.password, user.username, user.name, user.id])
        self.db.connection.commit()
        return user

    def update_token(self, token, id):
        cursor = self.db.connection.cursor()
        cursor.execute("UPDATE users SET push_notification_token = %s WHERE id = %s", [token, id])
        self.db.connection.commit()

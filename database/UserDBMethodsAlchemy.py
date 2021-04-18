from database.IUserDbMethods import IUserDbMethods
from mysql.connector import Error


class UserDBMethodsAlchemy(IUserDbMethods):

    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def login(self, username, password):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s and password = %s", (username, password))
        answer = cursor.fetchall()
        return answer

        # return self.model.query.filter_by(username=username, password=password).first()

    def get_by_username(self, username):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        answer = cursor.fetchall()
        return answer
        # return self.model.query.filter_by(username=username).first()

    def put(self, username, password, name):
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
                           (name, username, password,))
            self.db.connection.commit()
            return cursor.lastrowid
        except Error as error:
            return error




    def update(self, user):
        local_object = self.db.session.merge(user)
        self.db.session.add(local_object)
        self.db.session.commit()

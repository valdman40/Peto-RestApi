# this class creates db with tables
# notice! if you activate it (db.create_all()) it will recreate all

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class UserModel(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User(name= {self.name}, username= {self.username},password= {self.password})"


class PetModel(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.INTEGER, nullable=False)

    def __repr__(self):
        return f"Pet(name= {self.name}, type= {self.type}, user_id= {self.user_id})"


db.create_all()

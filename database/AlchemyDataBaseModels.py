# this class creates db with tables
# notice! if you activate it (db.create_all()) it will recreate all

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.INTEGER, nullable=False)
    likes = db.Column(db.INTEGER, nullable=False)

    def __repr__(self):
        return f"Video(name= {self.name}, view= {self.views}, likes= {self.likes})"


db.create_all()

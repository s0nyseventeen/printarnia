from src import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    email = db.Column(db.String(256))
    password = db.Column(db.String(256))

from src import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256))

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, email={self.email})>'

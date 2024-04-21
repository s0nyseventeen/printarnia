from src import db


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True, nullable=False)
    created = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    images = db.relationship(
        'Image', backref='work', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Work(id={self.id}, title={self.title}, created={self.created})>'


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.Text)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))

    def __repr__(self):
        return f'<Image(id={self.id}, title={self.title}, work_id={self.work_id})>'

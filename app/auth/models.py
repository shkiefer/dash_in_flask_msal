from flask_login import UserMixin
from app import db, lm


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)




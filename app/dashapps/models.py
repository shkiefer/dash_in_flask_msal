from app import db


class User_Image(db.Model):
    __bind_key__ = 'my_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    creator = db.Column(db.String(64), nullable=False, unique=False)
    img_web_url = db.Column(db.String(64), nullable=False, unique=True)
    img_dir_url = db.Column(db.String(64), nullable=False, unique=True)
    thumb = db.Column(db.LargeBinary(), nullable=False, unique=False)

    def __repr__(self):
        return '<Image {}>'.format(self.name)


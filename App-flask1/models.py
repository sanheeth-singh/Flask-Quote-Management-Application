from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    user = db.Column(db.String(150) ,unique=True, nullable=False )
    email = db.Column(db.String(150) ,unique=True, nullable=True )
    password = db.Column(db.String(150) ,unique=True, nullable=False )
    quote = db.relationship("Quotes", backref='author', lazy=True)
    bio = db.Column(db.Text, nullable=True)

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') ,nullable=False)

# class Userprofile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     bio = db.Column(db.Text, nullable=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_userprofile_user_id') , nullable=False)


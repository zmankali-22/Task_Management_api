from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 

    projects = db.relationship('Project', back_populates='user', cascade = 'all, delete')   

class UserSchema(ma.Schema):

    projects = fields.List(fields.Nested('ProjectSchema', exclude = ['user']))
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','is_admin', 'projects')


user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])

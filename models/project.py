from init import db, ma
from marshmallow import fields
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='projects') 



class ProjectSchema(ma.Schema):
    user = fields.Nested('UserSchema', only = ['username', 'email'])
    class Meta:
        fields = ('id', 'project_name', 'description','date', 'user')
        ordered = True
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
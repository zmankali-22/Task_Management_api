from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

from init import db, ma

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='projects') 
    tasks = db.relationship('Task', back_populates='project', cascade='all, delete')
   



class ProjectSchema(ma.Schema):

    project_name = fields.String(required=True, validate=And(
        Length(min=2, error="Project name must be at least 2 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$', error="Project name can only contain alphanumeric characters and spaces")
    ))

    user = fields.Nested('UserSchema', only = ['username', 'email'])
    tasks = fields.Nested('TaskSchema',many =True,only = ['id','task_name', 'description'], exclude=['project', 'user'])
   
    class Meta:
        fields = ('id', 'project_name', 'description','date', 'user','tasks')
        ordered = True
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

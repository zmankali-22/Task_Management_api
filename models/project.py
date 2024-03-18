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
    tasks = db.relationship('Task', back_populates='project')
    comments = db.relationship('Comment', back_populates='project')
   



class ProjectSchema(ma.Schema):
    user = fields.Nested('UserSchema', only = ['username', 'email'])
    tasks = fields.Nested('TaskSchema',many =True,only = ['id','task_name', 'description'], exclude=['project', 'user'])
    comments = fields.Nested('CommentSchema', many=True, only=['id', 'message'], exclude=['project', 'user','task']) 
   
    class Meta:
        fields = ('id', 'project_name', 'description','date', 'user','tasks')
        ordered = True
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
from init import db, ma
from marshmallow import fields

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String)
    priority = db.Column(db.String)
    date = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='tasks')
    project = db.relationship('Project', back_populates='tasks')
    comments = db.relationship('Comment', back_populates='task', cascade='all, delete')

class TaskSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username', 'email'])
    project = fields.Nested('ProjectSchema', only=['id','project_name', 'description'])
    comments = fields.Nested('CommentSchema', many=True, only=['id', 'message'])
    class Meta:
        fields = ('id', 'task_name', 'description', 'status', 'priority', 'date', 'project', 'user', 'comments')
        ordered = True

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
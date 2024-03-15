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

    project = db.relationship('Project', back_populates='tasks')

class TaskSchema(ma.Schema):

    project = fields.Nested('ProjectSchema', only = ['project_name', 'description'])

    class Meta:
        fields = ('id', 'task_name', 'description','status', 'priority', 'date', 'project')
        ordered = True


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf 
from marshmallow.exceptions import ValidationError


VALID_STATUSES = ['Open', 'In Progress','Testing',  'Done', 'Closed']
VALID_PRIORITIES = ['High', 'Medium', 'Low']

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

    task_name = fields.String(required=True, validate=And(
        Length(min=2, error="Project name must be at least 2 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$', error="Task name can only contain alphanumeric characters and spaces")
    ))

    status = fields.String(validate=OneOf(VALID_STATUSES))
    priority = fields.String(validate=OneOf(VALID_PRIORITIES))

    # There can only be one task with in progress'
    @validates('status')
    def validate_status(self, value):
        if value == VALID_STATUSES[1]:
            stmt = db.select(db.func.count()).select_from(Task).filter_by(status= VALID_STATUSES[1])
            count = db.session.scalar(stmt)

            if count > 0:
                raise ValidationError('There can only be one task with in progress')




    user = fields.Nested('UserSchema', only=['username', 'email'])
    project = fields.Nested('ProjectSchema', only=['id','project_name', 'description'])
    comments = fields.Nested('CommentSchema', many=True, only=['id', 'message'])
    class Meta:
        fields = ('id', 'task_name', 'description', 'status', 'priority', 'date', 'project', 'user', 'comments')
        ordered = True

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
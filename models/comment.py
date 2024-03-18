from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    project = db.relationship('Project', back_populates='comments')
    task = db.relationship('Task', back_populates='comments')

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username', 'email'])
    project = fields.Nested('ProjectSchema', only=['id', 'project_name', 'description'])
    task = fields.Nested('TaskSchema', only=['id', 'task_name', 'description'])

    class Meta:
        fields = ('id', 'message', 'user', 'project', 'task')
        ordered = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
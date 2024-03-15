from init import db, ma
from marshmallow import fields
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='projects') 



    class ProjectSchema(ma.Schema):

        class Meta:
            fields = ('id', 'project_name', 'description','start_date', 'end_date', 'user')

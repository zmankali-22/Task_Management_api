from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.project import Project
from models.task import Task, task_schema

tasks_bp = Blueprint('tasks', __name__, url_prefix='/<int:project_id>/tasks')


@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(project_id):

    # data we get from  the body of the request
    body_data = request.get_json()
    stmt = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(stmt)
    if project:
        task = Task(
            message=body_data.get('message'),
            user_id=get_jwt_identity(),
            project=project
        )
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task), 201
    else:
        return {'error': f"project with {project_id} not found"}, 404
    
# delete a comment
    

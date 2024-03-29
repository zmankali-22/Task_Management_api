
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

from init import db
from models.project import Project
from models.task import Task, task_schema, tasks_schema
from controllers.authorise_as_admin import authorise_as_admin
from controllers.comment_controller import comments_bp



tasks_bp = Blueprint('tasks', __name__, url_prefix='/<int:project_id>/tasks')
tasks_bp.register_blueprint(comments_bp)



#get all tasks for a project
@tasks_bp.route('/', methods=['GET'])
def get_tasks(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': f'Project with id {project_id} not found'}), 404

    stmt = db.select(Task).filter_by(project_id=project_id)
    tasks = db.session.scalars(stmt)
    return tasks_schema.dump(tasks), 200

# get a single task of a project


@tasks_bp.route('/<int:task_id>')
def get_task(project_id, task_id):
    # Check if the project exists first
    project = Project.query.get(project_id)
    if not project:
        return {'error': f'Project with id {project_id} not found'}, 404

    # Query the task associated with the project
    stmt = db.select(Task).filter_by(id=task_id, project_id=project_id)
    task = db.session.scalar(stmt)
    
    if task:
        return task_schema.dump(task), 200
    else:
        return {'error': f'Task {task_id} not found in project {project_id}'}, 404
    

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task(project_id):

    # data we get from  the body of the request
    body_data = task_schema.load(request.get_json())
    stmt = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(stmt)
    if project:
        task = Task(
            task_name=body_data.get('task_name'),
            description=body_data.get('description'),
            status=body_data.get('status'),
            priority=body_data.get('priority'),
            date = date.today(),
            user_id=get_jwt_identity(),
            project=project
        )
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task), 201
    else:
        return {'error': f"project with {project_id} not found"}, 404
    
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_task(project_id, task_id):
    # Check if the project exists
    project = Project.query.get(project_id)
    if not project:
        return {'error': f'Project with id {project_id} not found'}, 404

    # Query the task associated with the project
    stmt = db.select(Task).filter_by(id=task_id, project_id=project_id)
    task = db.session.scalar(stmt)
    
    if task:
        db.session.delete(task)
        db.session.commit()
        return {'message': f'Task {task_id} deleted'}, 200
    else:
        return {'error': f'Task {task_id} not found in project {project_id}'}, 404

@tasks_bp.route('/<int:task_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_task(project_id, task_id):
    # Check if the project exists
    project = Project.query.get(project_id)
    if not project:
        return {'error': f'Project with id {project_id} not found'}, 404

    # Query the task associated with the project
    stmt = db.select(Task).filter_by(id=task_id, project_id=project_id)
    task = db.session.scalar(stmt)
    
    if task:
        if str(task.user_id) != get_jwt_identity():
            return {'error': 'You have to be owner to update this project'}, 403
        # Update the task properties based on the request data
        body_data = task_schema.load(request.get_json(), partial=True)
        task.task_name = body_data.get('task_name', task.task_name)
        task.description = body_data.get('description', task.description)
        task.status = body_data.get('status', task.status)
        task.priority = body_data.get('priority', task.priority)
        
        db.session.commit()
        return task_schema.dump(task), 200
    else:
        return {'error': f'Task {task_id} not found in project {project_id}'}, 404
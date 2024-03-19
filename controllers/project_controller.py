from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from sqlalchemy.orm import selectinload

from init import db
from models.project import Project, projects_schema, project_schema
from models.task import Task, task_schema, tasks_schema
from models.comment import Comment, comment_schema


projects_bp = Blueprint('projects', __name__, url_prefix='/projects')


@projects_bp.route('/')
def get_projects():
    stmt = db.select(Project).order_by(Project.date.desc())
    projects = db.session.scalars(stmt)
    return projects_schema.dump(projects)


@projects_bp.route('/<int:project_id>')
def get_project(project_id):
    stmt = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(stmt)
    if project:
        return project_schema.dump(project)
    else:
        return {'error': f'Project {project_id} not found'}, 404
    
@projects_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    body_date = request.get_json()
    # create new project model instance

    project = Project(
        project_name = body_date.get('project_name'),
        description = body_date.get('description'),
        date = date.today(),
        user_id = get_jwt_identity()
    )
    # Add that to session and commit
    db.session.add(project)
    db.session.commit()

    # return newly created project
    return project_schema.dump(project), 201

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    # get project from database from id = project_id
    stmt = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(stmt)
    # if project exists, delete it
   
    if project:
        db.session.delete(project)
        db.session.commit()
        return {'message': f'Project {project_id} deleted'}, 200
    
    # else return error message
    else:
        return {'error': f'Project {project_id} not found'}, 404

@projects_bp.route('/<int:project_id>', methods=['PUT', 'PATCH'])
def update_project(project_id):
    # get the data from request body
    body_data = request.get_json()
    # get the project from the db whose fields need to be updated
    stmt = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(stmt)
    # if project exists, update it
    if project:
        project.project_name = body_data.get('project_name') or project.project_name
        project.description = body_data.get('description') or project.description
        db.session.commit()
        return project_schema.dump(project), 200
    # else return error message
    else:
        return {'error': f'Project {project_id} not found'}, 404


#get all tasks for a project
@projects_bp.route('/<int:project_id>/tasks')
def get_tasks(project_id):
    stmt = db.select(Task).filter_by(project_id=project_id)
    tasks = db.session.scalars(stmt).all()  # Fetch all results
    return jsonify(tasks_schema.dump(tasks)), 200

@projects_bp.route('/<int:project_id>/tasks', methods=['POST'])
@jwt_required()
def create_task(project_id):

    # data we get from  the body of the request
    body_data = request.get_json()
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
    
@projects_bp.route('/<int:project_id>/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(project_id, task_id):
    stmt = db.select(Task).filter_by(id=task_id, project_id=project_id)
    task = db.session.scalar(stmt)
    if task:
        db.session.delete(task)
        db.session.commit()
        return {'message': f'Task {task_id} deleted'}, 200
    else:
        return {'error': f'Task {task_id} not found in project {project_id}'}, 404
    

@projects_bp.route('/<int:project_id>/tasks/<int:task_id>', methods = ['PUT', 'PATCH'])
@jwt_required()
def update_task(project_id, task_id):
    body_data = request.get_json()
    stmt = db.select(Task).filter_by(id=task_id, project_id=project_id)
    task = db.session.scalar(stmt)
    if task:
        task.task_name = body_data.get('task_name') or task.task_name
        task.description = body_data.get('description') or task.description
        task.status = body_data.get('status') or task.status
        task.priority = body_data.get('priority') or task.priority
        db.session.commit()
        return task_schema.dump(task), 200
    else:
        return {'error': f'Task {task_id} not found in project {project_id}'}, 404

# create a new comment    

@projects_bp.route('/<int:project_id>/tasks/<int:task_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(project_id, task_id):
    body_data = request.get_json()
    stmt = db.select(Task).filter_by(id=task_id, project_id=project_id)
    task = db.session.scalar(stmt)
    if not task:
        return {'error': f'Task {task_id} not found in project {project_id}'}, 404
    
    try:
        comment = Comment(
            message=body_data.get('message'),
            user_id=get_jwt_identity(),
            task_id=task_id
        )
        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

    
# delete a comment
@projects_bp.route('/<int:project_id>/tasks/<int:task_id>/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(project_id, task_id, comment_id):
    # Check if the comment exists and belongs to the provided task
    stmt = db.select(Comment).filter_by(id=comment_id, task_id=task_id)
    comment = db.session.scalar(stmt)
    if not comment:
        return {'error': f'Comment {comment_id} not found in task {task_id}'}, 404
    
    # Check if the task associated with the comment belongs to the provided project
    if comment.task.project_id != project_id:
        return {'error': f'Comment {comment_id} does not belong to project {project_id}'}, 404
    
    # Delete the comment
    db.session.delete(comment)
    db.session.commit()
    return {'message': f'Comment {comment_id} deleted'}, 200

# edit comment
@projects_bp.route('/<int:project_id>/tasks/<int:task_id>/comments/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(project_id, task_id, comment_id):
    body_data = request.get_json()
    stmt = db.select(Comment).filter_by(id=comment_id, task_id=task_id)
    comment = db.session.scalar(stmt)
    if not comment:
        return {'error': f'Comment {comment_id} not found in task {task_id}'}, 404
    
    # Check if the task associated with the comment belongs to the provided project
    if comment.task.project_id!= project_id:
        return {'error': f'Comment {comment_id} does not belong to project {project_id}'}, 404
    
    # Update the comment
    comment.message = body_data.get('message') or comment.message
    db.session.commit()
    return comment_schema.dump(comment), 200




    

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

from init import db
from models.project import Project, projects_schema, project_schema


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


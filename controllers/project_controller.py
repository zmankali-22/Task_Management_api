from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date


from init import db
from models.project import Project, projects_schema, project_schema
from controllers.task_controller import tasks_bp
from controllers.authorise_as_admin import authorise_as_admin




projects_bp = Blueprint('projects', __name__, url_prefix='/projects')
projects_bp.register_blueprint(tasks_bp)





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
    body_data = project_schema.load(request.get_json())
    # create new project model instance

    project = Project(
        project_name = body_data.get('project_name'),
        description = body_data.get('description'),
        date = date.today(),
        user_id = get_jwt_identity()
    )
    # Add that to session and commit
    db.session.add(project)
    db.session.commit()

    # return newly created project
    return project_schema.dump(project), 201

@projects_bp.route('/<int:project_id>', methods=['DELETE'])

@jwt_required()
@authorise_as_admin
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
@jwt_required()
def update_project(project_id):
    # get the data from request body
    body_data = project_schema.load(request.get_json(), partial = True)
    # get the project from the db whose fields need to be updated
    stmt = db.select(Project).filter_by(id=project_id)
    project = db.session.scalar(stmt)
    # if project exists, update it
    if project:
        if str(project.user_id) != get_jwt_identity():
            return {'error': 'You have to be owner to update this project'}, 403
        project.project_name = body_data.get('project_name') or project.project_name
        project.description = body_data.get('description') or project.description
        db.session.commit()
        return project_schema.dump(project), 200
    # else return error message
    else:
        return {'error': f'Project {project_id} not found'}, 404
    








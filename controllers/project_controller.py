from flask import Blueprint

from init import db
from models.project import Project, projects_schema


projects_bp = Blueprint('projects', __name__, url_prefix='/projects')


@projects_bp.route('/')
def get_projects():
    stmt = db.select(Project).order_by(Project.date.desc())
    projects = db.session.scalars(stmt)
    return projects_schema.dump(projects)



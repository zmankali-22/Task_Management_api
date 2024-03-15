from flask import Blueprint

from datetime import date

from init import db
from models.task import Task, tasks_schema


tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/')
def get_tasks():
    stmt = db.select(Task).order_by(Task.date.desc())
    tasks = db.session.scalars(stmt)
    return tasks_schema.dump(tasks)


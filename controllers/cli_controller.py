from flask import Blueprint
from init import db,bcrypt
from models.user import User
from models.project import Project
from models.task import Task
from models.comment import Comment

from datetime import date


db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created")


@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(
            email="admin@example.com",
            password=bcrypt.generate_password_hash('123456').decode('utf8'),
            is_admin=True
        ),
        User(
            username='User1',
            email="user1@example.com",
            password=bcrypt.generate_password_hash('123456').decode('utf8'),
            is_admin=False
        )
    ]

    db.session.add_all(users)

    projects = [
        Project(
            project_name="Project1",
            description="This is the first project",
            date = date.today(),
            user = users[0]
        ),
        Project(
            project_name="Project2",
            description="This is the second project",
            date = date.today(),
            user = users[0]
        ),
        Project(
            project_name="Project3",
            description="This is the third project",
            date = date.today(),
            user = users[1]
        )

    ]

    db.session.add_all(projects)


    tasks = [

        Task(
            task_name="Task1",
            description="This is the first task",
            status="In Progress",
            priority="High",
            date = date.today(),
            project = projects[0],
            user = users[0]

        ),
        Task(
            task_name="Task2",
            description="This is the second task",
            status="In Progress",
            priority="High",
            date = date.today(),
            project = projects[1],
            user = users[0]
        ),
        Task(
            task_name="Task3",
            description="This is the third task",
            status="In Progress",
            priority="High",
            date = date.today(),
            project = projects[2],
            user = users[1]
        ),
        Task(
            task_name="Task4",
            description="This is the fourth task",
            status="In Progress",
            priority="High",
            date = date.today(),
            project = projects[2],
            user = users[1]
        )
    ]

    db.session.add_all(tasks)

    comments = [

        Comment(
            message="This is the first comment",
            user = users[0],
            project = projects[0],
            task = tasks[0]
        ),
        Comment(
            message="This is the second comment",
            user = users[0],
            project = projects[1],
            task = tasks[1]
        ),
        Comment(
            message="This is the third comment",
            user = users[1],
            project = projects[2],
            task = tasks[2]
        ),
        Comment(
            message="This is the fourth comment",
            user = users[1],
            project = projects[2],
            task = tasks[3],
        ),
        Comment(
            message="This is the fifth comment",
            user = users[1],
            project = projects[2],
            task = tasks[3],
        )

    ]

    db.session.add_all(comments)
    db.session.commit()
    print("Tables seeded")


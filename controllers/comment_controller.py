

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.project import Project
from init import db
from models.task import Task
from models.comment import Comment, comment_schema

comments_bp = Blueprint('comments', __name__, url_prefix='/<int:task_id>/comments')


# create a new comment    

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(project_id, task_id):
    # Check if the project exists
    project = Project.query.get(project_id)
    if not project:
        return {'error': f'Project with id {project_id} not found'}, 404

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
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(project_id, task_id, comment_id):
    

    # Check if the project exists
    project = Project.query.get(project_id)
    if not project:
        return {'error': f'Project with id {project_id} not found'}, 404

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
@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(project_id, task_id, comment_id):
  
    # Check if the project exists
    project = Project.query.get(project_id)
    if not project:
        return {'error': f'Project with id {project_id} not found'}, 404

    body_data = request.get_json()
    stmt = db.select(Comment).filter_by(id=comment_id, task_id=task_id)
    comment = db.session.scalar(stmt)
    if not comment:
        return {'error': f'Comment {comment_id} not found in task {task_id}'}, 404
    
    # Check if the task associated with the comment belongs to the provided project
    if comment.task.project_id != project_id:
        return {'error': f'Comment {comment_id} does not belong to project {project_id}'}, 404

  

    # Update the comment
    comment.message = body_data.get('message') or comment.message
    db.session.commit()




    

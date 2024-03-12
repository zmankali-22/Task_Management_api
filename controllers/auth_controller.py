from flask import Blueprint, request
from init import db, bcrypt

from models.user import User, user_schema

auth_bp = Blueprint ('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        body_data = request.get_json()

        password = body_data.get('password')
        hashed_password = ''
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf8')

        user = User(
            username = body_data.get('username'),
            email = body_data.get('email'),
            password = hashed_password
          
        )

        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    except Exception as e:
        raise e
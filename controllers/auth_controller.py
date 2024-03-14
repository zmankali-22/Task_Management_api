from datetime import timedelta
from flask import Blueprint, request
from init import db, bcrypt

from models.user import User, user_schema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from psycopg2 import errorcodes

auth_bp = Blueprint ('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        body_data = request.get_json()

        user = User(
            username = body_data.get('username'),
            email = body_data.get('email'),
          
        )
        password = body_data.get('password')
        if password:
            user.password= bcrypt.generate_password_hash(password).decode('utf8')


        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name}  is required"}
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'Email address  already exists'}, 409
    
@auth_bp.route('/login/', methods=['POST'])
def login():
    # get the data from request body
    body_data = request.get_json()
    # find the user with email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # if the user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # create token
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # return the token along with user information
        return {"email": user.email, "token":token, "is_admin": user.is_admin}
    else:
        # return the error message
        return {'error': 'Invalid email or password'}, 401
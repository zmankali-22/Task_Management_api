
import os
from flask import Flask
from marshmallow.exceptions import ValidationError

from init import db,ma,bcrypt,jwt 

def create_app():
    app = Flask(__name__)
    app.json.sort_keys =False
    # configs
    app.config["SQLALCHEMY_DATABASE_URI"] =os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # @app.errorhandler(400)
    # def bad_request(error):
    #     return {'error': str(error)}, 400
    
    # @app.errorhandler(404)
    # def not_found(error):
    #     return {'error': str(error)}, 404

    # @app.errorhandler(ValidationError)
    # def validation_error(error):
    #     return {'error': error.messages}, 400

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.project_controller import projects_bp
    app.register_blueprint(projects_bp)

    from controllers.task_controller import tasks_bp
    app.register_blueprint(tasks_bp)

    # from controllers.card_controller import cards_bp


    # app.register_blueprint(cards_bp)

    return app
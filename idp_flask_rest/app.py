import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user_resource import UserRegisterResource, UserLoginResource, UserListResource
from resources.project_resource import ProjectResource, ProjectListResource
from resources.task_resource import TaskResource, TaskListResource
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    api = Api(app)
    
    api.add_resource(UserRegisterResource, '/auth/register')
    api.add_resource(UserLoginResource, '/auth/login')
    
    api.add_resource(ProjectListResource, '/projects')
    api.add_resource(ProjectResource, '/projects/<int:project_id>')
    
    api.add_resource(TaskListResource, '/projects/<int:project_id>/tasks')
    api.add_resource(TaskResource, '/tasks/<int:task_id>')

    api.add_resource(UserListResource, '/users')
    
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.getenv('FLASK_DEBUG', 'True') == 'True')
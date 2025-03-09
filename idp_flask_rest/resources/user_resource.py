from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from schemas import UserSchema, UserLoginSchema, UserListSchema
from repositories import UserRepository
from services import UserService

user_schema = UserSchema()
users_schema = UserListSchema(many=True)
user_service = UserService(UserRepository())

class UserRegisterResource(Resource):
    def post(self):
        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        errors = user_schema.validate(json_data)
        if errors:
            return {"message": "Validation errors", "errors": errors}, 422
        
        user, error = user_service.create_user(json_data)
        
        if error:
            return {"message": error}, 409
        
        result = user_schema.dump(user)
        return {"message": "User created successfully", "user": result}, 201

class UserLoginResource(Resource):
    def post(self):
        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        login_schema = UserLoginSchema()
        errors = login_schema.validate(json_data)
        
        if errors:
            return {"message": "Validation errors", "errors": errors}, 422
        
        auth_data = user_service.authenticate(json_data.get('email'), json_data.get('password'))
        
        if not auth_data:
            return {"message": "Invalid credentials"}, 401
        
        result = user_schema.dump(auth_data['user'])
        return {
            "message": "Login successful",
            "user": result,
            "access_token": auth_data['access_token']
        }, 200

class UserListResource(Resource):
    @jwt_required()
    def get(self):
        users = user_service.get_users()
        return users_schema.dump(users), 200     
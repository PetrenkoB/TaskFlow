from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import ProjectSchema
from repositories import ProjectRepository
from services import ProjectService

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
project_service = ProjectService(ProjectRepository())

class ProjectResource(Resource):
    @jwt_required()
    def get(self, project_id):
        current_user_id = get_jwt_identity()
        project = project_service.get_project(project_id)
        
        if not project:
            return {"message": "Project not found"}, 404
        
        if project.owner_id != current_user_id:
            return {"message": "Access denied"}, 403
        
        return project_schema.dump(project), 200
    
    @jwt_required()
    def put(self, project_id):
        current_user_id = get_jwt_identity()
        
        if not project_service.is_owner(project_id, current_user_id):
            return {"message": "Access denied"}, 403
        
        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        errors = project_schema.validate(json_data)
        if errors:
            return {"message": "Validation errors", "errors": errors}, 422
        
        updated_project = project_service.update_project(project_id, json_data)
        
        if not updated_project:
            return {"message": "Project not found"}, 404
        
        return project_schema.dump(updated_project), 200
    
    @jwt_required()
    def delete(self, project_id):
        current_user_id = get_jwt_identity()
        
        if not project_service.is_owner(project_id, current_user_id):
            return {"message": "Access denied"}, 403
        
        project = project_service.delete_project(project_id)
        
        if not project:
            return {"message": "Project not found"}, 404
        
        return {"message": "Project deleted successfully"}, 204

class ProjectListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        
        
        status = request.args.get('status')
        name = request.args.get('name')
        
        filters = {'owner_id': current_user_id}
        if status:
            filters['status'] = status
        if name:
            filters['name'] = name
        
        projects = project_service.get_projects(filters)
        return projects_schema.dump(projects), 200
    
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        
        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        
        json_data['owner_id'] = current_user_id
        
        errors = project_schema.validate(json_data)
        if errors:
            return {"message": "Validation errors", "errors": errors}, 422
        
        new_project = project_service.create_project(json_data)
        
        return project_schema.dump(new_project), 201
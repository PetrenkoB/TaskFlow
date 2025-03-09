from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas import TaskSchema
from repositories import TaskRepository
from services import TaskService, ProjectService
from repositories import ProjectRepository

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

project_service = ProjectService(ProjectRepository())
task_service = TaskService(TaskRepository(), project_service)

class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id):
        current_user_id = get_jwt_identity()
        task = task_service.get_task(task_id)
        
        if not task:
            return {"message": "Task not found"}, 404
        
        project = project_service.get_project(task.project_id)
        

        if project.owner_id != current_user_id and task.assignee_id != current_user_id:
            return {"message": "Access denied"}, 403
        
        return task_schema.dump(task), 200
    
    @jwt_required()
    def put(self, task_id):
        current_user_id = get_jwt_identity()
        
        if not task_service.can_manage_task(task_id, current_user_id):
            return {"message": "Access denied"}, 403
        
        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        

        if 'project_id' in json_data:
            del json_data['project_id']
        
        errors = task_schema.validate(json_data)
        if errors:
            return {"message": "Validation errors", "errors": errors}, 422
        
        updated_task = task_service.update_task(task_id, json_data)
        
        if not updated_task:
            return {"message": "Task not found"}, 404
        
        return task_schema.dump(updated_task), 200
    
    @jwt_required()
    def delete(self, task_id):
        current_user_id = get_jwt_identity()
        
        task = task_service.get_task(task_id)
        if not task:
            return {"message": "Task not found"}, 404
        
        if not project_service.is_owner(task.project_id, current_user_id):
            return {"message": "Access denied"}, 403
        
        task_service.delete_task(task_id)
        return {"message": "Task deleted successfully"}, 204

class TaskListResource(Resource):
    @jwt_required()
    def get(self, project_id):
        current_user_id = get_jwt_identity()
        
        project = project_service.get_project(project_id)
        if not project:
            return {"message": "Project not found"}, 404
        
        if project.owner_id != current_user_id:

            return {"message": "Access denied"}, 403
        
        
        status = request.args.get('status')
        priority = request.args.get('priority')
        assignee_id = request.args.get('assignee_id')
        
        filters = {'project_id': project_id}
        if status:
            filters['status'] = status
        if priority:
            filters['priority'] = priority
        if assignee_id:
            filters['assignee_id'] = int(assignee_id)
        
        tasks = task_service.get_tasks(filters)
        return tasks_schema.dump(tasks), 200
    
    @jwt_required()
    def post(self, project_id):
        current_user_id = get_jwt_identity()
        
        project = project_service.get_project(project_id)
        if not project:
            return {"message": "Project not found"}, 404
        

        if project.owner_id != current_user_id:
            return {"message": "Access denied"}, 403
        
        json_data = request.get_json()
        
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        json_data['project_id'] = project_id
        
        errors = task_schema.validate(json_data)
        if errors:
            return {"message": "Validation errors", "errors": errors}, 422
        
        new_task = task_service.create_task(json_data)
        
        return task_schema.dump(new_task), 201
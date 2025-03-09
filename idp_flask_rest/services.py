from flask_jwt_extended import create_access_token

class UserService:
    def __init__(self, repository):
        self.repository = repository
    
    def get_users(self, filters=None):
        filters = filters or {}
        return self.repository.get_all(**filters)
    
    def get_user(self, user_id):
        return self.repository.get_by_id(user_id)
    
    def create_user(self, user_data):
        
        if self.repository.get_by_email(user_data.get('email')):
            return None, "Email already registered"
        
      
        if self.repository.get_by_username(user_data.get('username')):
            return None, "Username already taken"
        
        user = self.repository.create(user_data)
        return user, None
    
    def authenticate(self, email, password):
        user = self.repository.get_by_email(email)
        
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {
                'user': user,
                'access_token': access_token
            }
        
        return None

class ProjectService:
    def __init__(self, repository):
        self.repository = repository
    
    def get_projects(self, filters=None):
        filters = filters or {}
        return self.repository.get_all(**filters)
    
    def get_project(self, project_id):
        return self.repository.get_by_id(project_id)
    
    def create_project(self, project_data):
        return self.repository.create(project_data)
    
    def update_project(self, project_id, project_data):
        return self.repository.update(project_id, project_data)
    
    def delete_project(self, project_id):
        return self.repository.delete(project_id)
    
    def is_owner(self, project_id, user_id):
        project = self.get_project(project_id)
        return project and project.owner_id == user_id

class TaskService:
    def __init__(self, repository, project_service):
        self.repository = repository
        self.project_service = project_service
    
    def get_tasks(self, filters=None):
        filters = filters or {}
        return self.repository.get_all(**filters)
    
    def get_task(self, task_id):
        return self.repository.get_by_id(task_id)
    
    def create_task(self, task_data):
        return self.repository.create(task_data)
    
    def update_task(self, task_id, task_data):
        return self.repository.update(task_id, task_data)
    
    def delete_task(self, task_id):
        return self.repository.delete(task_id)
    
    def can_manage_task(self, task_id, user_id):
        task = self.get_task(task_id)
        if not task:
            return False
        
        return self.project_service.is_owner(task.project_id, user_id) or task.assignee_id == user_id
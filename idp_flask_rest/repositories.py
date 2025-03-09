from interfaces import RepositoryInterface
from models import User, Project, Task
from db import db

class UserRepository(RepositoryInterface):
    def get_all(self, **kwargs):
        query = User.query
        if 'username' in kwargs:
            query = query.filter(User.username.like(f"%{kwargs['username']}%"))
        if 'email' in kwargs:
            query = query.filter(User.email == kwargs['email'])
        return query.all()
    
    def get_by_id(self, id):
        return User.query.get(id)
    
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()
    
    def create(self, data):
        user = User(
            email=data.get('email'),
            username=data.get('username')
        )
        user.set_password(data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        return user
    
    def update(self, id, data):
        user = self.get_by_id(id)
        if user:
            if 'email' in data:
                user.email = data['email']
            if 'username' in data:
                user.username = data['username']
            if 'password' in data:
                user.set_password(data['password'])
            if 'role' in data:
                user.role = data['role']
            
            db.session.commit()
        return user
    
    def delete(self, id):
        user = self.get_by_id(id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user

class ProjectRepository(RepositoryInterface):
    def get_all(self, **kwargs):
        query = Project.query
        if 'owner_id' in kwargs:
            query = query.filter_by(owner_id=kwargs['owner_id'])
        if 'status' in kwargs:
            query = query.filter_by(status=kwargs['status'])
        if 'name' in kwargs:
            query = query.filter(Project.name.like(f"%{kwargs['name']}%"))
        return query.all()
    
    def get_by_id(self, id):
        return Project.query.get(id)
    
    def create(self, data):
        project = Project(
            name=data.get('name'),
            description=data.get('description'),
            status=data.get('status', 'active'),
            deadline=data.get('deadline'),
            owner_id=data.get('owner_id')
        )
        
        db.session.add(project)
        db.session.commit()
        return project
    
    def update(self, id, data):
        project = self.get_by_id(id)
        if project:
            for key, value in data.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            
            db.session.commit()
        return project
    
    def delete(self, id):
        project = self.get_by_id(id)
        if project:
            db.session.delete(project)
            db.session.commit()
        return project

class TaskRepository(RepositoryInterface):
    def get_all(self, **kwargs):
        query = Task.query
        if 'project_id' in kwargs:
            query = query.filter_by(project_id=kwargs['project_id'])
        if 'assignee_id' in kwargs:
            query = query.filter_by(assignee_id=kwargs['assignee_id'])
        if 'status' in kwargs:
            query = query.filter_by(status=kwargs['status'])
        if 'priority' in kwargs:
            query = query.filter_by(priority=kwargs['priority'])
        return query.all()
    
    def get_by_id(self, id):
        return Task.query.get(id)
    
    def create(self, data):
        task = Task(
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status', 'todo'),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date'),
            project_id=data.get('project_id'),
            assignee_id=data.get('assignee_id')
        )
        
        db.session.add(task)
        db.session.commit()
        return task
    
    def update(self, id, data):
        task = self.get_by_id(id)
        if task:
            for key, value in data.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            
            db.session.commit()
        return task
    
    def delete(self, id):
        task = self.get_by_id(id)
        if task:
            db.session.delete(task)
            db.session.commit()
        return task
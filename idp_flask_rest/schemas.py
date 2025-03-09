from marshmallow import Schema, fields, validate, validates, ValidationError
from models import User, Project

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class UserListSchema(Schema):
    email = fields.Email(dump_only=True)
    username = fields.String(dump_only=True)   
    role = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)     


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

class ProjectSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String()
    status = fields.String(validate=validate.OneOf(['active', 'completed', 'on_hold', 'cancelled']))
    deadline = fields.Date(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    owner_id = fields.Integer(dump_only=True)
    owner = fields.Nested(lambda: UserSchema(only=('id', 'username')), dump_only=True)
    task_count = fields.Method("get_task_count", dump_only=True)
    
    def get_task_count(self, obj):
        return len(obj.tasks)

class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String()
    status = fields.String(validate=validate.OneOf(['todo', 'in_progress', 'review', 'done']))
    priority = fields.String(validate=validate.OneOf(['low', 'medium', 'high', 'urgent']))
    due_date = fields.Date(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    project_id = fields.Integer()
    project = fields.Nested(lambda: ProjectSchema(only=('id', 'name')), dump_only=True)
    assignee_id = fields.Integer(allow_none=True)
    assignee = fields.Nested(lambda: UserSchema(only=('id', 'username')), dump_only=True)
    
    @validates('project_id')
    def validate_project(self, value):
        if not Project.query.get(value):
            raise ValidationError('Project not found')
    
    @validates('assignee_id')
    def validate_assignee(self, value):
        if value is None:
            return
        if not User.query.get(value):
            raise ValidationError('User not found')
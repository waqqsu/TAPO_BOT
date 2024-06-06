from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from init import db ,app
from datetime import datetime

# Вспомогательная таблица для связи "много ко многим"
user_project_association = db.Table('user_project_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    secondname = db.Column(db.String(50), nullable=False)
    kod = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    birth_date = db.Column(db.Date)

    projects = db.relationship('Project', secondary=user_project_association, back_populates='users')
    
    def ToDict(self):
        return {
            'user_id': self.user_id,
            'telegram_id': self.telegram_id,
            'username': self.username,
            'firstname': self.firstname,
            'secondname': self.secondname,
            'kod':self.kod,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    lid_id = db.Column(db.String(50), db.ForeignKey('user.telegram_id'), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    users = db.relationship('User', secondary=user_project_association, back_populates='projects')

    def ToDict(self):
        return {
            'project_id': self.project_id,
            'project_name': self.project_name,
            'description': self.description,
            'lid_id': self.lid_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Integer)
    status = db.Column(db.Enum('New', 'In Progress', 'Completed'), default='New')
    priority = db.Column(db.Enum('Low', 'Medium', 'High'), default='Medium')
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def ToDict(self):
        return {
            'task_id': self.task_id,
            'project_id': self.project_id,
            'assigned_to': self.assigned_to,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'rating': self.rating,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    comment_text = db.Column(db.Text, nullable=False)

    def ToDict(self):
        return {
            'comment_id': self.comment_id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'comment_text': self.comment_text
        }
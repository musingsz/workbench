from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Association table for private workspace members
workspace_members = db.Table('workspace_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('workspace_id', db.Integer, db.ForeignKey('workspace.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(64), unique=True, nullable=False) # WeCom UserID
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(255))
    
    # Relationships
    workbenches_owned = db.relationship('Workbench', backref='owner', lazy=True)
    
    def __repr__(self):
        return f'<User {self.name}>'

class Workbench(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    workspaces = db.relationship('Workspace', backref='workbench', lazy=True, cascade="all, delete-orphan")

class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_public = db.Column(db.Boolean, default=True) # If False, check allowed_users
    workbench_id = db.Column(db.Integer, db.ForeignKey('workbench.id'), nullable=False)
    
    # Relationships
    apps = db.relationship('AppIcon', backref='workspace', lazy=True, cascade="all, delete-orphan")
    allowed_users = db.relationship('User', secondary=workspace_members, lazy='subquery',
        backref=db.backref('accessible_workspaces', lazy=True))

class AppIcon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255)) # Added description
    url = db.Column(db.String(500), nullable=False)
    icon_url = db.Column(db.String(500)) # URL to an image/logo (remote or local path)
    icon_type = db.Column(db.String(20), default="url") # 'url', 'upload', 'auto'
    color = db.Column(db.String(20), default="blue") # For UI styling if no icon provided
    visits = db.Column(db.Integer, default=0) # Added visits counter
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)

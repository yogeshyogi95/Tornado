import datetime
import secrets
from sqlalchemy import (Column, BigInteger, String, Text, DateTime, 
                        Boolean, Unicode, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import collate
from sqlalchemy.sql.expression import null
from tornado_sqlalchemy import SQLAlchemy
from todo import database_url

db = SQLAlchemy(database_url)



class Task(db.Model):
    """Tasks for the To Do List"""
    __tablename__ = "tasks"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), unique=True)
    note = Column(Text)
    creation_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="tasks")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creation_date = datetime.now()

class User(db.Model):
    """The User Object that owns tasks"""
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(50), nullable=False)
    date_joined = Column(DateTime, nullable=False)
    token = Column(Unicode, nullable=False)
    tasks = relationship("Task", back_populates="users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_joined = datetime.now()
        self.token = secrets.token_urlsafe(64)

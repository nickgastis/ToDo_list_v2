from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    todo_lists = relationship('TodoList', backref='user', lazy=True)
    

class TodoList(Base):
    __tablename__ = 'todo_lists'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tasks = relationship('Task', backref='todo_list', lazy=True)
    

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    todo_list_id = Column(Integer, ForeignKey('todo_lists.id'), nullable=False)

# engine = create_engine('sqlite:///todo_App.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
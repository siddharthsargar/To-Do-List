# # models.py
# from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# #from .database import Base  # Assuming you're using a `Base` object from SQLAlchemy

# DATABASE_URL = "sqlite:///./test.db"

# Base = declarative_base()
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     password = Column(String)

#     # Relationship with tasks (User can have many tasks)
#     tasks = relationship("Task", back_populates="owner")
    
# class Task(Base):
#     __tablename__ = "tasks"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, nullable=True)
#     completed = Column(Boolean, default=False)
#     owner_id = Column(Integer, ForeignKey("users.id"))


#     # Relationship with the User model (assumed to be defined)
#     owner = relationship("User", back_populates="tasks")




#------------------------17/12/24--------------------


#Define database models for User and Task.
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks") 















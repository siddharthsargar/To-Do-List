# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional

# app = FastAPI()


# # Define the structure of the Task using Pydantic
# class Task(BaseModel):
#     id: int
#     title: str
#     description: Optional[str] = None
#     completed: bool = False


# # In-memory database (a simple list to store tasks)
# tasks = []
# task_counter = 0  # To keep track of the last task ID


# # Route to get all tasks
# @app.get("/tasks", response_model=List[Task])
# def get_tasks():
#     return tasks


# # Route to create a new task
# @app.post("/tasks", response_model=Task)
# def create_task(task: Task):
#     global task_counter
#     task.id = task_counter  # Assign a unique id to the task
#     print("tasks 0 is", tasks)
#     tasks.append(task)
#     task_counter += 1
#     print("tasks is", tasks)
#     print("task is", task)
#     return task


# # Route to get a specific task by ID
# @app.get("/tasks/{task_id}", response_model=Task)
# def get_task(task_id: int):
#     print("task_id is", task_id)
#     print("tasks is", tasks)
#     if task_id < 0 or task_id >= len(tasks):
#         return {"error": "Task not found"}
#     return tasks[task_id]


# # Route to update a task
# @app.put("/tasks/{task_id}", response_model=Task)
# def update_task(task_id: int, updated_task: Task):
#     print("task_id is", task_id)
#     print("tasks is", tasks)
#     if task_id < 0 or task_id >= len(tasks):
#         return {"error": "Task not found"}
#     tasks[task_id] = updated_task
#     tasks[task_id].id = task_id  # Ensure the task id remains the same after update
#     return updated_task


# # Route to delete a task
# @app.delete("/tasks/{task_id}", response_model=Task)
# def delete_task(task_id: int):
#     if task_id < 0 and task_id >= len(tasks):
#         return {"error": "Task not found"}
#     task = tasks.pop(task_id)
#     return task



#---------------------------------------------------------------------

# main.py
# from fastapi import FastAPI, Depends, HTTPException, status, Header
# from sqlalchemy.orm import Session
# import uvicorn
# from models import SessionLocal, User, Task  # Make sure this imports from your actual models file
# from pydantic import BaseModel
# import jwt
# import bcrypt
# from datetime import datetime, timedelta
# from typing import List, Optional

# # Settings for JWT
# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Pydantic models for validation
# class UserCreate(BaseModel):
#     username: str
#     password: str

#     class Config:
#         # Ensures compatibility with SQLAlchemy models
#         from_attributes = True  # Renamed from 'orm_mode' in FastAPI v2


# class UserInDB(UserCreate):
#     password: str

# class TaskCreate(BaseModel):
#     title: str
#     description: str = None
#     completed: bool = False

# class TaskOut(BaseModel):
#     id: int
#     title: str
#     description: Optional[str] = None
#     completed: bool

#     # This will help Pydantic understand how to serialize the response
#     class Config:
#         from_attributes = True  # Renamed from 'orm_mode' in FastAPI v2


# # FastAPI instance
# app = FastAPI()

# # JWT Token generation function
# def create_access_token(data: dict):
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode = data.copy()
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # Hash password function
# def hash_password(password: str):
#     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# # Verify password function
# def verify_password(plain_password, hashed_password):
#     return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# # Create new user (registration)
# @app.post("/register", response_model=UserCreate)
# def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     hashed_password = hash_password(user.password)
#     db_user = User(username=user.username, password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return user

# # Login (authenticate user and return JWT token)
# @app.post("/login")
# def login(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if not db_user or not verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     # Create JWT token
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

# # Dependency to get the current user from the JWT token
# def get_current_user(token: str = Depends(Header)):
#     try:
#         # Get the token from the Authorization header
#         token = token.split(" ")[1]  # Expecting "Bearer <token>"
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Could not validate credentials")
#         return username
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401, detail="Could not validate credentials")
#     except IndexError:
#         raise HTTPException(status_code=401, detail="Token is missing or malformed")

# # Get all tasks (for authenticated user)
# @app.get("/tasks", response_model=List[TaskOut])
# def get_tasks(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
#     db_tasks = db.query(Task).filter(Task.owner_id == current_user).all()
#     return db_tasks

# # Create a new task (for authenticated user)
# @app.post("/tasks", response_model=TaskOut)
# def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
#     db_task = Task(**task.dict(), owner_id=current_user)
#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)
#     return db_task

# # Get a specific task by ID (for authenticated user)
# @app.get("/tasks/{task_id}", response_model=TaskOut)
# def get_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
#     db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user).first()
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task

# # Update a task by ID (for authenticated user)
# @app.put("/tasks/{task_id}", response_model=TaskOut)            
# def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
#     db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user).first()
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     db_task.title = task.title
#     db_task.description = task.description
#     db_task.completed = task.completed
#     db.commit()
#     db.refresh(db_task)
#     return db_task

# # Delete a task by ID (for authenticated user)
# @app.delete("/tasks/{task_id}")            
# def delete_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):    
#     db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user).first()
#     if db_task is None:     
#         raise HTTPException(status_code=404, detail="Task not found")
#     db.delete(db_task)
#     db.commit()
#     return {"message": "Task deleted successfully"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



#-------------------17/12/24-------------------

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import User, Task
from schemas import UserCreate, UserResponse, TaskCreate, TaskResponse, TaskListResponse
from auth import ALGORITHM, SECRET_KEY, hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

#import main
from models import User
from sqlalchemy.orm import Session

#Create Tables
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Initialize FastAPI
app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        db_user = db.query(User).filter(User.username == username).first()
        if db_user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return db_user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


# --- User Registration ---
@app.post("/register/", response_model = UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# --- User Login ---
@app.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}



# --- Create Task ---
#@app.post("/tasks/", response_model=TaskResponse)
# def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     new_task = Task(**task.dict(), owner_id=current_user.id) # Mocked owner_id
#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)
#     return new_task
@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the task with the same title already exists for the current user
    existing_task = db.query(Task).filter(Task.title == task.title, Task.owner_id == current_user.id).first()
    if existing_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A task with this title already exists."
        )

    # If no existing task, create the new task
    new_task = Task(**task.dict(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# --- List Tasks ---
@app.get("/tasks/", response_model=TaskListResponse)
def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()  # Mocked owner_id
    return {"tasks": tasks}
 






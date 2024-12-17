from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./todolist.db"


# SQLAlchemy Database Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# Session Maker for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#Base class for declarative models
Base = declarative_base()
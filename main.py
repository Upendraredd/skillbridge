
# from datetime import datetime
# from enum import Enum as PyEnum
# from fastapi import FastAPI
# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Time, Enum, Table
# from sqlalchemy.orm import declarative_base, relationship

# Base = declarative_base()

# # --- Enums ---
# app = FastAPI()  # It must be 'app' in lowercase
    
# class Role(str, PyEnum):
#     student = "student"
#     trainer = "trainer"
#     institution = "institution"
#     programme_manager = "programme_manager"
#     monitoring_officer = "monitoring_officer"

# class AttendanceStatus(str, PyEnum):
#     present = "present"
#     absent = "absent"
#     late = "late"

# # --- Association Tables for Many-to-Many Relationships ---

# batch_trainers = Table(
#     'batch_trainers', Base.metadata,
#     Column('batch_id', Integer, ForeignKey('batches.id', ondelete="CASCADE"), primary_key=True),
#     Column('trainer_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
# )

# batch_students = Table(
#     'batch_students', Base.metadata,
#     Column('batch_id', Integer, ForeignKey('batches.id', ondelete="CASCADE"), primary_key=True),
#     Column('student_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
# )

# # --- Core Entities ---

# class User(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     role = Column(Enum(Role), nullable=False)
#     institution_id = Column(Integer, nullable=True) # Can link to an institution User ID
#     created_at = Column(DateTime, default=datetime.utcnow)

# class Batch(Base):
#     __tablename__ = 'batches'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     institution_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
    
#     # Relationships
#     trainers = relationship("User", secondary=batch_trainers, backref="training_batches")
#     students = relationship("User", secondary=batch_students, backref="enrolled_batches")

# class BatchInvite(Base):
#     __tablename__ = 'batch_invites'
    
#     id = Column(Integer, primary_key=True, index=True)
#     batch_id = Column(Integer, ForeignKey('batches.id', ondelete="CASCADE"), nullable=False)
#     token = Column(String, unique=True, index=True, nullable=False)
#     created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
#     expires_at = Column(DateTime, nullable=False)
#     used = Column(Boolean, default=False)

# class Session(Base):
#     __tablename__ = 'sessions'
    
#     id = Column(Integer, primary_key=True, index=True)
#     batch_id = Column(Integer, ForeignKey('batches.id', ondelete="CASCADE"), nullable=False)
#     trainer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     title = Column(String, nullable=False)
#     date = Column(Date, nullable=False)
#     start_time = Column(Time, nullable=False)
#     end_time = Column(Time, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

# class Attendance(Base):
#     __tablename__ = 'attendance'
    
#     id = Column(Integer, primary_key=True, index=True)
#     session_id = Column(Integer, ForeignKey('sessions.id', ondelete="CASCADE"), nullable=False)
#     student_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
#     status = Column(Enum(AttendanceStatus), nullable=False)
#     marked_at = Column(DateTime, default=datetime.utcnow)

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
import datetime

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-super-secret-key" # Store this in .env later!
ALGORITHM = "HS256"

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

def create_access_token(data: dict, expires_delta: datetime.timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/auth/signup")
def signup(user: UserCreate):
    # In a real app, you must check if the email already exists in the database here
    
    hashed_password = pwd_context.hash(user.password)
    
    # Save the new user to your database here using SQLAlchemy
    
    # Generate token
    access_token_expires = datetime.timedelta(hours=24)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Add your /auth/login and other endpoints here
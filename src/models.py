from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) 
    institution_id = Column(Integer, nullable=True) # Assuming no strict FK to institutions table for simplicity if it doesn't exist yet
    created_at = created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Batch(Base):
    __tablename__ = 'batches'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    institution_id = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class BatchTrainer(Base):
    __tablename__ = 'batch_trainers'
    batch_id = Column(Integer, ForeignKey('batches.id'), primary_key=True)
    trainer_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

class BatchStudent(Base):
    __tablename__ = 'batch_students'
    batch_id = Column(Integer, ForeignKey('batches.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

class BatchInvite(Base):
    __tablename__ = 'batch_invites'
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey('batches.id'))
    token = Column(String, unique=True, index=True)
    created_by = Column(Integer, ForeignKey('users.id'))
    expires_at = Column(DateTime)
    used = Column(Boolean, default=False)

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey('batches.id'))
    trainer_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    student_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, nullable=False) # present / absent / late
    marked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Institution(Base):
    __tablename__ = 'institutions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
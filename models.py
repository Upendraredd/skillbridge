from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # student, trainer, institution, programme_manager, monitoring_officer
    institution_id = Column(Integer, ForeignKey('institutions.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Institution(Base):
    __tablename__ = 'institutions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Batch(Base):
    __tablename__ = 'batches'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    institution_id = Column(Integer, ForeignKey('institutions.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Add the remaining models (batch_trainers, batch_students, batch_invites, sessions, attendance) here based on the schema.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, User, Batch, Institution
from src.auth import get_password_hash
import os
from dotenv import load_dotenv

# Load database URL from .env
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    db = SessionLocal()
    
    # Check if we already have users to avoid duplicate errors on multiple runs
    if db.query(User).first():
        print("Database is already seeded!")
        db.close()
        return

    print("Seeding database...")

    # 1. Create a dummy institution
    demo_inst = Institution(name="SkillBridge Academy")
    db.add(demo_inst)
    db.commit()
    db.refresh(demo_inst)

    # 2. Create the test users mentioned in your README
    users_data = [
        {"name": "Demo Student", "email": "student1@test.com", "role": "student"},
        {"name": "Demo Trainer", "email": "trainer1@test.com", "role": "trainer"},
        {"name": "Demo Admin", "email": "inst_admin@test.com", "role": "institution"},
        {"name": "Demo Manager", "email": "prog_mgr@test.com", "role": "programme_manager"},
        {"name": "Demo Monitor", "email": "monitor1@test.com", "role": "monitoring_officer"},
    ]

    hashed_pw = get_password_hash("password123")

    for u in users_data:
        db_user = User(
            name=u["name"],
            email=u["email"],
            hashed_password=hashed_pw,
            role=u["role"],
            institution_id=demo_inst.id
        )
        db.add(db_user)

    # 3. Create a dummy batch
    demo_batch = Batch(name="Full Stack Web Dev - Cohort A", institution_id=demo_inst.id)
    db.add(demo_batch)
    
    db.commit()
    print("Database seeded successfully with test accounts!")
    db.close()

if __name__ == "__main__":
    seed_database()
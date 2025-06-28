import os
import sys
from datetime import datetime, timedelta
from faker import Faker
from werkzeug.security import generate_password_hash

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db, Base, engine
from app.models import User, Job, Application
from app.auth import hash_password

# Initialize Faker
fake = Faker()
Faker.seed(42)  # For consistent results

def create_dummy_data(db):
    """Create dummy users, jobs, and applications"""
    print("🚀 Starting database seeding...")
    
    # Clear existing data
    print("🧹 Clearing existing data...")
    db.query(Application).delete()
    db.query(Job).delete()
    db.query(User).delete()
    db.commit()

    # Create employers
    print("👔 Creating employers...")
    employers = []
    for _ in range(5):
        user = User(
            username=fake.user_name(),
            email=fake.company_email(),
            role="employer",
            hashed_password=hash_password("EmployerPass123!"),
        )
        db.add(user)
        employers.append(user)
    db.commit()

    # Create applicants
    print("👤 Creating applicants...")
    applicants = []
    for _ in range(20):
        user = User(
            username=fake.user_name(),
            email=fake.free_email(),
            role="applicant",
            hashed_password=hash_password("ApplicantPass123!"),
        )
        db.add(user)
        applicants.append(user)
    db.commit()

    # Create jobs
    print("💼 Creating jobs...")
    job_titles = [
        "Senior Software Engineer", "Data Analyst", "Product Manager",
        "UX Designer", "DevOps Engineer", "Marketing Specialist",
        "Sales Representative", "Financial Analyst", "HR Coordinator"
    ]
    job_types = ["full-time", "part-time", "contract"]
    companies = ["TechCorp", "DataSystems", "InnovateCo", "FutureTech", "GlobalSolutions"]
    
    jobs = []
    for _ in range(30):
        employer = fake.random_element(employers)
        job = Job(
            title=fake.random_element(job_titles),
            description=fake.paragraph(nb_sentences=10),
            location=fake.city(),
            salary=round(fake.random_int(min=50000, max=150000), -1),
            company=fake.random_element(companies),
            job_type=fake.random_element(job_types),
            posted_by=employer.id,
            date_posted=fake.date_time_between(start_date="-30d", end_date="now")
        )
        db.add(job)
        jobs.append(job)
    db.commit()

    # Create applications
    print("📝 Creating applications...")
    statuses = ["pending", "reviewed", "rejected", "hired"]
    
    for job in jobs:
        # Each job gets 3-8 applications
        for _ in range(fake.random_int(min=3, max=8)):
            applicant = fake.random_element(applicants)
            
            # Ensure applicant hasn't already applied to this job
            existing = db.query(Application).filter(
                Application.applicant_id == applicant.id,
                Application.job_id == job.id
            ).first()
            
            if not existing:
                application = Application(
                    applicant_id=applicant.id,
                    job_id=job.id,
                    resume_path=f"/resumes/{applicant.username}_resume.pdf",
                    cover_letter_path=f"/cover_letters/{applicant.username}_cover.pdf",
                    submitted_at=fake.date_time_between(
                        start_date=job.date_posted, 
                        end_date="now"
                    ),
                    status=fake.random_element(statuses)
                )
                db.add(application)
    db.commit()

    print("✅ Database seeded successfully!")
    print(f"Created: {len(employers)} employers, {len(applicants)} applicants")
    print(f"         {len(jobs)} jobs, {db.query(Application).count()} applications")

def main():
    # Initialize database connection
    db = next(get_db())
    
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Seed data
        create_dummy_data(db)
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
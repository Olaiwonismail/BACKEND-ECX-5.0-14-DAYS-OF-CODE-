import requests
import random
from datetime import datetime, timedelta

# Current time and location for context
# Current time is Saturday, June 21, 2025 at 5:06:25 AM WAT.
# Current location is Lagos, Lagos, Nigeria.

url = "http://localhost:8080/employer/jobs/create_jobs"  # Change to your actual URL

titles = [
    "Frontend Developer", "Backend Developer", "Fullstack Developer", "Data Scientist",
    "Project Manager", "QA Engineer", "DevOps Engineer", "UI/UX Designer",
    "Content Writer", "Customer Support Rep", "Cloud Engineer", "Mobile Developer",
    "Cybersecurity Analyst", "Network Administrator", "Database Administrator",
    "Business Analyst", "Marketing Specialist", "HR Manager", "Financial Analyst",
    "Systems Administrator"
]

descriptions = [
    "Build and maintain user interfaces using modern frameworks like React/Angular/Vue.",
    "Develop robust and scalable backend services and APIs using Python/Node.js/Java.",
    "Design and implement data pipelines, perform analytics, and build machine learning models for insights.",
    "Coordinate project tasks, manage timelines, and ensure successful project delivery from conception to completion.",
    "Ensure software quality through comprehensive testing, automation, and continuous integration.",
    "Design, implement, and manage scalable infrastructure and CI/CD pipelines on cloud platforms.",
    "Create intuitive, user-friendly, and aesthetically pleasing designs for web and mobile applications.",
    "Write engaging, SEO-friendly content for blogs, websites, marketing materials, and social media.",
    "Provide excellent customer service and technical support to users, resolving inquiries efficiently.",
    "Manage cloud infrastructure on AWS, Azure, or GCP, ensuring high availability and security.",
    "Develop native or cross-platform mobile applications for iOS and Android.",
    "Protect systems, networks, and data from cyber threats through monitoring and incident response.",
    "Maintain and troubleshoot computer networks, ensuring optimal performance and security.",
    "Manage and maintain organizational databases, including backup, recovery, and performance tuning.",
    "Analyze business processes and data to identify areas for improvement and propose solutions.",
    "Develop and execute marketing strategies across various channels to drive brand awareness and lead generation.",
    "Manage human resources functions including recruitment, employee relations, and talent development.",
    "Conduct financial analysis, forecasting, and reporting to support business decisions.",
    "Install, configure, and maintain computer systems and servers."
]

locations = [
    "Lagos, Nigeria", "Abuja, Nigeria", "Ibadan, Nigeria", "Remote", "Port Harcourt, Nigeria",
    "Kano, Nigeria", "Enugu, Nigeria", "Accra, Ghana", "Nairobi, Kenya", "Cape Town, South Africa",
    "London, UK (Remote Eligible)", "New York, USA (Remote Eligible)"
]

companies = [
    "TechCorp Solutions", "DevSpark Innovations", "PrimeWorks Systems", "InsightHub Analytics",
    "QuickHelp Support", "InnoSoft Technologies", "GlobalTech Ventures", "FutureMinds Inc.",
    "Apex Solutions", "Synergy Digital", "BrightLink Services", "Venture Growth",
    "Optimise IT", "Nexus Innovations", "Pinnacle Tech"
]

job_types = ["full-time", "part-time", "contract", "internship", "temporary"]

def generate_dummy_job():
    # Generate a random date within the last 120 days for 'date_posted'
    # This makes the job postings look recent, spanning about 4 months.
    end_date = datetime.now()
    start_date = end_date - timedelta(days=120)
    
    # Randomly pick a datetime between start_date and end_date
    time_diff = end_date - start_date
    random_seconds = random.uniform(0, time_diff.total_seconds())
    date_posted_dt = start_date + timedelta(seconds=random_seconds)

    # For 'updated_at', let's say it's sometimes the same as created, or slightly later
    # 70% chance updated_at is the same, 30% it's later
    updated_at_dt = date_posted_dt
    if random.random() < 0.35: # 35% chance of a later update
        # Add a random number of days (1-30) and hours to simulate updates
        updated_at_dt = date_posted_dt + timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
        # Ensure updated_at is not in the future
        if updated_at_dt > datetime.now():
            updated_at_dt = datetime.now()

    # Generate a random salary, possibly with different ranges for different roles if desired
    # For now, a general broad range
    salary = round(random.uniform(150000, 1200000), 2) # Wider salary range

    return {
        "title": random.choice(titles),
        "description": random.choice(descriptions),
        "location": random.choice(locations),
        "salary": salary,
        "company": random.choice(companies),
        "job_type": random.choice(job_types),
        # Format the datetime objects as ISO 8601 strings
        "date_posted": date_posted_dt.isoformat(),
        # Assuming you have these fields in your model for auditing
        "created_at": date_posted_dt.isoformat(),
        "updated_at": updated_at_dt.isoformat(),
        # Example for application_deadline (optional)
        # "application_deadline": (date_posted_dt + timedelta(days=random.randint(20, 90))).isoformat()
    }

# Assuming a fixed user ID for simplicity for the 'posted_by' field in your model
# IMPORTANT: This ID (e.g., 1) MUST correspond to an existing user in your 'users' table
# who has the role of an employer/recruiter, if your application has such logic.
# Otherwise, your foreign key constraint will fail.
FIXED_EMPLOYER_ID = 1 

# No headers needed if you're truly disabling auth and not setting specific content types.
# However, `requests` will typically set `Content-Type: application/json` automatically
# when `json=` parameter is used, which is generally what you want for a JSON API.

print("Starting to feed dummy job data...")
for i in range(75): # Increased to 75 jobs for more data volume
    job_data = generate_dummy_job()
    
    # Add the fixed employer ID
    job_data["posted_by"] = FIXED_EMPLOYER_ID

    # Using json= parameter will set Content-Type: application/json automatically
    response = requests.post(url, json=job_data) 
    
    if response.status_code == 201:
        print(f"Job {i+1} created successfully. Title: {job_data['title']}, Posted: {job_data['date_posted']}")
    else:
        print(f"Failed to create job {i+1}: Status {response.status_code} - Response: {response.text}")
        print(f"Attempted data: {job_data}")
    
    # Optional: Add a small delay to avoid overwhelming your local server
    import time
    time.sleep(0.1) 

print("Finished feeding dummy job data.")
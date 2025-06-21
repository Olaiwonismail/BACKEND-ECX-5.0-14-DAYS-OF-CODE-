import requests
import random

url = "http://localhost:8080/employer/jobs/create_jobs"  # Change to your actual URL

titles = [
    "Frontend Developer", "Backend Developer", "Fullstack Developer", "Data Scientist",
    "Project Manager", "QA Engineer", "DevOps Engineer", "UI/UX Designer",
    "Content Writer", "Customer Support Rep"
]

descriptions = [
    "Build and maintain user interfaces.",
    "Develop backend services and APIs.",
    "Manage data pipelines and analytics.",
    "Coordinate project tasks and timelines.",
    "Ensure software quality and testing.",
    "Design scalable infrastructure.",
    "Create user-friendly designs.",
    "Write engaging content for blogs.",
    "Provide customer service and support.",
]

locations = ["Lagos, Nigeria", "Abuja, Nigeria", "Ibadan, Nigeria", "Remote", "Port Harcourt"]

companies = ["TechCorp", "DevSpark", "PrimeWorks", "InsightHub", "QuickHelp", "InnoSoft"]

job_types = ["full-time", "part-time", "contract"]

def generate_dummy_job():
    return {
        "title": random.choice(titles),
        "description": random.choice(descriptions),
        "location": random.choice(locations),
        "salary": round(random.uniform(100000, 500000), 2),
        "company": random.choice(companies),
        "job_type": random.choice(job_types),
    }

for i in range(40):
    job_data = generate_dummy_job()
    response = requests.post(url, json=job_data)
    if response.status_code == 201:
        print(f"Job {i+1} created successfully")
    else:
        print(f"Failed to create job {i+1}: {response.status_code} - {response.text}")

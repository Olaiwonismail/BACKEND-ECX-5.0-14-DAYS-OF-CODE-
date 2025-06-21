# BACKEND-ECX-5.0-14-DAYS-OF-CODE-

A modular FastAPI project template with authentication, user roles, job posting, and filtering functionality.

## Features

- User authentication (signup, login) with JWT tokens
- Role-based access control (applicant, employer)
- Employer job posting management (CRUD)
- Applicant job search and filtering with pagination
- SQLAlchemy ORM with SQLite (default, configurable)
- Environment-based configuration
- CORS enabled for frontend integration

## Project Structure

```
my-fastapi-blueprint/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── index.py
│       ├── employer/
│       │   └── jobs.py
│       └── applicant/
│           └── jobs.py
├── main.py
├── requirements.txt
├── .env
├── get_dummy_job_postings.py
└── README.md
```

## Setup

1. **Clone the repository**

   ```sh
   git clone <repo-url>
   cd my-fastapi-blueprint
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the root directory:

   ```
   APP_NAME=My FastAPI App
   APP_VERSION=0.1.0
   DATABASE_URI=sqlite:///./test.db
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ```

4. **Run the application**

   ```sh
   uvicorn main:app --reload
   ```

5. **API Documentation**

   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## Dummy Data

To populate the database with dummy job postings, run:

```sh
python get_dummy_job_postings.py
```

## License

MIT License
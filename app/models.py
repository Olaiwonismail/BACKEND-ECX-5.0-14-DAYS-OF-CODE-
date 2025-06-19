from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base, engine

class Table(Base):
    """SQLAlchemy model for an Item."""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}')>"

class User(Base):
    """SQLAlchemy model for a User."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="user")  
    hashed_password = Column(String)
    

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

# You can add a function to create tables if they don't exist
def create_db_tables():
    """Creates all defined database tables."""
    Base.metadata.create_all(bind=engine) # Use the engine from database.py if not already bound
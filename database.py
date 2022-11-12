from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a database engine
engine = create_engine('sqlite:///item.db', echo=True)

Base = declarative_base()

# Create a session
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
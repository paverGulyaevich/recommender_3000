# This is a script for initializing SQLAlchemy and creating sessions.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a URL object to connect to DB
SQLALCHEMY_DATABASE_URL = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"
# Create engine and link it to the URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Instantiate a Session maker object used to create sessions with required parameters
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a parental class Base from which other classes will be inherited
Base = declarative_base()

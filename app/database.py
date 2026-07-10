from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv



load_dotenv()

DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')

# SQLALCHEMY_DB_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/ApiMon DB'


engine = create_engine(SQLALCHEMY_DB_URL) # responsible for connection

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # ???What is this???

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

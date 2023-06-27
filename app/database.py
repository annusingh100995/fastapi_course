from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
from .config import settings


 
#Coonection string for sql alchemy
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address>/<hostname>:<port number>/<databas_name>
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:annu1234@localhost:5432/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Func to get connected to db
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()


"""
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi',user='postgres', password='annu1234',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfully connected to database ")
        break

    except Exception as error:
        print("Failed to connect to DB")
        print("Error", error)
        time.sleep(2)
"""
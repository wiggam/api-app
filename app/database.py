# from FastAPI documentation : https://fastapi.tiangolo.com/tutorial/sql-databases/
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# imports to connect to DB if running raw SQL code
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# importing config file to use env variables
from .config import settings

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# From FastAPI documentation, used during every request
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# If we were running raw SQL and not using SQLAlchemy ORM this would be the following code to connect to the Postgres DB
# connecting to Postgres database (uses psycopg2, and psycopg2.extras imports)
# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('Database connection was successful')
# except Exception as error:
#     print('Connecting to database failed')
#     print("Error: ", error)
#     time.sleep(2)
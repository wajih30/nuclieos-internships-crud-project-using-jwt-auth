from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config



db_connection=Config().get_db_url()

engine=create_engine(db_connection)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base=declarative_base()

 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://postgres:kyrie123@localhost:5432/course_platform")

    def get_db_url(self):
        return self.database_url

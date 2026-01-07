# check.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Test model
class TestModel(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    created_at: datetime = datetime.now()

if __name__ == "__main__":
    try:
        test_instance = TestModel(name="Alice", email="alice@example.com", age=25)
        print("Pydantic import is working!")
        # Use model_dump_json for Pydantic v2
        print(test_instance.model_dump_json(indent=4))
    except Exception as e:
        print("Something went wrong:", e)

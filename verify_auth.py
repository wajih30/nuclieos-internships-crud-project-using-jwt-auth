from fastapi.testclient import TestClient
from main import app
from db.db import get_db, base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
import pytest

# Use a separate test database or just the current one if acceptable for this verification 
# (Since it's a dev env, using current one is often easiest for quick verify, but risky if data matters. 
# However, "beginner friendly" implies we can probably test on dev db or mock it.)

# For this check, we will use the app and try to signup a random user.
import random
import string

client = TestClient(app)

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_signup_login():
    email = f"test_{get_random_string(5)}@example.com"
    password = "password123"
    name = "Test User"
    role = "Student"

    # Signup
    response = client.post("/auth/signup", json={
        "name": name,
        "email": email,
        "password": password,
        "role": role
    })
    
    print(f"Signup Status: {response.status_code}")
    print(f"Signup Response: {response.json()}")
    
    if response.status_code != 200:
        print("Signup failed!")
        return

    # Login
    response = client.post("/auth/login", data={
        "username": email,
        "password": password
    })
    
    print(f"Login Status: {response.status_code}")
    print(f"Login Response: {response.json()}")
    
    if response.status_code == 200:
        print("Login Successful! Token received.")
        assert "access_token" in response.json()
    else:
        print("Login failed!")

if __name__ == "__main__":
    try:
        test_signup_login()
    except Exception as e:
        print(f"An error occurred: {e}")

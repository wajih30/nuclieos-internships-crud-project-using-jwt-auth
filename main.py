from fastapi import FastAPI
from db.db import base, engine

from routes.student_routes import student_router 
from routes.teacher_routes import teacher_router
from routes.user_routes import user_router   # if you have one

from routes.auth_routes import auth_router

app = FastAPI(
    title="Online Course Platform",
    version="1.0.0"
)



# Register routers
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(user_router)   # optional

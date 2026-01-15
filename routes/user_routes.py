from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db  
from services import users_services, courses_services, enrollment_services, lessons_services, quiz_services,quiz_score_service
from Schemas import userschemas, coursesschemas, enrollmentschemas, lessonsschema, quizschema


app = FastAPI()
user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/register", response_model=userschemas.UserResponse)
def register_user(user: userschemas.UserBase, db: Session = Depends(get_db)):
    user_service = users_services.User(db)
    return user_service.create_user(user.name,user.email,user.role)

@user_router.get("/{user_id}", response_model=userschemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = users_services.User(db)
    user_obj = user_service.read_user_by_id(user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj

@user_router.delete("/{user_id}")
def delete_user(user_id:int,db: Session = Depends(get_db)):
    del_user=users_services.User(db).delete_user(user_id)
    return del_user




from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class EnrollmentBase(BaseModel):
    CourseId:int
    InstructorId:int




class EnrollmentUpdate(BaseModel):
    StudentId: Optional[int] = None
    CourseId: Optional[int] = None
    InstructorId:Optional[int]= None


class EnrollmentRating(BaseModel):
    StudentId: int
    CourseId : int
    InstructorId:int
    rating : int

class EnrollmentRatingResponse(BaseModel):
    Enrollmentnumber:int
    StudentId: int
    CourseId: int
    InstructorId : int
    rating:int

    created_at: datetime 

    class Config:
        orm_mode= True    
    



class EnrollmentResponse(BaseModel):
    Enrollmentnumber:int
    StudentId: int
    CourseId: int
    InstructorId : int

    created_at: datetime 

    class Config:
        orm_mode= True







from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class CourseBase(BaseModel):
    CourseName: str
    InstructorId : int
    Categoryid : int

class CourseCategory(BaseModel):
    Categoryid: int



class CourseUpdate(BaseModel):
    CourseName: Optional[str] = None
    InstructorId: Optional[int] = None
    Categoryid  : Optional[int] = None




class CourseResponse(CourseBase):
    courseId:int
    ratings:Optional[float|None]
    created_at: datetime 

    class Config:
        orm_mode= True







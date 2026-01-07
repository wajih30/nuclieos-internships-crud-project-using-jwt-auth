from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class LessonsBase(BaseModel):
    lessonName: str
    




class LessonsUpdate(BaseModel):
    lessonName : Optional[str] = None
    





class LessonsResponse(LessonsBase):
    lessonnumber:int
    courseId : int
    InstructorId:int
    created_at: datetime 

    class Config:
        orm_mode= True







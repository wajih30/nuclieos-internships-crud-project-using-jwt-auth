from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class QuizBase(BaseModel):
    QuizTopic: str
    






class QuizUpdate(BaseModel):
    QuizTopic: Optional[str] = None






class QuizResponse(QuizBase):
    QuizId: int
    created_at: datetime 
    InstructorId: int
    CourseId:int

    class Config:
        orm_mode= True



class QuizScoreBase(BaseModel): 
    QuizScore : int



class ScoreResponse(BaseModel):
    QuizId: int
    StudentId : int
    QuizScore: int
    CourseId : int
    InstructorId: int
    attempted_at: datetime
    class Config:
        orm_mode=True


# Quiz Generation Schemas
class QuizGenerationRequest(BaseModel):
    instructions: str  # Natural language instructions from user


class QuestionData(BaseModel):
    QuestionId: int
    QuizId: int
    Questions: dict  # The questions JSON data
    
    class Config:
        orm_mode = True


class QuizGenerationResponse(BaseModel):
    quiz: QuizResponse
    questions: QuestionData
    question_count: int
    
    class Config:
        orm_mode = True













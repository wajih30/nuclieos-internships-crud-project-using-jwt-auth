from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.db import base


class Quiz(base):
    __tablename__ = "Quizzes"

    QuizId = Column(Integer, primary_key=True, index=True)
    QuizTopic = Column(String, nullable=False, unique=True)
    CourseId = Column(Integer, ForeignKey("Courses.courseId"), nullable=False)
    InstructorId = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")

    



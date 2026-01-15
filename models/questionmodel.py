from sqlalchemy import Column, Integer, JSON, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.db import base


class Question(base):
    __tablename__ = "Questions"

    QuestionId = Column(Integer, primary_key=True, index=True)
    QuizId = Column(Integer, ForeignKey("Quizzes.QuizId", ondelete="CASCADE"), nullable=False, index=True)
    Questions = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
        
    quiz = relationship("Quiz", back_populates="questions")


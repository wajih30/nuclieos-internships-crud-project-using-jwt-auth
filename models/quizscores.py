from sqlalchemy import Column, Integer, String , DateTime, func,ForeignKey,PrimaryKeyConstraint
from db.db import base


class QuizScore(base):
    __tablename__= "QuizScore"

    QuizId=Column(Integer,ForeignKey("Quizzes.QuizId"), index=True)
    StudentId=Column(Integer,ForeignKey("Users.id"))
    QuizScore=Column(Integer,nullable=True)
    CourseId=Column(Integer,ForeignKey("Courses.courseId"),nullable=False)
    InstructorId=Column(Integer)
    attempted_at= Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        PrimaryKeyConstraint('QuizId', 'StudentId', name='quizscore_pk'),
    )    





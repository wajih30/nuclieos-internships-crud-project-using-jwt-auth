from sqlalchemy import Column, Integer, String , DateTime, func,ForeignKey,PrimaryKeyConstraint,Sequence
from db.db import base


class Lessons(base):
    __tablename__= "Lessons"

    lessonnumber=Column(Integer,Sequence('lessonnumber_seq'), index=True)
    lessonName=Column(String,nullable=False,unique=True)
    courseId=Column(Integer,ForeignKey("Courses.courseId"),nullable=False)
    InstructorId=Column(Integer,nullable=False)
    created_at= Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        PrimaryKeyConstraint('lessonnumber', 'courseId', name='lessons_pk'),
    )
    



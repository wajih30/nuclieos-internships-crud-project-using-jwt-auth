from sqlalchemy import Column, Integer, String , DateTime, func,ForeignKey
from db.db import base


class Enrollments(base):
    __tablename__= "Enrollments"

    Enrollmentnumber=Column(Integer,primary_key=True, index=True)
    StudentId=Column(Integer,nullable=False)
    CourseId=Column(Integer,ForeignKey("Courses.courseId"),nullable=False)
    InstructorId=Column(Integer,nullable=False)
    rating=Column(Integer,nullable=True)
    created_at= Column(DateTime(timezone=True), server_default=func.now())


    


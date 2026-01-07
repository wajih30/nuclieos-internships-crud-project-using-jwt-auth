from sqlalchemy import Column, Integer, String , DateTime, func,ForeignKey

from db.db import base


class Courses(base):
    __tablename__= "Courses"

    courseId=Column(Integer,primary_key=True, index=True)
    CourseName=Column(String,nullable=False,unique=True)
    Categoryid=Column(Integer,ForeignKey("Category.CategoryId"),nullable=False)
    InstructorId=Column(Integer,ForeignKey("Users.id"),nullable=False)
    ratings=Column(Integer,nullable=True)
    created_at= Column(DateTime(timezone=True), server_default=func.now())









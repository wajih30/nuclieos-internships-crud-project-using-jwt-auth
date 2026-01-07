from sqlalchemy.orm import Session
from sqlalchemy import func
from models import usermodel,coursesmodel
from Schemas import coursesschemas

class Courses():
    def __init__(self,db:Session):
        self.db=db

    def create_course(self,course_name:str, instructor_id: int,category_id:int):
        
        instructor = (self.db.query(usermodel.Users).filter(usermodel.Users.id == instructor_id).first())
        if not instructor:
            raise ValueError("Instructor not found")

        
        if instructor.role.lower() != "teacher":
            raise ValueError("Only teachers can create courses")

        
        db_course = coursesmodel.Courses(
            CourseName=course_name,
            InstructorId=instructor_id,
            Categoryid=category_id
        )

        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)

        return db_course
    
    def read_courses(self):
        return self.db.query(coursesmodel.Courses).all()
    
    def read_courses_by_id(self,course_id):
        return self.db.query(coursesmodel.Courses).filter(coursesmodel.Courses.courseId==course_id).first()
    
    def read_courses_by_teacher(self,instructor_id):
        return self.db.query(coursesmodel.Courses).filter(coursesmodel.Courses.InstructorId==instructor_id).all()
    
    def read_course_by_category(self,course_category:int):
        return self.db.query(coursesmodel.Courses).filter(coursesmodel.Courses.Categoryid==course_category).all()

    def update_course(self,course_id: int, course: coursesschemas.CourseUpdate):
        db_user = self.db.query(coursesmodel.Courses).filter(coursesmodel.Courses.courseId == course_id).first()
        
        
        if not db_user:
           return None
        new_instructor= self.db.query(usermodel.Users).filter(usermodel.Users.id == course.InstructorId).first()
        
        
        if new_instructor.role.lower()!= "teacher":
            raise Exception("Only teachers can update courses")

        db_user.CourseName = course.CourseName

        db_user.InstructorId=course.InstructorId
        db_user.Categoryid=course.Categoryid
        self.db.commit()
        self.db.refresh(db_user)
        return db_user    
    

    def get_course_rating(self, course_id: int, instructor_id: int):
        course = self.db.query(coursesmodel.Courses).filter(coursesmodel.Courses.courseId == course_id,coursesmodel.Courses.InstructorId == instructor_id).first()

        if not course:
            raise ValueError("Course does not exist")

        return course

    


    def delete_course(self, course_id: int, user_id: int):
    
        db_course = self.db.query(coursesmodel.Courses).filter(coursesmodel.Courses.courseId == course_id).first()
        if not db_course:
           return None
        user = self.db.query(usermodel.Users).filter(usermodel.Users.id == user_id).first()
        if not user or user.role.lower() != "teacher":
           raise Exception("Only teachers can delete courses")

        if db_course.InstructorId != user_id:
           raise Exception("You can only delete courses you created")

        self.db.delete(db_course)
        self.db.commit()
        return db_course
    









    


from sqlalchemy.orm import Session
from models import lessonsmodel,coursesmodel
from Schemas import lessonsschema

class Lessons():
    def __init__(self,db:Session):
        self.db=db

    def create_lesson(self,course_id:int,instructor_id:int,lesson:lessonsschema.LessonsBase):
        course = self.db.query(coursesmodel.Courses).filter(coursesmodel.Courses.courseId == course_id).first()
        if not course:
            raise Exception("Course does not exist")
        db_lessons= lessonsmodel.Lessons(lessonName=lesson.lessonName,courseId=course_id,InstructorId=instructor_id)
        self.db.add(db_lessons)
        self.db.commit()
        self.db.refresh(db_lessons)
        return db_lessons
    
    def read_lesson(self):
        return self.db.query(lessonsmodel).all()
    
    def read_lesson_by_id(self, lessonnumber: int, course_id: int):
    
        lesson = (self.db.query(lessonsmodel.Lessons).filter(lessonsmodel.Lessons.lessonnumber == lessonnumber,lessonsmodel.Lessons.courseId == course_id).first())
        return lesson
    

    def read_lesson_by_course(self, course_id: int, instructor_id: int):
    
        lesson = (self.db.query(lessonsmodel.Lessons).filter(lessonsmodel.Lessons.courseId == course_id,lessonsmodel.Lessons.InstructorId == instructor_id).all())
        return lesson

    def update_lesson(self, lessonnumber: int, course_id: int, lesson: lessonsschema.LessonsBase):
        db_lesson = (self.db.query(lessonsmodel.Lessons).filter(lessonsmodel.Lessons.lessonnumber == lessonnumber,lessonsmodel.Lessons.courseId == course_id).first())
        if not db_lesson:
            return None


        db_lesson.lessonName = lesson.lessonName
        self.db.commit()
        self.db.refresh(db_lesson)
        return db_lesson


    
    
    



    def delete_lesson(self,course_id:int,lessonnumber:int):
        db_lesson = (self.db.query(lessonsmodel.Lessons).filter(lessonsmodel.Lessons.lessonnumber == lessonnumber,lessonsmodel.Lessons.courseId == course_id).first())

        if not db_lesson:
           return None
        self.db.delete(db_lesson)
        self.db.commit()
        return db_lesson






    


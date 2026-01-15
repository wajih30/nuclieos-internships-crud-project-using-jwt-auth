from sqlalchemy.orm import Session
from models import quizmodel,usermodel,coursesmodel
from Schemas import quizschema

class Quiz():
    def __init__(self,db:Session):
        self.db=db

    def create_quiz(self,course_id:int,instructor_id:int,topic:str):
        get_user=(self.db.query(usermodel.Users).filter(usermodel.Users.id==instructor_id).first())
        if not get_user:
           raise ValueError("User not found")
        if get_user.role!= "teacher":
            raise ValueError("Only teachers can create quizzes")
        get_course=(self.db.query(coursesmodel.Courses).filter(coursesmodel.Courses.courseId==course_id,coursesmodel.Courses.InstructorId==instructor_id).first())
        
        if get_course is None:
            raise ValueError("Course does not exist")


        db_quiz = quizmodel.Quiz(QuizTopic=topic, CourseId=course_id,InstructorId=instructor_id)
        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)
        return db_quiz
    
    def read_quiz(self,course_id:int):
        return self.db.query(quizmodel.Quiz).filter(quizmodel.Quiz.CourseId==course_id).all()
    
    def read_quiz_by_id(self,course_id:int,quiz_id:int):
        return self.db.query(quizmodel.Quiz).filter(quizmodel.Quiz.QuizId==quiz_id,quizmodel.Quiz.CourseId==course_id).first()
    
    def update_quiz(self,quiz_id: int,course_id:int, quiz: quizschema.QuizUpdate):
        db_quiz = self.db.query(quizmodel.Quiz).filter(quizmodel.Quiz.QuizId == quiz_id,quizmodel.Quiz.CourseId==course_id).first()
        get_instructor=self.db.query(usermodel.Users).filter(usermodel.Users.id==quiz.InstructorId).first()
        if not db_quiz:
           return None
        if get_instructor.role!= "teacher":
            raise ValueError("Only Teachers can update quizzes.")
        

        

        db_quiz.QuizTopic = quiz.QuizTopic

        db_quiz.CourseId = quiz.CourseId
        db_quiz.InstructorId=quiz.InstructorId
        self.db.commit()
        self.db.refresh(db_quiz)
        return db_quiz   


    
    
    



    def delete_quiz(self,quiz_id: int,course_id:int):
        db_user = self.db.query(quizmodel.Quiz).filter(quizmodel.Quiz.QuizId == quiz_id,quizmodel.Quiz.CourseId==course_id).first()
        if not db_user:
           return None
        self.db.delete(db_user)
        self.db.commit()
        return db_user






    


from sqlalchemy.orm import Session
from models import quizmodel,usermodel,coursesmodel,quizscores
from Schemas import quizschema

class Quiz():
    def __init__(self,db:Session):
        self.db=db

    def attempt_quiz(self,quiz_id:int,course_id:int,instructor_id:int,student_id:int,score:int):
        
        quiz_check=self.db.query(quizmodel.Quiz).filter(quizmodel.Quiz.QuizId==quiz_id,quizmodel.Quiz.CourseId==course_id,quizmodel.Quiz.InstructorId==instructor_id).first()
        if not quiz_check:
            raise ValueError("Quiz Does not exist")


        db_quiz = quizscores.QuizScore(QuizId=quiz_id,CourseId=course_id,InstructorId=instructor_id,StudentId=student_id,QuizScore=score)

        self.db.add(db_quiz)
        self.db.commit()
        self.db.refresh(db_quiz)
        return db_quiz
    
    def read_quizscores(self):
        return self.db.query(quizscores.QuizScore).all()
    
    def read_quiz_by_student(self,course_id:int,student_id:int,quiz_id:int):
        return self.db.query(quizscores.QuizScore).filter(quizscores.QuizScore.CourseId==course_id,quizscores.QuizScore.StudentId==student_id,quizscores.QuizScore.QuizId==quiz_id).first()
    






    


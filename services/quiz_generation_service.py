import json
import re
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import quizmodel, questionmodel, usermodel, coursesmodel
from services.groq_service import GroqService
from services.quiz_prompt_template import build_quiz_prompt


class QuizGenerationService:
    
    
    def __init__(self, db: Session):
        self.db = db
        self.groq_service = GroqService()
    
    def check_instructor_exists(self, instructor_id: int) -> bool:
        
        instructor = self.db.query(usermodel.Users).filter(
            usermodel.Users.id == instructor_id
        ).first()
        
        return instructor is not None
    
    def check_course_exists(self, course_name: str, instructor_id: int) -> bool:
        
        normalized = str(course_name).strip()
        course = self.db.query(coursesmodel.Courses).filter(
            func.lower(coursesmodel.Courses.CourseName) == func.lower(normalized),
            coursesmodel.Courses.InstructorId == instructor_id,
        ).first()
        
        return course is not None
    
    def get_course(self, course_name: str, instructor_id: int):
     
        normalized = str(course_name).strip()
        course = self.db.query(coursesmodel.Courses).filter(
            func.lower(coursesmodel.Courses.CourseName) == func.lower(normalized),
            coursesmodel.Courses.InstructorId == instructor_id,
        ).first()
        
        return course
    
    def clean_json_response(self, response: str) -> str:
       
        response = response.replace('```json', '')
        response = response.replace('```', '')
        response = response.strip()
        
        
        start_pos = response.find('{')
        end_pos = response.rfind('}')
        
        if start_pos != -1 and end_pos != -1 and end_pos > start_pos:
            return response[start_pos:end_pos + 1]
        
        return response
    
    def validate_quiz_data(self, quiz_data: dict) -> tuple:
        
        if "instructor_id" not in quiz_data or not quiz_data["instructor_id"]:
            return False, "Could not find instructor ID in the AI response"
        
        if "course_name" not in quiz_data or not quiz_data["course_name"]:
            return False, "Could not find course name in the AI response"
        
        if "quiz_topic" not in quiz_data or not quiz_data["quiz_topic"]:
            return False, "Could not find quiz topic in the AI response"
        
        if "question_count" not in quiz_data or not isinstance(quiz_data["question_count"], int) or quiz_data["question_count"] < 1 or quiz_data["question_count"] > 20:
            return False, "Number of questions must be between 1 and 20"
        
        if "questions" not in quiz_data or not quiz_data["questions"]:
            return False, "Could not find questions in the AI response"

        if len(quiz_data["questions"]) != quiz_data["question_count"]:
            return False, f"Number of questions in data ({len(quiz_data['questions'])}) does not match question_count ({quiz_data['question_count']})"


        instructor_id = int(quiz_data["instructor_id"])
        course_name = str(quiz_data["course_name"]).strip()
        
        
        if not self.check_instructor_exists(instructor_id):
            return False, f"Instructor with ID {instructor_id} does not exist"
        
        
        if not self.check_course_exists(course_name, instructor_id):
            return False, f"Course '{course_name}' not found for instructor {instructor_id}"
        
        return True, ""
    
    def generate_quiz(self, user_instructions: str) -> dict:
        
        prompt = build_quiz_prompt(user_instructions)
        ai_response = self.groq_service.generate_text(
            prompt=prompt,
            temperature=0.7,
            max_tokens=4000
        )
        
        
        cleaned_json = self.clean_json_response(ai_response)
        
        try:
            quiz_data = json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"AI response was not valid JSON. Error: {str(e)}")

        # Check if the response is an error response
        if "error" in quiz_data:
            raise ValueError(f"AI returned an error: {quiz_data['error']}")

        is_valid, error_msg = self.validate_quiz_data(quiz_data)
        if not is_valid:
            raise ValueError(error_msg)
        
        
        instructor_id = int(quiz_data["instructor_id"])
        course_name = str(quiz_data["course_name"]).strip()
        quiz_topic = str(quiz_data["quiz_topic"]).strip()
        
        
        course = self.get_course(course_name, instructor_id)
        
        
        new_quiz = quizmodel.Quiz(
            QuizTopic=quiz_topic,
            CourseId=course.courseId,
            InstructorId=instructor_id
        )
        
        
        self.db.add(new_quiz)
        self.db.commit()
        self.db.refresh(new_quiz)
        
        
        new_questions = questionmodel.Question(
            QuizId=new_quiz.QuizId,
            Questions=quiz_data["questions"]
        )
        
        
        self.db.add(new_questions)
        self.db.commit()
        self.db.refresh(new_questions)
        
       
        return {
            "quiz": {
                "QuizId": new_quiz.QuizId,
                "QuizTopic": new_quiz.QuizTopic,
                "CourseId": new_quiz.CourseId,
                "InstructorId": new_quiz.InstructorId,
                "created_at": new_quiz.created_at
            },
            "questions": {
                "QuestionId": new_questions.QuestionId,
                "QuizId": new_questions.QuizId,
                "Questions": new_questions.Questions
            },
            "question_count": len(quiz_data["questions"])
        }

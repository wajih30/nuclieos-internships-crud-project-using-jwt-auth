from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db  
from services import  courses_services, enrollment_services,quiz_score_service
from Schemas import  coursesschemas, enrollmentschemas, quizschema,categoryschemas




from services.auth import get_current_active_student  
from models.usermodel import Users

student_router = APIRouter(prefix="/student", tags=["Student"])


@student_router.post("/enroll", response_model=enrollmentschemas.EnrollmentResponse)
def enroll_course(enrollment: enrollmentschemas.EnrollmentBase,current_student: Users = Depends(get_current_active_student),  db: Session = Depends(get_db)):

    enroll_service = enrollment_services.EnrollmentsService(db)
    
    return enroll_service.create_enrollment(
        course_id=enrollment.CourseId,
        student_id=current_student.id, 
        instructor_id=enrollment.InstructorId
    )


@student_router.get("/courses", response_model=list[coursesschemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    course = courses_services.Courses(db)
    return course.read_courses()


@student_router.get("/courses/{category_id}", response_model=list[coursesschemas.CourseResponse])
def get_courses_by_category(category_id, db: Session = Depends(get_db)):
    course = courses_services.Courses(db)
    return course.read_course_by_category(category_id)



@student_router.get("/enrollments/{student_id}", response_model=list[enrollmentschemas.EnrollmentResponse])
def get_my_enrollments(student_id: int, db: Session = Depends(get_db)):
    enroll_service = enrollment_services.EnrollmentsService(db)
    return enroll_service.read_enrollments_by_student(student_id)


@student_router.post("/rate", response_model=enrollmentschemas.EnrollmentRatingResponse)
def rate_course(rate: enrollmentschemas.EnrollmentRating, db: Session = Depends(get_db)):
    enroll_service = enrollment_services.EnrollmentsService(db)
    updated = enroll_service.rate_course(rate.StudentId, rate.CourseId,rate.InstructorId, rate.rating) 
    return updated

@student_router.get("/courses/{course_id}/instructor/{instructor_id}/rating",response_model=coursesschemas.CourseResponse)
def view_course_rating(course_id: int,instructor_id: int,db: Session = Depends(get_db)):
    course_service = courses_services.Courses(db)
    rating = course_service.get_course_rating(course_id, instructor_id)

    return rating




@student_router.post("/instructor/{instructor_id}/course/{course_id}/quiz/{quiz_id}/student/{student_id}/attempt")
def attempt_quiz(quiz_attempt: quizschema.QuizScoreBase, course_id:int, quiz_id:int, student_id:int, instructor_id:int, db: Session = Depends(get_db)):
    quiz_service = quiz_score_service.Quiz(db)
    return quiz_service.attempt_quiz(quiz_id, course_id, instructor_id, student_id, quiz_attempt.QuizScore)

@student_router.get("/quizscore/{course_id}/quiz/{quiz_id}/student/{student_id}",response_model=quizschema.ScoreResponse)
def get_score_by_student(course_id:int,student_id:int,quiz_id:int,db:Session=Depends(get_db)):
    quiz_service = quiz_score_service.Quiz(db)
    return quiz_service.read_quiz_by_student(course_id,student_id,quiz_id)




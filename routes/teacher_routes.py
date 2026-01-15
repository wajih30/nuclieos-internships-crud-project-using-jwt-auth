from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db  
from services import  courses_services, enrollment_services,quiz_services,lessons_services,category_services,quiz_generation_service
from Schemas import  coursesschemas, enrollmentschemas, quizschema,categoryschemas,lessonsschema
from services.auth import get_current_active_teacher
from models.usermodel import Users

teacher_router = APIRouter(prefix="/teacher", tags=["Teacher"])

@teacher_router.post("/category",response_model=categoryschemas.CategoryResponse)
def create_category(category:categoryschemas.CategoryBase, current_teacher: Users = Depends(get_current_active_teacher), db:Session= Depends(get_db)):
    category_service=category_services.Category(db)
    return category_service.create_category(category.CategoryName)



@teacher_router.post("/courses", response_model=coursesschemas.CourseResponse)
def create_course(course: coursesschemas.CourseBase, current_teacher: Users = Depends(get_current_active_teacher), db: Session = Depends(get_db)):
    course_service = courses_services.Courses(db)
    return course_service.create_course(course.CourseName,course.InstructorId,course.Categoryid)

@teacher_router.get("/courses/{instructor_id}", response_model=list[coursesschemas.CourseResponse])
def get_my_courses(instructor_id: int, db: Session = Depends(get_db)):
    course_service = courses_services.Courses(db)
    return course_service.read_courses_by_teacher(instructor_id)



@teacher_router.delete("/{user_id}/courses/{course_id}")
def delete_course(course_id: int, user_id: int, current_teacher: Users = Depends(get_current_active_teacher), db: Session = Depends(get_db)):
    courses_service = courses_services.Courses(db)
    deleted = courses_service.delete_course(course_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}


@teacher_router.get("/enrollments/{instructor_id}", response_model=list[enrollmentschemas.EnrollmentResponse])
def get_enrollments(instructor_id: int, current_teacher: Users = Depends(get_current_active_teacher), db: Session = Depends(get_db)):
    enroll_service = enrollment_services.EnrollmentsService(db)
    return enroll_service.read_all_enrollments(instructor_id)


@teacher_router.post("/quizzes/instructor/{instructor_id}/{course_id}",response_model=quizschema.QuizResponse)
def create_quiz(instructor_id:int,course_id:int,quiz:quizschema.QuizBase, current_teacher: Users = Depends(get_current_active_teacher), db:Session=Depends(get_db)):
    quizz=quiz_services.Quiz(db)
    return quizz.create_quiz(course_id,instructor_id,quiz.QuizTopic)



@teacher_router.post("/lessons/{instructor_id}/{course_id}",response_model=lessonsschema.LessonsResponse)
def create_lessonn(instructor_id:int,course_id:int,lesson:lessonsschema.LessonsBase, current_teacher: Users = Depends(get_current_active_teacher), db:Session=Depends(get_db)):
    lesson_service=lessons_services.Lessons(db)
    return lesson_service.create_lesson(course_id,instructor_id,lesson)

@teacher_router.get("/lessons/{instructor_id}/{course_id}",response_model=list[lessonsschema.LessonsResponse])
def get_lesson(instructor_id:int,course_id:int, current_teacher: Users = Depends(get_current_active_teacher), db:Session=Depends(get_db)):
    lesson_service=lessons_services.Lessons(db)
    return lesson_service.read_lesson_by_course(course_id,instructor_id)


@teacher_router.post("/quizzes/generate", response_model=quizschema.QuizGenerationResponse)
def generate_quiz_with_ai(
    request: quizschema.QuizGenerationRequest,
    db: Session = Depends(get_db),
):
    """
    Public/test endpoint (NO LOGIN REQUIRED).
    Generate quiz using Groq AI based on natural language instructions.

    NOTE: If you want the secured version (teacher-only), use:
    `POST /teacher/quizzes/generate/secure`
    """
    try:
        quiz_gen_service = quiz_generation_service.QuizGenerationService(db)
        result = quiz_gen_service.generate_quiz(request.instructions)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")


@teacher_router.post("/quizzes/generate/secure", response_model=quizschema.QuizGenerationResponse)
def generate_quiz_with_ai_secure(
    request: quizschema.QuizGenerationRequest,
    current_teacher: Users = Depends(get_current_active_teacher),
    db: Session = Depends(get_db),
):
    """
    Secured endpoint (TEACHER LOGIN REQUIRED).
    Same behavior as `POST /teacher/quizzes/generate` but enforces teacher auth.
    """
    try:
        quiz_gen_service = quiz_generation_service.QuizGenerationService(db)
        result = quiz_gen_service.generate_quiz(request.instructions)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")



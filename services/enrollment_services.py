from sqlalchemy.orm import Session
from sqlalchemy import func
from models import enrollmentsmodel, coursesmodel
from Schemas import enrollmentschemas

class EnrollmentsService:
    def __init__(self, db: Session):
        self.db = db

    
    def create_enrollment(self, course_id: int, student_id: int,instructor_id:int):
        course = self.db.query(coursesmodel.Courses).filter(coursesmodel.Courses.courseId == course_id,coursesmodel.Courses.InstructorId==instructor_id).first()
        if not course:
            raise Exception("Course does not exist")

        
        existing = self.db.query(enrollmentsmodel.Enrollments).filter(enrollmentsmodel.Enrollments.StudentId == student_id,enrollmentsmodel.Enrollments.CourseId == course_id,enrollmentsmodel.Enrollments.InstructorId==instructor_id).first()
        if existing:
            raise Exception("Student already enrolled in this course")

        enrollment = enrollmentsmodel.Enrollments(
            StudentId=student_id,
            CourseId=course_id,
            InstructorId=instructor_id
        )
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    
    def read_all_enrollments(self,instructor_id):
        return self.db.query(enrollmentsmodel.Enrollments).filter(enrollmentsmodel.Enrollments.InstructorId==instructor_id).all()

    
    def read_enrollments_by_student(self, student_id: int):
        enrollments = self.db.query(enrollmentsmodel.Enrollments).filter(enrollmentsmodel.Enrollments.StudentId == student_id).all()
        return enrollments

    
    def update_enrollment(self, enrollment_id: int,student_id:int, enrollment: enrollmentschemas.EnrollmentUpdate):
        enrollment = self.db.query(enrollmentsmodel.Enrollments).filter(enrollmentsmodel.Enrollments.Enrollmentnumber == enrollment_id,enrollmentsmodel.Enrollments.StudentId==student_id).first()
        if not enrollment:
            return None

        
        enrollment.StudentId = enrollment.StudentId

        enrollment.CourseId = enrollment.CourseId

        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment
    

    def rate_course(
        self,
        student_id: int,
        course_id: int,
        instructor_id: int,
        rating: int
    ):
        enrollment = self.db.query(enrollmentsmodel.Enrollments).filter(
            enrollmentsmodel.Enrollments.StudentId == student_id,
            enrollmentsmodel.Enrollments.CourseId == course_id,
            enrollmentsmodel.Enrollments.InstructorId == instructor_id
        ).first()

        if not enrollment:
            raise ValueError("Enrollment not found")

        # 1️⃣ Update student's rating
        enrollment.rating = rating
        self.db.commit()

        # 2️⃣ Recalculate course average automatically
        self._update_course_rating(course_id, instructor_id)

        self.db.refresh(enrollment)
        return enrollment

    
    def _update_course_rating(self, course_id: int, instructor_id: int):
        avg_rating = self.db.query(func.avg(enrollmentsmodel.Enrollments.rating)).filter(
            enrollmentsmodel.Enrollments.CourseId == course_id,
            enrollmentsmodel.Enrollments.InstructorId == instructor_id
        ).scalar()

        course = self.db.query(coursesmodel.Courses).filter(
            coursesmodel.Courses.courseId == course_id,
            coursesmodel.Courses.InstructorId == instructor_id
        ).first()

        if course:
            course.ratings = avg_rating
            self.db.commit()


    
    def delete_enrollment(self, student_id:int,course_id:int):
        enrollment = self.db.query(enrollmentsmodel.Enrollments
        ).filter(enrollmentsmodel.Enrollments.StudentId == student_id
        ,enrollmentsmodel.Enrollments.CourseId==course_id
         ).first()
        if not enrollment:
            return None

        self.db.delete(enrollment)
        self.db.commit()
        return enrollment

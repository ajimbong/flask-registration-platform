from datetime import datetime

from config import db


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    matricule = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(250), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class Program(db.Model):
    __tablename__ = 'program'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    tuition = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    course_code = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class ProgramCourse(db.Model):
    __tablename__ = 'program_course'

    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.now())

class Registration(db.Model):
    __tablename__ = 'registration'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    verification_status = db.Column(db.String(50), nullable=False, default='PENDING')
    has_paid = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class RegistrationDocument(db.Model):
    __tablename__ = 'registration_document'

    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    document_link = db.Column(db.String(250), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())





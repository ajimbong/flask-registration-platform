from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Student, Program, Registration, RegistrationDocument
from functools import wraps

bp = Blueprint('main', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)

    return decorated_function


@bp.route('/')
def home():
    programs = Program.query.all()
    return render_template("index.html", programs=programs)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        student = Student(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(student)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        student = Student.query.filter_by(email=email).first()

        if student and check_password_hash(student.password, password):
            session['user_id'] = student.id
            flash('Login successful.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))


@bp.route('/program/<int:program_id>')
def program_detail(program_id):
    program = Program.query.get_or_404(program_id)
    courses = [pc.course for pc in program.program_courses]
    return render_template('program_detail.html', program=program, courses=courses)


@bp.route('/register_program/<int:program_id>', methods=['GET', 'POST'])
@login_required
def register_program(program_id):
    if request.method == 'POST':
        student_id = session['user_id']
        documents = request.files.getlist('documents')

        registration = Registration(student_id=student_id, program_id=program_id)
        db.session.add(registration)
        db.session.commit()

        for document in documents:
            document_link = f"uploads/{document.filename}"
            document.save(document_link)
            registration_document = RegistrationDocument(registration_id=registration.id, student_id=student_id,
                                                         document_link=document_link)
            db.session.add(registration_document)

        db.session.commit()
        flash('Registration submitted successfully. Wait for your documents to be verified.', 'success')
        return redirect(url_for('main.profile'))

    program = Program.query.get_or_404(program_id)
    return render_template('register_program.html', program=program)


@bp.route('/profile')
@login_required
def profile():
    student_id = session['user_id']
    student = Student.query.get_or_404(student_id)
    registrations = Registration.query.filter_by(student_id=student_id).all()
    return render_template('profile.html', student=student, registrations=registrations)
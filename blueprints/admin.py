from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from models import Admin, Registration, RegistrationDocument

admin_bp = Blueprint('admin', __name__)


# Admin login route
@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin.home'))
        flash('Invalid email or password')
    return render_template('admin/login.html')


# Admin home route
@admin_bp.route('/admin')
def home():
    if 'admin_id' not in session:
        return redirect(url_for('admin.login'))

    page = request.args.get('page', 1, type=int)
    registrations = Registration.query.paginate(page=page, per_page=10)
    return render_template('admin/index.html', registrations=registrations)


# View registration details
@admin_bp.route('/admin/registration/<int:registration_id>')
def registration_detail(registration_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin.login'))

    registration = Registration.query.get_or_404(registration_id)
    documents = RegistrationDocument.query.filter_by(registration_id=registration.id).all()
    return render_template('admin/registration_detail.html', registration=registration, documents=documents)


# Accept registration
@admin_bp.route('/admin/registration/<int:registration_id>/accept', methods=['POST'])
def accept_registration(registration_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin.login'))

    registration = Registration.query.get_or_404(registration_id)
    registration.verification_status = 'VERIFIED'
    db.session.commit()
    return redirect(url_for('admin.home'))


# Decline registration
@admin_bp.route('/admin/registration/<int:registration_id>/decline', methods=['POST'])
def decline_registration(registration_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin.login'))

    registration = Registration.query.get_or_404(registration_id)
    registration.verification_status = 'DECLINED'
    db.session.commit()
    return redirect(url_for('admin.home'))

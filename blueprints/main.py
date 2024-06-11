from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template("index.html")


@bp.route('/program/<int:program_id>')
def program_details(program_id):

    return f'<h1>Program details: {program_id}</h1>'
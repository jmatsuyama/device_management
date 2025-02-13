from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
from functools import wraps

auth = Blueprint('auth', __name__)

def jeis_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.organization != 'JEIS':
            flash('このページにアクセスする権限がありません。', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def jr_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.organization != 'JR':
            flash('このページにアクセスする権限がありません。', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.organization == 'JEIS':
            return redirect(url_for('device.list_devices'))
        else:
            return redirect(url_for('locker.reception'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')

        user = User.query.filter_by(user_id=user_id).first()

        if not user or not check_password_hash(user.password, password):
            flash('ユーザーIDまたはパスワードが正しくありません。', 'error')
            return redirect(url_for('auth.login'))

        login_user(user)
        
        if user.organization == 'JEIS':
            return redirect(url_for('device.list_devices'))
        else:
            return redirect(url_for('locker.reception'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
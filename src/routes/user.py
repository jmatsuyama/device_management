from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from models import User, db
from routes.auth import jeis_required

user = Blueprint('user', __name__)

@user.route('/users')
@login_required
@jeis_required
def list_users():
    users = User.query.all()
    return render_template('users_new.html', users=users)

@user.route('/add_user', methods=['GET', 'POST'])
@login_required
@jeis_required
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        organization = request.form.get('organization')

        if not all([name, user_id, password, organization]):
            flash('すべての項目を入力してください。', 'error')
            return redirect(url_for('user.add_user'))

        if User.query.filter_by(user_id=user_id).first():
            flash('このユーザーIDは既に使用されています。', 'error')
            return redirect(url_for('user.add_user'))

        user = User(
            name=name,
            user_id=user_id,
            password=generate_password_hash(password),
            organization=organization
        )
        db.session.add(user)
        db.session.commit()

        flash('ユーザーを追加しました。', 'success')
        return redirect(url_for('user.list_users'))

    return render_template('add_user.html')

@user.route('/delete_user/<int:id>')
@login_required
@jeis_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    # 管理者は削除不可
    if user.user_id == 'admin':
        flash('管理者は削除できません。', 'error')
        return redirect(url_for('user.list_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('ユーザーを削除しました。', 'success')
    return redirect(url_for('user.list_users'))
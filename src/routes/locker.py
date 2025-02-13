from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import Locker, Device, db
from routes.auth import jeis_required, jr_required
from datetime import datetime, timedelta
import pytz
import random
import string

locker = Blueprint('locker', __name__)

def generate_password():
    return ''.join(random.choices(string.digits, k=4))

@locker.route('/lockers')
@login_required
@jeis_required
def list_lockers():
    lockers = Locker.query.all()
    devices = Device.query.all()
    return render_template('lockers_new.html', lockers=lockers, devices=devices)

@locker.route('/toggle_locker/<int:id>')
@login_required
@jeis_required
def toggle_locker(id):
    locker = Locker.query.get_or_404(id)
    locker.is_locked = not locker.is_locked
    locker.last_updated = datetime.now(pytz.UTC)
    db.session.commit()
    return redirect(url_for('locker.list_lockers'))

@locker.route('/get_available_lockers')
@login_required
def get_available_lockers():
    lockers = Locker.query.filter_by(device_id=None).all()
    return jsonify([{'id': l.id, 'name': l.name} for l in lockers])

@locker.route('/issue_password', methods=['POST'])
@login_required
@jeis_required
def issue_password():
    locker_id = request.form.get('locker_id')
    device_id = request.form.get('device_id')
    expiry_hours = int(request.form.get('expiry_hours', 24))

    if not all([locker_id, device_id]):
        flash('ロッカーとデバイスを選択してください。', 'error')
        return redirect(url_for('locker.list_lockers'))

    locker = Locker.query.get_or_404(locker_id)
    device = Device.query.get_or_404(device_id)

    password = generate_password()
    expiry = datetime.now(pytz.UTC) + timedelta(hours=expiry_hours)

    locker.password = password
    locker.password_expiry = expiry
    locker.device_id = device.id
    locker.is_locked = True
    locker.last_updated = datetime.now(pytz.UTC)

    db.session.commit()

    flash(f'パスワードを発行しました: {password}', 'success')
    return redirect(url_for('locker.list_lockers'))

@locker.route('/reception')
@login_required
@jr_required
def reception():
    return render_template('reception.html')

@locker.route('/password_input', methods=['GET', 'POST'])
@login_required
@jr_required
def password_input():
    if request.method == 'POST':
        locker_id = request.form.get('locker_id')
        password = request.form.get('password')

        if not all([locker_id, password]):
            flash('ロッカーとパスワードを入力してください。', 'error')
            return redirect(url_for('locker.password_input'))

        locker = Locker.query.get_or_404(locker_id)
        now = datetime.now(pytz.UTC)

        if not locker.password or not locker.password_expiry:
            flash('このロッカーにはパスワードが設定されていません。', 'error')
        elif locker.password_expiry < now:
            flash('パスワードの有効期限が切れています。', 'error')
        elif locker.password != password:
            flash('パスワードが正しくありません。', 'error')
        else:
            locker.is_locked = False
            locker.password = None
            locker.password_expiry = None
            locker.last_updated = now
            db.session.commit()
            flash('ロッカーを解錠しました。', 'success')
            return redirect(url_for('locker.reception'))

    lockers = Locker.query.filter(
        Locker.password.isnot(None),
        Locker.password_expiry > datetime.now(pytz.UTC)
    ).all()
    return render_template('password_input.html', lockers=lockers)
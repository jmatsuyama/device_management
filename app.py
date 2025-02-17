from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, session
from functools import wraps
import sqlite3
import csv
from datetime import datetime, timedelta
from io import StringIO
import random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
DATABASE = 'devices.db'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('ログインが必要です')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        # 初期ロッカーデータの作成
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM lockers')
        if cursor.fetchone()[0] == 0:
            for i in range(1, 4):
                cursor.execute('INSERT INTO lockers (name) VALUES (?)', (f'ロッカー{i}',))
        db.commit()

def generate_password():
    return f"{random.randint(0, 9999):04d}"

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            session['organization'] = user['organization']
            flash('ログインしました')
            return redirect(url_for('home'))
        
        flash('ユーザーIDまたはパスワードが正しくありません')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('ログアウトしました')
    return redirect(url_for('login'))

@app.route('/users')
@login_required
def users():
    if session.get('organization') != 'JEIS':
        flash('権限がありません')
        return redirect(url_for('home'))
    
    db = get_db()
    users = db.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if session.get('organization') != 'JEIS':
        flash('権限がありません')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form['name']
        user_id = request.form['user_id']
        password = request.form['password']
        organization = request.form['organization']
        
        db = get_db()
        try:
            db.execute(
                'INSERT INTO users (name, user_id, password, organization) VALUES (?, ?, ?, ?)',
                (name, user_id, generate_password_hash(password), organization)
            )
            db.commit()
            flash('ユーザーが正常に登録されました')
            return redirect(url_for('users'))
        except sqlite3.IntegrityError:
            flash('そのユーザーIDは既に使用されています')
    
    return render_template('add_user.html')

@app.route('/users/delete/<int:id>')
@login_required
def delete_user(id):
    if session.get('organization') != 'JEIS':
        flash('権限がありません')
        return redirect(url_for('home'))
    
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (id,))
    db.commit()
    flash('ユーザーが削除されました')
    return redirect(url_for('users'))

@app.route('/devices')
@login_required
def devices():
    db = get_db()
    devices = db.execute('''
        SELECT d.*, l.name as locker_name 
        FROM devices d 
        LEFT JOIN lockers l ON d.locker_id = l.id 
        ORDER BY d.created_at DESC
    ''').fetchall()
    return render_template('devices.html', devices=devices)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        location = request.form['location']
        pc_id = request.form['pc_id']
        is_replacement = 1 if request.form.get('is_replacement') else 0

        db = get_db()
        db.execute(
            'INSERT INTO devices (location, pc_id, is_replacement) VALUES (?, ?, ?)',
            (location, pc_id, is_replacement)
        )
        db.commit()
        flash('端末が正常に登録されました')
        return redirect(url_for('devices'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    db = get_db()
    if request.method == 'POST':
        location = request.form['location']
        pc_id = request.form['pc_id']
        status = request.form['status']
        release_date = request.form['release_date'] or None
        is_replacement = 1 if request.form.get('is_replacement') else 0

        db.execute(
            'UPDATE devices SET location = ?, pc_id = ?, status = ?, '
            'release_date = ?, is_replacement = ?, updated_at = CURRENT_TIMESTAMP '
            'WHERE id = ?',
            (location, pc_id, status, release_date, is_replacement, id)
        )
        db.commit()
        flash('端末情報が更新されました')
        return redirect(url_for('devices'))

    device = db.execute('SELECT * FROM devices WHERE id = ?', (id,)).fetchone()
    return render_template('edit.html', device=device)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM devices WHERE id = ?', (id,))
    db.commit()
    flash('端末が削除されました')
    return redirect(url_for('devices'))

@app.route('/export')
@login_required
def export_csv():
    db = get_db()
    devices = db.execute('SELECT * FROM devices ORDER BY created_at DESC').fetchall()
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', '箇所名', 'PC/ID', 'ステータス', '解除期限', '故障機交換', '作成日時', '更新日時'])
    
    for device in devices:
        cw.writerow([
            device['id'],
            device['location'],
            device['pc_id'],
            device['status'],
            device['release_date'],
            '有' if device['is_replacement'] else '無',
            device['created_at'],
            device['updated_at']
        ])
    
    output = si.getvalue()
    si.close()
    
    return send_file(
        StringIO(output),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'devices_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/lockers')
@login_required
def lockers():
    db = get_db()
    lockers = db.execute('SELECT * FROM lockers ORDER BY id').fetchall()
    return render_template('lockers.html', lockers=lockers)

@app.route('/locker/<int:id>/toggle')
@login_required
def toggle_locker(id):
    db = get_db()
    locker = db.execute('SELECT status FROM lockers WHERE id = ?', (id,)).fetchone()
    new_status = '解錠' if locker['status'] == '施錠' else '施錠'
    
    db.execute(
        'UPDATE lockers SET status = ?, last_updated = CURRENT_TIMESTAMP WHERE id = ?',
        (new_status, id)
    )
    db.commit()
    flash(f'ロッカー{id}のステータスが{new_status}に変更されました')
    return redirect(url_for('lockers'))

@app.route('/get_available_lockers')
@login_required
def get_available_lockers():
    db = get_db()
    lockers = db.execute('SELECT * FROM lockers WHERE status = "施錠" AND password IS NULL').fetchall()
    return jsonify([dict(locker) for locker in lockers])

@app.route('/issue_password/<int:device_id>', methods=['POST'])
@login_required
def issue_password(device_id):
    db = get_db()
    locker_id = request.form.get('locker_id')
    expiry_date = request.form.get('expiry_date')
    
    if not locker_id or not expiry_date:
        return jsonify({'error': '必要な情報が不足しています'}), 400
    
    password = generate_password()
    expiry_datetime = datetime.strptime(expiry_date, '%Y-%m-%d')
    
    db.execute(
        'UPDATE lockers SET status = ?, password = ?, password_expiry = ? WHERE id = ?',
        ('施錠', password, expiry_datetime, locker_id)
    )
    
    db.execute(
        'UPDATE devices SET status = ?, locker_id = ?, release_date = ? WHERE id = ?',
        ('受取待ち', locker_id, expiry_date, device_id)
    )
    
    db.commit()
    
    return jsonify({
        'password': password,
        'locker_name': db.execute('SELECT name FROM lockers WHERE id = ?', (locker_id,)).fetchone()['name']
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=53430)

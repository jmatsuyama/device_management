from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import csv
from datetime import datetime
from io import StringIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
DATABASE = 'devices.db'

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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/devices')
def devices():
    db = get_db()
    devices = db.execute('SELECT * FROM devices ORDER BY created_at DESC').fetchall()
    return render_template('devices.html', devices=devices)

@app.route('/add', methods=['GET', 'POST'])
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
def delete(id):
    db = get_db()
    db.execute('DELETE FROM devices WHERE id = ?', (id,))
    db.commit()
    flash('端末が削除されました')
    return redirect(url_for('devices'))

@app.route('/export')
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
def lockers():
    db = get_db()
    lockers = db.execute('SELECT * FROM lockers ORDER BY id').fetchall()
    return render_template('lockers.html', lockers=lockers)

@app.route('/locker/<int:id>/toggle')
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

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=53430)

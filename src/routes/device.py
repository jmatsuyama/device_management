from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Device, db
from routes.auth import jeis_required
import csv
from io import StringIO
from datetime import datetime
import pytz

device = Blueprint('device', __name__)

@device.route('/devices')
@login_required
@jeis_required
def list_devices():
    devices = Device.query.all()
    return render_template('devices_new.html', devices=devices)

@device.route('/add', methods=['GET', 'POST'])
@login_required
@jeis_required
def add_device():
    if request.method == 'POST':
        location = request.form.get('location')
        pc_id = request.form.get('pc_id')
        status = request.form.get('status')
        release_date = request.form.get('release_date')
        is_replacement = bool(request.form.get('is_replacement'))

        if not all([location, pc_id, status]):
            flash('必須項目を入力してください。', 'error')
            return redirect(url_for('device.add_device'))

        try:
            release_date = datetime.strptime(release_date, '%Y-%m-%d').replace(tzinfo=pytz.UTC) if release_date else None
        except ValueError:
            flash('日付の形式が正しくありません。', 'error')
            return redirect(url_for('device.add_device'))

        device = Device(
            location=location,
            pc_id=pc_id,
            status=status,
            release_date=release_date,
            is_replacement=is_replacement
        )
        db.session.add(device)
        db.session.commit()

        flash('デバイスを追加しました。', 'success')
        return redirect(url_for('device.list_devices'))

    return render_template('add.html')

@device.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@jeis_required
def edit_device(id):
    device = Device.query.get_or_404(id)
    
    if request.method == 'POST':
        device.location = request.form.get('location')
        device.pc_id = request.form.get('pc_id')
        device.status = request.form.get('status')
        release_date = request.form.get('release_date')
        device.is_replacement = bool(request.form.get('is_replacement'))

        try:
            device.release_date = datetime.strptime(release_date, '%Y-%m-%d').replace(tzinfo=pytz.UTC) if release_date else None
        except ValueError:
            flash('日付の形式が正しくありません。', 'error')
            return redirect(url_for('device.edit_device', id=id))

        db.session.commit()
        flash('デバイス情報を更新しました。', 'success')
        return redirect(url_for('device.list_devices'))

    return render_template('edit.html', device=device)

@device.route('/delete/<int:id>')
@login_required
@jeis_required
def delete_device(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    flash('デバイスを削除しました。', 'success')
    return redirect(url_for('device.list_devices'))

@device.route('/export_devices')
@login_required
@jeis_required
def export_devices():
    si = StringIO()
    cw = csv.writer(si)
    
    # BOM付きUTF-8のヘッダーを書き込む
    si.write('\ufeff')
    
    # ヘッダー行を書き込む
    cw.writerow(['ID', '箇所名', 'PC/ID', 'ステータス', '解除期限', '故障機交換'])
    
    # データを書き込む
    devices = Device.query.all()
    for device in devices:
        cw.writerow([
            device.id,
            device.location,
            device.pc_id,
            device.status,
            device.release_date.strftime('%Y-%m-%d') if device.release_date else '',
            '1' if device.is_replacement else '0'
        ])
    
    output = si.getvalue()
    si.close()
    
    return output, 200, {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename=devices.csv'
    }

@device.route('/import_devices_csv', methods=['POST'])
@login_required
@jeis_required
def import_devices_csv():
    if 'file' not in request.files:
        flash('ファイルがアップロードされていません。', 'error')
        return redirect(url_for('device.list_devices'))
    
    file = request.files['file']
    if file.filename == '':
        flash('ファイルが選択されていません。', 'error')
        return redirect(url_for('device.list_devices'))
    
    if not file.filename.endswith('.csv'):
        flash('CSVファイルを選択してください。', 'error')
        return redirect(url_for('device.list_devices'))
    
    try:
        # CSVファイルを読み込む
        stream = StringIO(file.stream.read().decode('utf-8-sig'))
        reader = csv.DictReader(stream)
        
        for row in reader:
            device = Device.query.get(int(row['ID'])) if row.get('ID') else None
            
            if device:
                # 既存のデバイスを更新
                device.location = row['箇所名']
                device.pc_id = row['PC/ID']
                device.status = row['ステータス']
                device.release_date = datetime.strptime(row['解除期限'], '%Y-%m-%d').replace(tzinfo=pytz.UTC) if row['解除期限'] else None
                device.is_replacement = bool(int(row['故障機交換']))
            else:
                # 新規デバイスを作成
                device = Device(
                    location=row['箇所名'],
                    pc_id=row['PC/ID'],
                    status=row['ステータス'],
                    release_date=datetime.strptime(row['解除期限'], '%Y-%m-%d').replace(tzinfo=pytz.UTC) if row['解除期限'] else None,
                    is_replacement=bool(int(row['故障機交換']))
                )
                db.session.add(device)
        
        db.session.commit()
        flash('CSVファイルのインポートが完了しました。', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'CSVファイルのインポートに失敗しました: {str(e)}', 'error')
    
    return redirect(url_for('device.list_devices'))
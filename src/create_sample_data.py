from app import create_app
from models import db, Locker, Device, User
from datetime import datetime
import pytz

def create_sample_data():
    app = create_app()
    with app.app_context():
        # サンプルロッカーの作成
        lockers_data = [
            {'name': 'ロッカー1-A'},
            {'name': 'ロッカー1-B'},
            {'name': 'ロッカー1-C'},
            {'name': 'ロッカー2-A'},
            {'name': 'ロッカー2-B'},
            {'name': 'ロッカー2-C'},
            {'name': 'ロッカー3-A'},
            {'name': 'ロッカー3-B'},
            {'name': 'ロッカー3-C'},
            {'name': 'ロッカー4-A'},
        ]

        # 既存のロッカーをチェック
        existing_lockers = {locker.name: locker for locker in Locker.query.all()}

        # ロッカーの作成
        for locker_data in lockers_data:
            if locker_data['name'] not in existing_lockers:
                locker = Locker(
                    name=locker_data['name'],
                    is_locked=True,
                    last_updated=datetime.now(pytz.UTC)
                )
                db.session.add(locker)
                print(f"ロッカーを作成しました: {locker_data['name']}")
            else:
                print(f"ロッカーは既に存在します: {locker_data['name']}")

        # サンプルデバイスの作成（まだデバイスが存在しない場合）
        if Device.query.count() == 0:
            devices_data = [
                {
                    'location': '東京オフィス',
                    'pc_id': 'PC-TKY-001',
                    'status': '利用可能'
                },
                {
                    'location': '大阪オフィス',
                    'pc_id': 'PC-OSK-001',
                    'status': '利用可能'
                },
                {
                    'location': '名古屋オフィス',
                    'pc_id': 'PC-NGY-001',
                    'status': '利用可能'
                }
            ]

            for device_data in devices_data:
                device = Device(
                    location=device_data['location'],
                    pc_id=device_data['pc_id'],
                    status=device_data['status'],
                    is_replacement=False
                )
                db.session.add(device)
                print(f"デバイスを作成しました: {device_data['pc_id']}")

        try:
            db.session.commit()
            print('サンプルデータの作成が完了しました。')
        except Exception as e:
            db.session.rollback()
            print(f'エラーが発生しました: {str(e)}')

if __name__ == '__main__':
    create_sample_data()
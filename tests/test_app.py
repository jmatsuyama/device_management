import unittest
import os
import tempfile
from datetime import datetime, timedelta
from app import app, init_db, get_db
from werkzeug.security import generate_password_hash

class TestApp(unittest.TestCase):
    def setUp(self):
        # テスト用のデータベースを作成
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        with app.app_context():
            init_db()
            # テストユーザーを作成
            self.create_test_users()
            # テストデータを作成
            self.create_test_data()
    
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def create_test_users(self):
        with app.app_context():
            db = get_db()
            # 既存のユーザーを削除
            db.execute('DELETE FROM users')
            # JEISユーザー
            db.execute(
                'INSERT INTO users (name, user_id, password, organization) VALUES (?, ?, ?, ?)',
                ('管理者', 'admin', generate_password_hash('admin123'), 'JEIS')
            )
            # JRユーザー
            db.execute(
                'INSERT INTO users (name, user_id, password, organization) VALUES (?, ?, ?, ?)',
                ('JRユーザー', 'jr', generate_password_hash('jr123'), 'JR')
            )
            db.commit()
    
    def create_test_data(self):
        with app.app_context():
            db = get_db()
            # 既存のデータを削除
            db.execute('DELETE FROM lockers')
            db.execute('DELETE FROM devices')
            # テスト用ロッカー
            db.execute('INSERT INTO lockers (name, status) VALUES (?, ?)', ('テストロッカー1', '施錠'))
            db.execute('INSERT INTO lockers (name, status, password, password_expiry) VALUES (?, ?, ?, ?)',
                      ('テストロッカー2', '施錠', '1234', datetime.now() + timedelta(days=1)))
            # テスト用端末
            db.execute(
                'INSERT INTO devices (location, pc_id, status, is_replacement) VALUES (?, ?, ?, ?)',
                ('テスト箇所', 'TEST001', '準備中', 0)
            )
            db.commit()
    
    def login(self, user_id, password):
        return self.client.post('/login', data={
            'user_id': user_id,
            'password': password
        }, follow_redirects=True)
    
    def logout(self):
        return self.client.get('/logout', follow_redirects=True)
    
    # ログインのテスト
    def test_login_jeis(self):
        # JEISユーザーでログイン
        response = self.login('admin', 'admin123')
        self.assertIn(b'\xe3\x83\x9b\xe3\x83\xbc\xe3\x83\xa0', response.data)  # "ホーム"が含まれていることを確認
    
    def test_login_jr(self):
        # JRユーザーでログイン
        response = self.login('jr', 'jr123')
        self.assertIn(b'\xe7\xab\xaf\xe6\x9c\xab\xe5\x8f\x97\xe4\xbb\x98', response.data)  # "端末受付"が含まれていることを確認
    
    def test_invalid_login(self):
        # 無効なログイン
        response = self.login('invalid', 'invalid')
        self.assertIn(b'\xe3\x83\xa6\xe3\x83\xbc\xe3\x82\xb6\xe3\x83\xbc\xe3\x81\xbe\xe3\x81\x9f\xe3\x81\xaf\xe3\x83\x91\xe3\x82\xb9\xe3\x83\xaf\xe3\x83\xbc\xe3\x83\x89\xe3\x81\x8c\xe6\xad\xa3\xe3\x81\x97\xe3\x81\x8f\xe3\x81\x82\xe3\x82\x8a\xe3\x81\xbe\xe3\x81\x9b\xe3\x82\x93', response.data)  # "ユーザーIDまたはパスワードが正しくありません"が含まれていることを確認
    
    # アクセス制御のテスト
    def test_jeis_access(self):
        self.login('admin', 'admin123')
        # JEISユーザーは全ての機能にアクセス可能
        response = self.client.get('/devices')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/master_output')
        self.assertEqual(response.status_code, 200)
    
    def test_jr_access(self):
        self.login('jr', 'jr123')
        # JRユーザーは受付画面のみアクセス可能
        response = self.client.get('/devices')
        self.assertEqual(response.status_code, 302)  # リダイレクト
        response = self.client.get('/reception')
        self.assertEqual(response.status_code, 200)
    
    # ロッカー機能のテスト
    def test_locker_password(self):
        self.login('jr', 'jr123')
        # 正しいパスワードでロッカーを解錠
        response = self.client.post('/enter_password', data={
            'locker_id': '2',
            'password': '1234'
        }, follow_redirects=True)
        self.assertIn(b'\xe3\x81\x94\xe5\x88\xa9\xe7\x94\xa8\xe3\x81\x82\xe3\x82\x8a\xe3\x81\x8c\xe3\x81\xa8\xe3\x81\x86\xe3\x81\x94\xe3\x81\x96\xe3\x81\x84\xe3\x81\xbe\xe3\x81\x97\xe3\x81\x9f', response.data)  # "ご利用ありがとうございました"が含まれていることを確認
    
    def test_invalid_locker_password(self):
        self.login('jr', 'jr123')
        # 誤ったパスワードでロッカーを解錠
        response = self.client.post('/enter_password', data={
            'locker_id': '2',
            'password': '9999'
        }, follow_redirects=True)
        self.assertIn(b'\xe3\x83\x91\xe3\x82\xb9\xe3\x83\xaf\xe3\x83\xbc\xe3\x83\x89\xe3\x81\x8c\xe6\xad\xa3\xe3\x81\x97\xe3\x81\x8f\xe3\x81\x82\xe3\x82\x8a\xe3\x81\xbe\xe3\x81\x9b\xe3\x82\x93', response.data)  # "パスワードが正しくありません"が含まれていることを確認
    
    # マスタ出力機能のテスト
    def test_export_master(self):
        self.login('admin', 'admin123')
        # 端末マスタのエクスポート
        response = self.client.get('/export_devices_master')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')
        
        # ロッカーマスタのエクスポート
        response = self.client.get('/export_lockers_master')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')
    
    def test_import_master(self):
        self.login('admin', 'admin123')
        # 端末マスタのインポート
        with open('tests/test_devices.csv', 'w', encoding='utf-8-sig') as f:
            f.write('ID,箇所名,PC/ID,ステータス,解除期限,故障機交換,ロッカーID\n')
            f.write('1,テスト箇所,TEST002,準備中,,0,\n')
        
        with open('tests/test_devices.csv', 'rb') as f:
            response = self.client.post('/import_devices_master', data={
                'file': (f, 'test_devices.csv')
            }, follow_redirects=True)
        
        self.assertIn(b'\xe3\x82\xa4\xe3\x83\xb3\xe3\x83\x9d\xe3\x83\xbc\xe3\x83\x88\xe3\x81\x8c\xe5\xae\x8c\xe4\xba\x86\xe3\x81\x97\xe3\x81\xbe\xe3\x81\x97\xe3\x81\x9f', response.data)  # "インポートが完了しました"が含まれていることを確認
        os.unlink('tests/test_devices.csv')

if __name__ == '__main__':
    unittest.main()

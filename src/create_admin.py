from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

def create_admin_user():
    app = create_app()
    with app.app_context():
        # 管理者ユーザーが存在するか確認
        admin = User.query.filter_by(user_id='admin').first()
        if not admin:
            admin = User(
                name='管理者',
                user_id='admin',
                password=generate_password_hash('admin123'),
                organization='JEIS'
            )
            db.session.add(admin)
            db.session.commit()
            print('管理者ユーザーを作成しました。')
        else:
            print('管理者ユーザーは既に存在します。')

if __name__ == '__main__':
    create_admin_user()
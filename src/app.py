from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
import os
from models import db, User

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth as auth_blueprint
    from routes.device import device as device_blueprint
    from routes.locker import locker as locker_blueprint
    from routes.user import user as user_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(device_blueprint)
    app.register_blueprint(locker_blueprint)
    app.register_blueprint(user_blueprint)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if current_user.organization == 'JEIS':
            return redirect(url_for('device.list_devices'))
        return redirect(url_for('locker.reception'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=52109)
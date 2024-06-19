from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
bootstrap = Bootstrap5()

@login_manager.user_loader
def load_user(user_id):
    from costcalc.models import User
    try:
        return User.query.get(int(user_id))
    except ValueError:
        return None

# 自定义未登录处理函数
@login_manager.unauthorized_handler
def unauthorized():
    from flask import flash,redirect, url_for
    flash('请先登录以访问此页面。', 'danger')  # 自定义的flash消息
    return redirect(url_for('auth.login'))

login_manager.login_view = 'auth.login'
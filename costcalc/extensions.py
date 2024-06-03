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
    return User.query.get(int(user_id))

login_manager.login_view = 'auth.login'
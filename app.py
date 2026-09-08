from flask import Flask
from flask_login import LoginManager

from auth.routes import bp as auth_bp
from items.routes import bp as items_bp
from config import SECRET_KEY
from db import db_session
from models import User


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, int(user_id))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=True)

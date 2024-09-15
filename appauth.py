from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)


class User(db.Model, UserMixin):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(30), unique=True, nullable=False)
    password: str = db.Column(db.String(16), nullable=False)
    age: int = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"{self.id} - {self.username}"

    def is_authenticated(self):
        return True


class IndexView(AdminIndexView):
    def is_accessible(self):
        return True


class UserView(ModelView):
    def is_accessible(self):
        return True


admin = Admin(app, index_view=IndexView())
admin.add_view(UserView(User, db.session))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            username=request.form.get('username'),
            password=generate_password_hash(request.form.get('password'))
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect('/')
    return "Форма регистрации"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.session.query(User).filter_by(username=request.form.get('username')).first()
        if check_password_hash(user.password, request.form.get('password')):
            login_user(user)
        else:
            return "Ты самозванец!"
    return "Форма авторизации"


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_required
@app.route('/super_secret')
def profile():
    return f"User {current_user.username}"


@app.errorhandler(401)
def not_authorized():
    return "Вы не авторизованы!"


@app.errorhandler(404)
def not_found(info):
    return "Такой страницы не найдено!"


if __name__ == '__main__':
    app.run(host='0.0.0.0')

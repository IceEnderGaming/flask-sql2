from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login_form import LoginForm
from forms.jobs_form import WorksForm
from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.user_id == current_user.id).first()
    jobs = jobs.jobs
    return render_template('index.html', jobs=jobs.split(", "))


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session.global_init("db/users.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


app.run(host='127.0.0.1', port=5000, debug=True)

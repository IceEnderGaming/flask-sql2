from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.login_form import LoginForm
from forms.jobs_form import JobsForm
from forms.register_form import RegisterForm
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
    jobs = db_sess.query(Jobs)
    users = db_sess.query(User)
    return render_template("index.html", jobs=jobs, users=users)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.activity = form.title.data
        jobs.team_leader = form.leader_id.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        db_sess.merge(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           form=form)


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.submit.data:
        user = User()
        user.email = form.login.data
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.set_password(form.password.data)
        db_session.global_init("db/users.db")
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


app.run(host='127.0.0.1', port=5000, debug=True)

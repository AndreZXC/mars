import datetime as dt

from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_restful import Api, abort

from data import db_session, jobs_api2
from data.jobs import Jobs
from data.users import User
from data.departaments import Departament
from froms.depeart import DepartamentForm
from froms.login import LoginForm
from froms.newjob import NewJobForm
from froms.reg import RegisterForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'KOLLOS'
app.config['PARAMETR_SESSION_LIFE'] = dt.timedelta(days=3)
api = Api(app)
loginmng = LoginManager()
loginmng.init_app(app)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@loginmng.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('reg.html', title='Регистрация', form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('reg.html', title='Регистрация', form=form,
                                   message='Данный email уже зарегестрирован')
        user = User(name=form.name.data,
                    surname=form.surname.data,
                    speciality=form.speciality.data,
                    position=form.position.data,
                    address=form.address.data,
                    email=form.email.data,
                    age=form.age.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('reg.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', title='Login', message='wrong password error',
                               form=form)
    return render_template('login.html', title='Login', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/newjob', methods=['GET', 'POST'])
@login_required
def newjob():
    form = NewJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(Jobs).filter(User.id == form.teamlead.data).first():
            return render_template('newjob.html', title='Создание работы', form=form,
                                   message='Тимлида нет в базе данных')
        job = Jobs(job=form.job.data,
                   work_size=form.work_size.data,
                   collaborators=form.collaborators.data,
                   team_leader=form.teamlead.data,
                   is_finished=form.completed.data)
        job.dates(form.start_date.data)
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('newjob.html', title='Создание работы', form=form)


@app.route('/editjob/<int:idjob>', methods=['GET', 'POST'])
@login_required
def editjob(idjob):
    form = NewJobForm()
    userid = current_user.id
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == idjob).first()
        if job and (job.team_leader == userid or userid == 1):
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.start_date.data = job.start_date
            form.collaborators.data = job.collaborators
            form.completed.data = job.is_finished
            form.teamlead.data = job.team_leader
            form.teamlead.render_kw = {'readonly': True}
            form.submit.label.text = 'Изменить'
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == idjob).first()
        if job:
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.start_date = form.start_date.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.completed.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('newjob.html', title='Редактирование работы', form=form)


@login_required
@app.route('/deljob/<int:jobid>')
def deljob(jobid):
    userid = current_user.id
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == jobid).first()
    if job and (job.team_leader == userid or userid == 1):
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/deptable')
def deptable():
    db_sess = db_session.create_session()
    deps = db_sess.query(Departament).all()
    return render_template("departaments_view.html", departaments=deps)


@login_required
@app.route('/newdep', methods=['GET', 'POST'])
def newdep():
    form = DepartamentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(Departament).filter(User.id == form.chief.data).first():
            return render_template('dep.html', title='Создание департамента', form=form,
                                   message='Шефа нет в базе данных')
        dep = Departament(chief=form.chief.data,
                          email=form.email.data,
                          title=form.title.data,
                          members=form.members.data)
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/deptable')
    return render_template('dep.html', title='Создание департамента', form=form)


@login_required
@app.route('/editdep/<int:depid>', methods=['GET', 'POST'])
def editdep(depid):
    form = DepartamentForm()
    userid = current_user.id
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Departament).filter(Departament.id == depid).first()
        if dep and (dep.chief == userid or userid == 1):
            form.title.data = dep.title
            form.email.data = dep.email
            form.members.data = dep.members
            form.chief.data = dep.chief
            form.chief.render_kw = {'readonly': True}
            form.submit.label.text = 'Изменить'
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Departament).filter(Departament.id == depid).first()
        dep.title = form.title.data
        dep.email = form.email.data
        dep.members = form.members.data
        db_sess.commit()
        return redirect('/deptable')
    return render_template('dep.html', title='Редактирование департамента', form=form)


@login_required
@app.route('/deldep/<int:depid>')
def deldep(depid):
    userid = current_user.id
    db_sess = db_session.create_session()
    dep = db_sess.query(Departament).filter(Departament.id == depid).first()
    if dep and (dep.chief == userid or userid == 1):
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/deptable')


def main():
    db_session.global_init("db/users.db")
    api.add_resource(jobs_api2.JobResourse, '/api/job/<int:jobid>')
    api.add_resource(jobs_api2.JobListResourse, '/api/jobs')
    app.run()


if __name__ == '__main__':
    main()
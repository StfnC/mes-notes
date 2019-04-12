from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, GradeForm, RScoreForm
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Grade
from werkzeug.urls import url_parse
from datetime import datetime
from graphing import build_graph

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = GradeForm()
    if form.validate_on_submit():
        grade = Grade(mark=form.mark.data, subject=form.subject.data, timestamp=form.timestamp.data, student=current_user)
        mpl_timestamp = str(form.timestamp.data)
        grade.reformat_date(mpl_timestamp)
        db.session.add(grade)
        db.session.commit()
        flash(f'''La note a été ajoutée!''')
        return redirect(url_for('index'))
    user = User.query.filter_by(username=current_user.username).first()
    marks = Grade.query.filter_by(user_id=user.id).order_by(Grade.timestamp).all()
    subjects = []
    graph_data = dict()
    for m in marks:
        t = m.timestamp
        g = m.mark
        s = m.subject
        if s in graph_data:
            graph_data[s].append([g, t])
        else:
            graph_data[s] = [[g, t]]
    graph = build_graph(graph_data)
    return render_template('index.html', title='Accueil', user=current_user.username, form=form, graph=graph)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Mauvais nom d\'utilisateur ou mot de passe')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Connexion', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'''Bienvenue sur MesNotes, {form.username.data}''')
        return redirect(url_for('login'))
    return render_template('register.html', title='S\'enregistrer', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Vérifiez votre email pour les instructions du changement de mot de passe.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Demande changement de mot de passe', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Votre mot de passe à été changé.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Changer mot de passe', form=form)


@app.route('/cote_r', methods=['GET', 'POST'])
def cote_r():
    def average(marks):
        return sum(marks) / len(marks)
    def r_score(grades, group_average=80, std_deviation=8, average_mps=80):
        average_grade = average(grades)
        z_score = ((average_grade - group_average) / std_deviation)
        ifg = ((average_mps - 75) / 14)
        return round((z_score + ifg + 5) * 5, 2)
    form = RScoreForm()
    grades = Grade.query.all()
    marks = []
    for grade in grades:
        marks.append(int(grade.mark))
    if form.validate_on_submit():
        group_average = form.group_average.data
        std_deviation = form.std_deviation.data
        average_mps = form.average_mps.data
        r_score = r_score(grades=marks, group_average=group_average, std_deviation=std_deviation, average_mps=average_mps)
    else:
        r_score = r_score(grades=marks)
    return render_template('cote_r.html', title='Cote R', r_score=r_score, form=form)

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    user = User.query.filter_by(username=current_user.username).first()
    grades = Grade.query.filter_by(user_id=user.id).order_by(Grade.timestamp).all()
    for grade in grades:
        if grade.normal_timestamp == None:
            grade.set_normal_timestamp(grade.timestamp)
    return render_template('notes.html', title='Notes', grades=grades)

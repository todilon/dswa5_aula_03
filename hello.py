from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    surname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    school = StringField('Informe a sua Insituição de ensino:', validators=[DataRequired()])

    choices = [('DSWA5', 'DSWA5'), ('DWBA4', 'DWBA4'), ('Gestão de projetos', 'Gestão de projeto')]
    subject = SelectField('Informe a sua disciplina:', choices=choices)

    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')

        if old_name is not None and old_name != form.name.data:
            flash('Você alterou o seu nome!')

        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['school'] = form.school.data
        session['subject'] = form.subject.data

        return redirect(url_for('index'))

    return render_template('index.html', form=form, current_time=datetime.utcnow(), name=session.get('name'), surname=session.get('surname'), school=session.get('school'), subject=session.get('subject'), user_host=request.remote_addr, app_host=request.host)

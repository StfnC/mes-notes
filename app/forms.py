from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange, InputRequired
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se Souvenir de Moi')
    sign_in = SubmitField('Se Connecter')

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password_repeat = PasswordField(
        'Réécris ton mot de passe', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Créer le compte')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cette adresse email est déjà utilisée.')

class GradeForm(FlaskForm):
    subject_choices = [
                    ('Anglais', 'Anglais'), ('Art Dramatique', 'Art Dramatique'), ('Arts Plastiques', 'Arts Plastiques'),
                    ('Chimie', 'Chimie'), ('Éducation Financière', 'Éducation Financière'), ('Éducation Physique', 'Éducation Physique'),
                    ('Espagnol', 'Espagnol'), ('Éthique et Culture Religieuse', 'Éthique et Culture Religieuse'), ('Français', 'Français'), ('Géographie', 'Géographie'),
                    ('Histoire', 'Histoire'), ('Mathématiques', 'Mathématiques'), ('Monde Contemporain', 'Monde Contemporain'), ('Multimédia', 'Multimédia'), ('Musique', 'Musique'),
                    ('Physique', 'Physique'), ('Sciences et Technologie', 'Sciences et Technologie'), ('Autre', 'Autre')]

    subject = SelectField('Matière', choices=subject_choices, validators=[InputRequired()])
    mark = IntegerField('Note (pourcentage)', validators=[DataRequired(), NumberRange(min=0)])
    timestamp = DateField('Quand as-tu reçu la note?', format='%Y-%m-%d')
    submit = SubmitField('Ajouter')

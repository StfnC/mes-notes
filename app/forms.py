from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange, InputRequired
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(max=50)])
    remember_me = BooleanField('Se Souvenir de Moi')
    sign_in = SubmitField('Se Connecter')

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(max=50)])
    password_repeat = PasswordField(
        'Réécris ton mot de passe', validators=[DataRequired(), EqualTo('password'), Length(max=50)])
    register = SubmitField('Créer le compte')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cette adresse email est déjà utilisée.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Demander un changement de mot de passe')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nouveau mot de passe', validators=[DataRequired(), Length(max=50)])
    password_repeat = PasswordField(
        'Réécris ton mot de passe', validators=[DataRequired(), EqualTo('password'), Length(max=50)]
        )
    submit = SubmitField('Changer mot de passe')

class GradeForm(FlaskForm):
    subject_choices = [
                    ('Anglais', 'Anglais'), ('Art Dramatique', 'Art Dramatique'), ('Arts Plastiques', 'Arts Plastiques'),
                    ('Chimie', 'Chimie'), ('Éducation Financière', 'Éducation Financière'), ('Éducation Physique', 'Éducation Physique'),
                    ('Espagnol', 'Espagnol'), ('Éthique et Culture Religieuse', 'Éthique et Culture Religieuse'), ('Français', 'Français'), ('Géographie', 'Géographie'),
                    ('Histoire', 'Histoire'), ('Mathématiques', 'Mathématiques'), ('Monde Contemporain', 'Monde Contemporain'), ('Multimédia', 'Multimédia'), ('Musique', 'Musique'),
                    ('Physique', 'Physique'), ('Sciences et Technologie', 'Sciences et Technologie'), ('Autre', 'Autre')]

    subject = SelectField('Matière', choices=subject_choices, validators=[InputRequired()])
    mark = FloatField('Note (pourcentage)', validators=[DataRequired(), NumberRange(min=0, max=200)])
    timestamp = DateField('Quand as-tu reçu la note?', format='%Y-%m-%d')
    submit = SubmitField('Ajouter')

class RScoreForm(FlaskForm):
    student_average = FloatField('Ta moyenne', validators=[NumberRange(min=0, max=200)], default=80.0)
    group_average = FloatField('Moyenne du groupe', validators=[NumberRange(min=0, max=200)], default=80.0)
    std_deviation = FloatField('Écart type', validators=[NumberRange(min=0, max=200)], default=8.0)
    average_mps = FloatField('Moyenne des MPS', validators=[NumberRange(min=0, max=200)], default=80.0)
    submit = SubmitField('Envoyer')

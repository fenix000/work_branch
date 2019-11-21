from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

from webapp.user.models import User

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить', render_kw={"class": "form-check-input"})
    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary"})

class UserFormRegistration(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form-control"})
    fullname = StringField('Фамилия и Имя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Почта', render_kw={"class": "form-control"})
    phone = StringField('Телефон', render_kw={"class": "form-control"})
    role = SelectField('Права', choices = [('user', 'user'), ('admin', 'admin')], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators = [DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Добавить', render_kw={"class": "btn btn-primary"})
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Выберите другое имя.')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Такой E-mail уже существует.')


class EditProfileForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form-control"})
    fullname = StringField('Фамилия и Имя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Почта', render_kw={"class": "form-control"})
    phone = StringField('Телефон', render_kw={"class": "form-control"})
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)], render_kw={"class": "form-control"})
    submit = SubmitField('Изменить', render_kw={"class": "btn btn-primary"})
 
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators = [DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Изменить', render_kw={"class": "btn btn-primary"})

# class UploadAvatarForm(FlaskForm):
#     image = FileField('Загрузить: (<=3M)', validators=[
#         FileRequired(),
#         FileAllowed(['jpg', 'png'], 'Пожалуйста .jpg или .png.')
#     ])
#     submit = SubmitField()

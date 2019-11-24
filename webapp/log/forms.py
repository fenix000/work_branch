from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class PostForm(FlaskForm):
    post = TextAreaField('Сообщение:', validators=[DataRequired(), Length(
        min=5)], render_kw={"class": "form-control", "rows": "5"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class DocForm(FlaskForm):
    title = TextAreaField('Заголовок', validators=[DataRequired()], render_kw={
                          "class": "form-control", "rows": "1"})
    submit = SubmitField('Готово', render_kw={"class": "btn btn-primary"})


class CategoryForm(FlaskForm):
    name = StringField('Новая категория', validators=[DataRequired()], render_kw={
        "class": "form-control", "rows": "1"})
    submit = SubmitField('Готово', render_kw={"class": "btn btn-primary"})

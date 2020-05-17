from flask_wtf import FlaskForm
import wtforms as wtf
import wtforms.validators as vlds

from .validators import UsernameValidator, TagValidator
from .models import User


class LoginForm(FlaskForm):
    username = wtf.StringField(
        'Email или имя пользователя',
        validators=[
            vlds.DataRequired('Это поле обязательно')
        ],
        render_kw={'placeholder': 'Email или имя пользователя'}
    )
    password = wtf.PasswordField(
        'Пароль',
        validators=[
            vlds.DataRequired('Это поле обязательно')
        ],
        render_kw={'placeholder': 'Пароль'}
    )
    remember_me = wtf.BooleanField('Запомнить меня')


class RegisterForm(FlaskForm):
    username = wtf.StringField(
        'Придумайте имя пользователя',
        validators=[
            vlds.DataRequired('Это поле обязательно'),
            UsernameValidator()
        ]
    )
    email = wtf.StringField(
        'Адрес электронной почты',
        validators=[
            vlds.DataRequired('Это поле обязательно'),
            vlds.Email('Это не email')
        ]
    )
    password = wtf.PasswordField(
        'Пароль',
        validators=[
            vlds.DataRequired('Это поле обязательно'),
            vlds.Length(min=8, message='Пароль должен состоять минимум из 8 символов')
        ]
    )
    repeat_password = wtf.PasswordField(
        'Повторите пароль',
        validators=[
            vlds.DataRequired('Это поле обязательно'),
            vlds.EqualTo('password', 'Пароли должны совпадать'),
            vlds.Length(min=8, message="")
        ],
    )

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise vlds.ValidationError('Это имя пользователя уже занято')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise vlds.ValidationError('Этот email уже занят')


class PostForm(FlaskForm):
    title = wtf.StringField(
        'Название',
        validators=[
            vlds.DataRequired('Название не может быть пустым'),
            vlds.Length(max=128, message='Название поста не может быть больше 128 символов')
        ]
    )
    text = wtf.TextAreaField(
        validators=[vlds.DataRequired('Пост не может быть пустым')]
    )
    tags = wtf.StringField(
        'Список тегов через запятую',
        validators=[TagValidator()]
    )

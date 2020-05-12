from flask import redirect, url_for, flash, render_template
from flask_login import current_user, login_user, logout_user, login_required

from . import app, db
from .forms import LoginForm, RegisterForm
from .models import User

menu_items = [
        {
            'href': '#',
            'label': 'Подписки'
        },
        {
            'href': '#',
            'label': 'Мои посты'
        }
    ]


@app.route('/index/')
@app.route('/')
def index():
    return render_template('index.html', menu_items=menu_items)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash({
            'header': f'Вы уже вошли, {current_user.username}',
            'body': 'Чтобы войти в другой аккаунт сначала нажмите кнопку "Выйти"'
        }, 'toast-info')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if '@' in form.username.data:  # easy way to check if it is email or username
            user = User.query.filter_by(email=form.username.data).first()
        else:
            user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Неправильное имя пользователя или пароль", 'login-error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash({
            'header': 'Вход',
            'body': f'Вы успешно вошли в свой аккаунт, {user.username}'
        }, 'toast-info')
        return redirect(url_for('index'))
    return render_template('login.html', form=form, menu_items=menu_items, title="Войти в аккаунт")


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash({
            'header': f'Вы уже вошли, {current_user.username}',
            'body': 'Чтобы войти в другой аккаунт сначала нажмите кнопку "Выйти"'
        }, 'toast-info')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash({
            'header': 'Регистрация',
            'body': f'Вы успешно зарегистрировались в системе, {user.username}'
        }, 'toast-info')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Регистрация', menu_items=menu_items)


@app.route('/profile/<int:user_id>')
def profile(user_id: int):
    user = User.query.get_or_404(user_id)
    return f"{user.username}'s profile"

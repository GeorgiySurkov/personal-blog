from flask import redirect, url_for, flash, render_template, request, escape
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from werkzeug.urls import url_parse
from markdown import markdown

from . import app, db
from .forms import LoginForm, RegisterForm, PostForm, SearchPostForm
from .models import User, Tag, Post
from .services import parse_tags, list_most_frequent_tags


@app.route('/index')
@app.route('/')
def index():
    menu_items = [
        {
            'href': '#',
            'label': 'Подписки'
        },
        {
            'href': url_for('my_posts', page=1),
            'label': 'Мои посты'
        }
    ]
    query = request.args.get('q')
    if query is not None:
        page = request.args.get('page')
        if page is None:
            page = 1
        page = int(page)
        pagination = Post.query.filter(Post.title.ilike(f'%{query}%')).paginate(page, 5, True)
        return render_template('search.html', pagination=pagination, menu_items=menu_items, title=f"Поиск \"{query}\"",
                               query=query)
    return render_template('index.html', menu_items=menu_items, title="Микро блог")


@app.route('/login', methods=['GET', 'POST'])
def login():
    menu_items = [
        {
            'href': '#',
            'label': 'Подписки'
        },
        {
            'href': url_for('my_posts', page=1),
            'label': 'Мои посты'
        }
    ]
    if current_user.is_authenticated:
        flash({
            'header': f'Вы уже вошли, {current_user.username}',
            'body': 'Чтобы войти в другой аккаунт сначала нажмите кнопку "Выйти"',
            'timestamp': datetime.utcnow()
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
            'body': f'Вы успешно вошли в свой аккаунт, {user.username}',
            'timestamp': datetime.utcnow()
        }, 'toast-info')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form, menu_items=menu_items, title="Войти в аккаунт")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    menu_items = [
        {
            'href': '#',
            'label': 'Подписки'
        },
        {
            'href': url_for('my_posts', page=1),
            'label': 'Мои посты'
        }
    ]
    if current_user.is_authenticated:
        flash({
            'header': f'Вы уже вошли, {current_user.username}',
            'body': 'Чтобы войти в другой аккаунт сначала нажмите кнопку "Выйти"',
            'timestamp': datetime.utcnow()
        }, 'toast-info')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash({
            'header': 'Регистрация',
            'body': f'Вы успешно зарегистрировались в системе, {user.username}',
            'timestamp': datetime.utcnow()
        }, 'toast-info')
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Регистрация', menu_items=menu_items)


@app.route('/profile/<int:user_id>')
def profile(user_id: int):
    menu_items = [
        {
            'href': '#',
            'label': 'Подписки'
        },
        {
            'href': url_for('my_posts', page=1),
            'label': 'Мои посты'
        }
    ]
    user = User.query.get_or_404(user_id)
    posts_page = request.args.get('page')
    if posts_page is None:
        return redirect(url_for('profile', page=1, user_id=user.id))
    pagination = user.posts.paginate(int(posts_page), 5, False)
    most_used_tags = list_most_frequent_tags(user.posts.all())
    return render_template('profile.html', title=f"{user.username}'s profile", user=user, menu_items=menu_items,
                           most_used_tags=most_used_tags, pagination=pagination)


@app.route('/write_post', methods=['GET', 'POST'])
@login_required
def write_post():
    menu_items = [
        {
            'href': '#',
            'label': 'Подписки'
        },
        {
            'href': url_for('my_posts', page=1),
            'label': 'Мои посты'
        }
    ]
    form = PostForm()
    if form.validate_on_submit():
        md_text = form.text.data
        escaped_md_text = escape(md_text)
        html_text = markdown(escaped_md_text)
        post = Post(
            title=form.title.data,
            md_text=form.text.data,
            html_text=html_text,
            author=current_user
        )
        tags = parse_tags(form.tags.data)
        for tag in tags:
            tag_record = Tag.query.filter_by(name=tag).first()
            if tag_record is None:
                tag_record = Tag(name=tag)
            post.tags.append(tag_record)
            db.session.add(tag_record)
        db.session.add(post)
        db.session.commit()
        flash({
            'header': 'Пост',
            'body': 'Ваш пост успешно сохранен',
            'timestamp': datetime.utcnow()
        }, 'toast-info')
        return redirect(url_for('index'))
    return render_template('write_post.html', form=form, title='Редактор поста', menu_items=menu_items)


@app.route('/my_posts')
@login_required
def my_posts():
    menu_items = [
        {
            'href': '#',
            'label': 'Подписки'
        },
        {
            'active': True,
            'href': url_for('my_posts', page=1),
            'label': 'Мои посты'
        }
    ]
    page = request.args.get('page')
    if page is None:
        return redirect(url_for('my_posts', page='1'))
    page = int(page)
    pagination = Post.query.filter_by(author=current_user).paginate(page, 5, False)
    return render_template('my_posts.html', pagination=pagination, menu_items=menu_items, title='Мои посты')


@app.route('/post/<int:post_id>')
def post_view(post_id):
    menu_items = [
        {
            'href': '#',
            'label': 'Подписки'
        },
        {
            'href': url_for('my_posts', page=1),
            'label': 'Мои посты'
        }
    ]
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, menu_items=menu_items, title=f"{post.title} - Микро блог")


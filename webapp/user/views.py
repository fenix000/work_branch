from datetime import datetime
from dateutil.tz import tzlocal
from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from webapp import db
from webapp.decorators import admin_required
from webapp.user.forms import LoginForm, UserFormRegistration, EditProfileForm, ChangePasswordForm
from webapp.log.forms import PostForm
from webapp.user.models import User
from webapp.log.models import Post

blueprint = Blueprint('user', __name__, url_prefix='/user')

@blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        dt = datetime.now()
        current_user.last_seen = dt
        db.session.commit()


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('log.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('user.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Добро пожаловать!')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('log.index')
        return redirect(next_page)
    return render_template('user/login.html', form=form)

# @app.route('/register') 
# def registration():
#     title = 'Регистрация'
#     form = UserFormRegistration
#     return render_template('register.html', title=title, form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
@admin_required
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('log.index'))
    title = 'Регистрация'
    form = UserFormRegistration()
    return render_template('user/register.html', title=title, form=form)


@blueprint.route('/registration', methods=['GET', 'POST'])
@admin_required
def registration():
    title = 'Регистрация'
    form = UserFormRegistration()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        fullname=form.fullname.data,
                        role=form.role.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь зарегистрирован')
        return redirect(url_for('log.index')) 
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return render_template('user/register.html', title=title, form=form)

@blueprint.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form = EditProfileForm(current_user.username)
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.fullname = form.fullname.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('log.index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.about_me.data = current_user.about_me
    return render_template('user/user.html', user=user, form=form)


@blueprint.route('/user/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    user = User.query.filter_by(username=current_user.username).first()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Пароль изменен!')
        return redirect(url_for('user.logout'))
    return render_template('user/reset_password.html',user=user, form=form)


@blueprint.route('user/user_list.html', methods=['GET', 'POST'])
@admin_required
def user_list():
    all_user = User.query.order_by(User.id).all()
    return render_template('user/user_list.html', all_user=all_user)


@blueprint.route('/delete/<id>')
def user_delete(id):
    delete_user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(delete_user)
    db.session.commit()
    flash('Пользователь удален!')
    return redirect(url_for('user.user_list'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))

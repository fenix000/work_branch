from datetime import datetime
from dateutil.tz import tzlocal
from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request
from flask_login import current_user, login_required

from webapp import db

from webapp.log.models import Post
from webapp.log.forms import PostForm
from webapp.user.models import User


blueprint = Blueprint('log', __name__)

@blueprint.route('/')
@blueprint.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POST_PER_PAGE'], False)
    next_url = url_for('log.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('log.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url)

# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         dt = datetime.now()
#         current_user.last_seen = dt
#         db.session.commit()

@blueprint.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(text=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Запись добавлена!')
        return redirect(url_for('log.index'))
    return render_template('log/new_post.html', title='Новая запись!', form=form, posts=posts)


@blueprint.route('/new_doc', methods=['GET', 'POST'])
@login_required
def new_documentation():
    documentation = Post.query.order_by(Documentation.timestamp.desc()).all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(text=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Запись добавлена!')
        return redirect(url_for('log.index'))
    return render_template('log.new_post.html', title='Новая запись!', form=form, posts=posts)
from datetime import datetime
from dateutil.tz import tzlocal
from flask import Blueprint, flash, render_template, redirect, url_for, current_app, request
from flask_login import current_user, login_required

from webapp import db

from webapp.log.models import Post, Doc, Category
from webapp.log.forms import PostForm, DocForm, CategoryForm
from webapp.user.models import User


blueprint = Blueprint('log', __name__)


@blueprint.route('/')
@blueprint.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POST_PER_PAGE'], False)
    next_url = url_for('log.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('log.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Главная', posts=posts.items, next_url=next_url, prev_url=prev_url)


@blueprint.route('/edit_post', methods=['GET', 'POST'])
@blueprint.route('/edit_post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id=None):
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    if id:
        edit_post = Post.query.filter_by(id=id).first_or_404()
        if edit_post is None:
            return (404)
    else:
        edit_post = ''

    if request.method == "POST":
        if id:
            edit_post.text = request.form.get('editordata')
            db.session.add(edit_post)
        else:
            edit_post = Post(text=request.form.get(
                'editordata'), author=current_user)
            db.session.add(edit_post)
        db.session.commit()
        flash('Запись добавлена!')
        return redirect(url_for('log.index'))
    return render_template('log/edit_post.html', edit_post=edit_post,  posts=posts)


@blueprint.route('/delete/<id>')
@login_required
def post_delete(id):
    delete_post = Post.query.filter_by(id=id).first_or_404()
    db.session.delete(delete_post)
    db.session.commit()
    flash('Запись удалена!')
    return redirect(url_for('log.index'))


@blueprint.route('/edit_doc', methods=['GET', 'POST'])
@blueprint.route('/edit_doc/<id>', methods=['GET', 'POST'])
@login_required
def edit_doc(id=None):
    category = Category.query.order_by(Category.name).all()
    if id:
        edit_doc = Doc.query.filter_by(id=id).first_or_404()
        # title = edit_doc.title,
        # category = edit_doc.categiry_id
        if edit_doc is None:
            return (404)
    else:
        edit_doc = ''

    if request.method == "POST":
        if id:
            select_category = Category.query.filter_by(
                name=request.form.get('editorcategory')).first_or_404()
            edit_doc.category_id = select_category.id
            edit_doc.text = request.form.get('editordata')
            db.session.add(edit_doc)
        else:
            select_category = Category.query.filter_by(
                name=request.form.get('editorcategory')).first_or_404()
            edit_doc = Doc(title=request.form.get('editortitle'),
                           text=request.form.get('editordata'), author=current_user, category=select_category)
            db.session.add(edit_doc)
        db.session.commit()
        flash('Запись добавлена!')
        return redirect(url_for('log.documentation'))
    return render_template('log/edit_doc.html', edit_doc=edit_doc, category=category)


@blueprint.route('/documentation', methods=['GET', 'POST'])
@blueprint.route('/documentation/<id>', methods=['GET', 'POST'])
@blueprint.route('/documentation/<id>/<title>', methods=['GET', 'POST'])
@login_required
def documentation(title=None, id=None):
    form = CategoryForm()
    docs_category = Category.query.order_by(Category.name).all()
    # title = Doc.query.order_by(Doc.title).all()
    docs_list = ''
    docs_body = ''
    if id:
        docs_list = Doc.query.filter_by(category_id=id).all()
    if title:
        docs_body = Doc.query.filter_by(title=title).first_or_404()
    if request.method == "POST":
        if form.validate_on_submit():
            new_category = Category(name=form.name.data)
            db.session.add(new_category)
        db.session.commit()
        flash('Done')
        return redirect(url_for('log.documentation'))
    return render_template('log/documentation.html', docs_category=docs_category, docs_list=docs_list, form=form, docs_body=docs_body, title=title)


@blueprint.route('/documentation/<id>', methods=['GET', 'POST'])
@login_required
def doc_list(id):
    docs_list = Doc.query.filter_by(category_id=id).all()
    return render_template('log/documentation.html', docs_list=docs_list)


@blueprint.route('/documentation/<id>/<title>', methods=['GET', 'POST'])
@login_required
def doc_view(title):
    docs_body = Doc.query.filter_by(title=title).first_or_404()
    return render_template('log/documentation.html', docs_body=docs_body)


@blueprint.route('/contact', methods=['GET'])
@login_required
def contacts():
    user_contacts = User.query.order_by(User.id).all()
    return render_template('log/contacts.html', user_contacts=user_contacts)

from flask import Blueprint, render_template
from webapp import app, db

blueprint = bp = Blueprint('errors', __name__)


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

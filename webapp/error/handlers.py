from flask import Blueprint, render_template, current_app
from webapp import db

blueprint = Blueprint('error', __name__)

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500

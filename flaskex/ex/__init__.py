from flask import Blueprint

ex = Blueprint(
    'flaskex', __name__, template_folder='templates', static_folder='static',
    # flask has a bug https://github.com/mitsuhiko/flask/issues/348
    static_url_path='/static/flaskex'
)

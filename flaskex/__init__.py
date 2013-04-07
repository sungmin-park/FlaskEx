from os import environ
from logging import StreamHandler, INFO
from functools import wraps

from flask import (
    Flask as Flask_, g, request, Blueprint as Blueprint_, render_template
)
from flask_debugtoolbar import DebugToolbarExtension
from pyjade.ext.jinja import PyJadeExtension
from facebook import parse_signed_request


class ShortCuts(object):
    def pgroute(self, *args, **kwargs):
        kwargs['methods'] = ['GET', 'POST']
        return self.route(*args, **kwargs)


class Flask(ShortCuts, Flask_):
    def __init__(self, *args, **kwargs):
        super(Flask, self).__init__(*args, **kwargs)
        # regist jade
        self.jinja_env.add_extension(PyJadeExtension)
        self.jinja_env.pyjade.options['pretty'] = 'JADE_PRETTY' in environ
        # hook config.from_object
        # because some extra settings needs config
        _config_from_object = self.config.from_object
        def config_from_object(*args, **kwargs):
            _config_from_object(*args, **kwargs)
            if self.debug:
                DebugToolbarExtension(self)
            else:
                self.logger.addHandler(StreamHandler())
                self.logger.setLevel(INFO)
        self.config.from_object = config_from_object

    # auto escape jade files too
    def select_jinja_autoescape(self, filename):
        if filename and filename.endswith('.jade'):
            return True
        return super(Flask, self).select_jinja_autoescape(filename)


# extra Features for Facebook
class FlaskFacebook(Flask_):
    def __init__(self, *args, **kwargs):
        super(FlaskFacebook, self).__init__(*args, **kwargs)

        @self.before_request
        def _before_request():
            signed_request = request.form.get('signed_request', None)
            if signed_request:
                g.signed_request = \
                    parse_signed_request(
                        signed_request, self.config['FACEBOOK_SECRET']
                    )


class Blueprint(ShortCuts, Blueprint_):
    pass


# http://flask.pocoo.org/docs/patterns/viewdecorators/#templating-decorator
def templated(template_or_view_func):
    # if arguments is function, act as calling with None template name
    if hasattr(template_or_view_func, '__call__'):
        return templated(None)(template_or_view_func)
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template_or_view_func
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.jade'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator

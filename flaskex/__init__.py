from os import environ
from logging import StreamHandler, INFO

from flask import Flask as Flask_
from flask_debugtoolbar import DebugToolbarExtension
from pyjade.ext.jinja import PyJadeExtension

class Flask(Flask_):
    def __init__(self, *args, **kwargs):
        super(Flask, self).__init__(*args, **kwargs)
        # regist jade
        self.jinja_env.add_extension(PyJadeExtension)
        self.jinja_env.pyjade.options['pretty'] = 'JADE_PRETTY' in environ
        # hook config.from_object
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


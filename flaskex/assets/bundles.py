from flask.ext.assets import Bundle
from flaskex.assets.filters import requirefy_vendors


class Require(Bundle):
    def __init__(self, **vendors):
        super(Require, self).__init__(
            'flaskex/js/require.coffee',
            filters=['coffeescript', requirefy_vendors(vendors)],
            output='built/requirefy.js'
        )

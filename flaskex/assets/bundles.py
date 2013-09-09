from flask.ext.assets import Bundle
from flaskex.assets.filters import (
    requirefy_vendors, StreamlineCoffee, requirefy
)
from glob2 import glob
from os import path


class Require(Bundle):
    def __init__(self, **vendors):
        super(Require, self).__init__(
            'flaskex/js/require.coffee',
            filters=['coffeescript', requirefy_vendors(vendors)],
            output='built/requirefy.js'
        )


class Requirefy(Bundle):
    def __init__(self, app, root, module):
        root_path = path.join(app.static_folder, root)
        bundles = []
        for i in glob(path.join(root_path, module, '**')):
            source = i[len(app.static_folder) + 1:]
            module_name = path.splitext(source[len(root) + 1:])[0]
            bundles.append(
                Bundle(
                    source, filters=[StreamlineCoffee, requirefy(module_name)],
                    output=path.join('built', source) + '.js'
                )
            )
        super(Requirefy, self).__init__(*bundles)

streamlinejs = Bundle(
    'node_modules/streamline/lib/util/future.js',
    'node_modules/streamline/lib/callbacks/runtime.js',
    'node_modules/streamline/lib/callbacks/builtins.js',
)

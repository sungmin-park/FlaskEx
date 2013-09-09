from webassets.filter import Filter
from webassets.exceptions import FilterError
from webassets import Bundle
from subprocess import Popen, PIPE
from glob2 import glob
from os import path
from flask import current_app
from webassets.filter import get_filter
from urlparse import urlparse
from .hashlibs import md5sum
from .shell import copyp
from flask import url_for
from simplejson import dumps
from . import io
from .shell import ensure_exists


class IcedCoffeescript(Filter):
    name = 'icedcoffeescript'
    max_debug_level = None

    def output(self, _in, out, **kw):
        args = ['iced', '-sp', '--runtime', 'inline']
        proc = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate(_in.read().encode('utf-8'))
        if proc.returncode != 0:
            raise FilterError(
                (
                    'iced: subprocess had error: stderr=%s, ' +
                    'stdout=%s, returncode=%s'
                ) % (stderr, stdout, proc.returncode)
            )
        elif stderr:
            print("coffeescript filter has warnings:", stderr)
        out.write(stdout.decode('utf-8'))

    @classmethod
    def bundles(cls, *sources):
        li = []
        for i in sources:
            li.append(
                Bundle(
                    "js/%s.iced" % i, output="built/%s.js" % i, filters=[cls]
                )
            )
        return Bundle(*li)


def cssrewrite_replace(url):
    app = current_app
    if url[0] == '/':
        url = url[1:]
    else:
        url = path.join('img', url)
    src = path.join(app.static_folder, url)
    version = md5sum(urlparse(src).path)
    name, ext = path.splitext(url)
    name = path.join("built", "%s_%s%s" % (name, version, ext))
    dest = path.join(app.static_folder, name)
    copyp(urlparse(src).path, urlparse(dest).path)
    return '/static/' + name

cssrewrite = get_filter('cssrewrite', replace=cssrewrite_replace)


def find_all_images(app):
    return tuple(glob(path.join(app.static_folder, 'img', '*')))


def tag_version(name):
    app = current_app
    src_path = path.join(app.static_folder, 'img', name)
    name, ext = path.splitext(name)
    version = md5sum(src_path)
    versioned_name = "%s_%s%s" % (name, version, ext)
    relative_built_path = path.join('built', 'img', versioned_name)
    built_path = path.join(app.static_folder, relative_built_path)
    copyp(src_path, built_path)
    return relative_built_path


def img_for(name, _external=False):
    app = current_app
    if app.debug:
        relative_built_path = tag_version(name)
    else:
        relative_built_path = app.assets[name]
    return url_for('static', filename=relative_built_path, _external=_external)


def build_images():
    assets = dict()
    app = current_app
    img_folder = path.join(app.static_folder, 'img')
    for i in glob(img_folder + '/**'):
        if path.isfile(i):
            source = i[len(img_folder) + 1:]
            assets[source] = tag_version(source)
    assets_json = path.join(app.built_folder, 'assets.json')
    ensure_exists(app.built_folder)
    io.write(assets_json, dumps(assets))

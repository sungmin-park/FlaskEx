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


def img_for(name):
    app = current_app
    src_path = path.join(app.static_folder, 'img', name)
    name, ext = path.splitext(name)
    version = md5sum(src_path)
    versioned_name = "%s_%s%s" % (name, version, ext)
    relative_built_path = path.join('built', 'img', versioned_name)
    built_path = path.join(app.static_folder, relative_built_path)
    copyp(src_path, built_path)
    return url_for('static', filename=relative_built_path)

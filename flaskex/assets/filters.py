from flask import json
from webassets.filter import Filter, FilterError
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from os import path
import os


def requirefy_vendors(vendors):
    class RequirefyVendors(Filter):
        max_debug_level = None

        def output(self, in_, out, **kw):
            out.write(in_.read())
            print >> out, "requirefy.addVendors(%s);" % json.dumps(vendors)
    return RequirefyVendors


class StreamlineCoffee(Filter):
    max_debug_level = None
    options = {
        '_coffee': 'STREAMLINE_COFFEE'
    }

    def input(self, in_, out, **kw):
        with NamedTemporaryFile(suffix='._coffee') as input_file:
            input_file.write(in_.read())
            input_file.flush()
            out_filename = path.splitext(input_file.name)[0] + '.js'
            try:
                _coffee = self._coffee or '_coffee'
                args = [_coffee, '-f', '-lm', '-c', input_file.name]
                proc = Popen(args, stdout=PIPE, stderr=PIPE)
                stdout, stderr = proc.communicate()
                if proc.returncode != 0 or stderr:
                    raise FilterError(
                        (
                            'StreamlineCoffee: subprocess had error: %s\n'
                            'stderr=%s, stdout=%s, returncode=%s'
                        ) % (kw['source'], stderr, stdout, proc.returncode)
                    )
                with open(out_filename) as f:
                    out.write(f.read())
            finally:
                if path.exists(out_filename):
                    os.remove(out_filename)


def requirefy(module):
    class Requirefy(Filter):
        max_debug_level = None

        def output(self, in_, out, **kw):
            out.write(
                """requirefy.regist(%s, function(__filename, module, exports){
                    %s
                    }, this)
                """ % (json.dumps(module), in_.read())
            )
    return Requirefy

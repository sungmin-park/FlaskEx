from webassets.filter import Filter
from webassets.exceptions import FilterError
from webassets import Bundle
from subprocess import Popen, PIPE


class IcedCoffeescript(Filter):
    name = 'icedcoffeescript'
    max_debug_level = None

    def output(self, _in, out, **kw):
        args = "-sp -l inline"
        proc = Popen(['iced', args], stdin=PIPE, stdout=PIPE, stderr=PIPE)
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

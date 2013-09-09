from flask import json
from webassets.filter import Filter


def requirefy_vendors(vendors):
    class RequirefyVendors(Filter):
        max_debug_level = None

        def output(self, in_, out, **kw):
            out.write(in_.read())
            print >> out, "require.addVendors(%s);" % json.dumps(vendors)
    return RequirefyVendors

from flask.ext.script import Manager


class Manager(Manager):
    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)

        @self.command
        def urls():
            for rule in self.app.url_map.iter_rules():
                print "%s -> %s" % (rule, rule.endpoint)

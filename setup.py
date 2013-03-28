from setuptools import setup

setup(
    name='FlaskEx',
    version='0.0.3',
    packages=['flaskex'],
    install_requires=[
        'Flask', 'pyjade', 'pytz', 'iso8601', 'flask-debugtoolbar'
    ],
    # supporting jinja autoescape
    dependency_links = [
        'https://github.com/vamf12/pyjade/tarball/fix_jinja_attr_escape'
            '#egg=pyjade-2.0.1'
    ]
)

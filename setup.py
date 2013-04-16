from setuptools import setup

setup(
    name='FlaskEx',
    version='0.0.14',
    packages=['flaskex'],
    zip_safe=False,
    install_requires=[
        'Flask', 'Flask-WTF', 'Flask-Script', 'Flask-SQLAlchemy',
        'pyjade==2.0.1b', 'pytz', 'iso8601', 'flask-debugtoolbar',
        'facebook-sdk'
    ],
    # supporting jinja autoescape
    dependency_links=[
        'https://github.com/vamf12/pyjade/tarball/fix_jinja_attr_escape'
        '#egg=pyjade-2.0.1b'
    ]
)

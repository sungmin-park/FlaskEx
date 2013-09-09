from setuptools import setup

setup(
    name='FlaskEx',
    version='0.0.59',
    packages=[
        'flaskex', 'flaskex.ex', 'flaskex.ext', 'flaskex.forms', 'flaskex.sns',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask', 'Flask-WTF', 'Flask-SQLAlchemy',
        'Flask-Assets', 'alembic', 'pyjade==2.0.1b', 'pytz', 'iso8601',
        'flask-debugtoolbar', 'facebook-sdk', 'glob2', 'simplejson', 'lepl',
        'Flask-Script<0.6'  # flask-assets dose not support 0.6
    ],
    # supporting jinja autoescape
    dependency_links=[
        'https://github.com/vamf12/pyjade/tarball/fix_jinja_attr_escape'
        '#egg=pyjade-2.0.1b'
    ]
)

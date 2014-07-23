#-*- coding:utf-8 -*-
from setuptools import setup, find_packages

kwargs = {}
try:
    from babel.messages import frontend as babel
    kwargs['cmdclass'] = {
        'extract_messages': babel.extract_messages,
        'update_catalog': babel.update_catalog,
        'compile_catalog': babel.compile_catalog,
        'init_catalog': babel.init_catalog,
    }
    kwargs['message_extractors'] = {
        'cogenda_app': [
            ('**.py', 'python', None),
            ('**/templates/**.html', 'jinja2', {
                'extensions': (
                    'jinja2.ext.autoescape,'
                    'jinja2.ext.with_,'
                    'jinja2.ext.do,'
                )
            }),
            ('**/templates/**.md', 'jinja2', {
                'extensions': (
                    'jinja2.ext.autoescape,'
                    'jinja2.ext.with_,'
                    'jinja2.ext.do,'
                    'cogenda_app.lib.md2_extension.md2ext,'
                )
            })
        ]
    }
except ImportError:
    pass


install_requires = [
    'cherrypy',
    'Jinja2',
    'SQLalchemy',
    'sqlalchemy-migrate',
    'Babel',
    'routes',
    'mailer',
    'markdown2',
    'fuzzywuzzy'
]

setup(
    name='cogenda-web',
    version='0.0.1',
    author='cogenda-dev-team',
    author_email='support@cogenda.com',
    url='http://cogenda.com',
    packages=find_packages(exclude=['tests', 'tests.*']), 
    install_requires=install_requires,
    zip_safe=False,
    include_package_data=True,
    **kwargs
)

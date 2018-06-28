from setuptools import setup

import os

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages

packages = find_packages(".")

setup(
    name='namex',
    packages=packages.keys(),
    package_dir=packages,
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-restplus',
        'flask-sqlalchemy',
        'flask-marshmallow',
        'flask-migrate',
        'flask-oidc',
        'marshmallow',
        'marshmallow-sqlalchemy',
        'psycopg2-binary',
        'gunicorn',
        'python-dotenv',
        'python-jose',
        'six',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    classifiers=[
          'Development Status :: 8 - Beta',
          'Environment :: Console',
          'Environment :: Web API',
          'Intended Audience :: API Service Users',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache 2.0 License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Communications :: Email',
          'Topic :: Office/Business :: BC Government Registries',
          'Topic :: Software Development :: GitHub Issue Tracking',
    ],
)

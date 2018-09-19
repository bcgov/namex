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


def read_requirements(filename):
    """
    Get application requirements from
    the requirements.txt file.
    :return: Python requirements
    :rtype: list
    """
    with open(filename, 'r') as req:
        requirements = req.readlines()
    install_requires = [r.strip() for r in requirements if r.find('git+') != 0]
    return install_requires


def read(filepath):
    """
    Read the contents from a file.
    :param str filepath: path to the file to be read
    :return: file contents
    :rtype: str
    """
    with open(filepath, 'r') as f:
        content = f.read()
    return content


packages = find_packages(".")
requirements = read_requirements('requirements.txt')


setup(
    name='colin-api',
    version='0.1.1b',
    packages=packages.keys(),
    package_dir=packages,
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-RESTplus',
        'flask-jwt-oidc',
        'python-dotenv',
        'marshmallow',
        'marshmallow-sqlalchemy',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    classifiers=[
          'Development Status :: Beta',
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

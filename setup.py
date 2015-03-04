try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements
import uuid

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("./requirements.txt", session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

config = {
    'description': 'Unisson Data Server',
    'author': 'Unisson',
    'url': 'Unisson.co',
    'download_url': 'https://github.com/UnissonCo/dataserver',
    'author_email': 'commons-dev＠ulists.org',
    'version': '0.1',
    'install_requires': reqs,
    'packages': ['dataserver'],
    'scripts': [],
    'name': 'dataserver'
}

setup(**config)

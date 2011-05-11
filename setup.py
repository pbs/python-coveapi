from distutils.core import setup

setup(
    name = 'python-coveapi',
    version = '0.1b',
    packages = ['coveapi', ],
    author = 'Drew Engelson',
    author_email = 'dsengelson@pbs.org',
    url = 'http://github.com/pbs/python-coveapi',
    license = 'GPLv3',
    description = 'A Python client for the PBS COVE API service.',
    long_description = 'A Python client for the PBS COVE API service.',
    keywords = 'python pbs cove video api',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import re
import sys

try:
    import pypandoc

    readme = pypandoc.convert_file("README.md", "rst")
except (IOError, ImportError):
    readme = ""


package = "gather_scrobble"
requirements = [
    "gather-client-ws<1",
    "keyring==23.13.1",
    "python-decouple==3.8",
    "tabulate==0.9.0",
    "pylast==5.1.0",
    "spotipy==2.22.1",
    "docopt==0.6.2",
]
test_requirements = []


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search(
        "^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE
    ).group(1)


def get_author(package):
    """
    Return package author as listed in `__author__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search(
        "^__author__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE
    ).group(1)


def get_email(package):
    """
    Return package email as listed in `__email__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search(
        "^__email__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE
    ).group(1)


# python setup.py register
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    args = {"version": get_version(package)}
    print("You probably want to also tag the version now:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()


setup(
    name="gather-scrobble",
    version=get_version(package),
    description="Gather WebSocket service client",
    long_description=readme,
    author=get_author(package),
    author_email=get_email(package),
    url="https://github.com/pyanderson/gather-scrobble",
    packages=[
        "gather_scrobble",
    ],
    package_dir={"gather_scrobble": "gather_scrobble"},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": ["gather-scrobble = gather_scrobble.cli:main"]
    },
    license="MIT",
    zip_safe=False,
    keywords=["gather", "gather-town", "lastfm", "spotify", "scrobble"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)

# -*- coding: utf-8 -*-
from setuptools import setup
import os
import sys
if sys.version_info[0] < 3:
    from io import open

here = os.path.abspath(os.path.dirname(__file__))

packages = ["mixvel"]

requires = [
    "lxml==3.7.2",
    "requests>=2.21.0, <3",
]

test_requirements = [
    "pytest==4.6.11",
]

about = {}
with open(os.path.join(here, "src/mixvel", "__version__.py"), encoding="utf-8") as f:
    exec(f.read(), about)

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=packages,
    package_dir={"mixvel": "src/mixvel"},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    tests_require=test_requirements,
)

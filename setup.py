# -*- coding: utf-8 -*-
"""Installer for the imio.urban.core package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='imio.urban.core',
    version='0.1',
    description="Core of application managing urban and environment licences for townships.",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='urban imio',
    author='Simon Declourt',
    author_email='simon.delcourt@imio.be',
    url='http://pypi.python.org/pypi/imio.urban.core',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['imio', 'imio.urban'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.z3cform.datagridfield',
        'plone.api',
        'plone.app.referenceablebehavior',
        'plone.formwidget.masterselect',
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)

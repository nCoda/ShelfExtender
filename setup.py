#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           ShelfExtender
# Program Description:    Programmatically fake a Mercurial repository.
#
# Filename:               setup.py
# Purpose:                Configuration for installation with setuptools.
#
# Copyright (C) 2016 Christopher Antila
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------
'''
Configuration for installation with setuptools.
'''

from setuptools import setup, Command
import shelfex  # for __version__


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


with open('README.rst', 'r') as file_pointer:
    _LONG_DESCRIPTION = file_pointer.read()

setup(
    name = 'ShelfExtender',
    version = shelfex.__version__,
    packages = ['shelfex'],

    install_requires = ['mercurial-hug'],
    tests_require = ['pytest>2.7,<3'],

    cmdclass = {'test': PyTest},

    # metadata for upload to PyPI
    author = 'Christopher Antila',
    author_email = 'christopher@antila.ca',
    description = 'Programmatically fake a Mercurial repository.',
    long_description = _LONG_DESCRIPTION,
    license = 'GPLv3+',
    keywords = 'vcs, version control, mercurial, shelving',
    url = 'https://goldman.ncodamusic.org/diffusion/SHELF/',
    classifiers =[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Version Control',
    ],
)

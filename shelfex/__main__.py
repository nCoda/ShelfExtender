#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           ShelfExtender
# Program Description:    Programmatically fake a Mercurial repository.
#
# Filename:               shelfex/__main__.py
# Purpose:                Main ShelfExtender module.
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
Main ShelfExtender module.
'''

import os
import os.path
import shutil
import subprocess
from xml.etree import ElementTree as etree

import hug as mercurial


def load_users(prepdir):
    '''
    Load and process the list of users.

    :param str prepdir: Path to the "prep directory" containing ``users.xml``.
    :returns: Dictionary with dictionaries of user data. Keys in the top-level data are the
        ``userid`` given in the XML file.
    :rtype: dict

    **Example:**

    >>> shelfex.load_users('.')
    {
        'bs': {
            'name': 'Blanzifor Solle',
            'email': 'bs@example.org',
        },
        'fu': {
            'name': 'Fulgebrandt Urquhart',
            'email': 'fu@example.org',
        },
    }
    '''
    parsed = etree.parse(os.path.join(prepdir, 'users.xml')).getroot()
    assert parsed.tag == 'users'

    users = {}

    for user in parsed.iter(tag='user'):
        assert user.get('userid')
        assert user.get('name')
        assert user.get('email')
        users[user.get('userid')] = {'name': user.get('name'), 'email': user.get('email')}

    return users


def load_revlog(prepdir):
    '''
    Load and process the revlog.

    :param str prepdir: Path to the "prep directory" containing ``revlog.xml``.
    :returns: List with the dictionaries of changeset data. List index matches the revision number.
    :rtype: list

    **Example:**
    >>> shelfex.load_revlog('.')
    [
        {
            'revnumber': '0',
            'message': 'first commit!',
            'userid': 'bs',
            'date': 'Sat Apr 30 23:09:54 2016 -0400',
        },
        {
            'revnumber': '1',
            'message': 'fix a spelling mistake',
            'userid': 'bs',
            'date': 'Tue Dec 08 01:25:03 2015 -0500',
        },
        {
            'revnumber': '2',
            'message': 'add some more text',
            'userid': 'fu',
            'date': 'Tue Mar 03 15:00:00 2015 -0500',
        },
    ]
    '''
    parsed = etree.parse(os.path.join(prepdir, 'revlog.xml')).getroot()
    assert parsed.tag == 'revlog'

    revlog = []

    revnumber = -1
    while True:
        revnumber += 1
        revision = parsed.find('./revision[@revnumber="{0}"]'.format(revnumber))
        if revision is not None:
            revlog.append({
                'revnumber': str(revnumber),
                'message': revision.find('./message').text,
                'userid': revision.find('./userid').text,
                'date': revision.find('./date').text,
            })
        else:
            break

    return revlog


def make_revision(prepdir, hug, users, revlog, revnumber):
    '''
    Make a new revision according to the arguments provided.

    :param prepdir: Path to the directory in which to find revision data.
    :param hug: A :class:`hug.Hug` instance for the repository being built.
    :param users: Output from :func:`load_users`.
    :param revlog: Output from :func:`load_revlog`.
    :param int revnumber: The revision number to make.
    '''
    assert revlog[revnumber]
    rev_dir = os.path.join(prepdir, str(revnumber))
    assert os.path.exists(rev_dir)
    assert os.path.isdir(rev_dir)

    # copy all files from rev_dir to Hug's directory
    destdir = hug.repo_dir
    copied_files = []
    for directory, _, filenames in os.walk(rev_dir):
        for filename in filenames:
            src = os.path.join(directory, filename)
            dest = os.path.join(destdir, filename)
            shutil.copy2(src, dest)
            copied_files.append(dest)

    # "add" all the files that were copied
    hug.add(copied_files)

    # make the commit
    rev = revlog[revnumber]
    rev_user = users[rev['userid']]
    hug.username = u'{0} <{1}>'.format(rev_user['name'], rev_user['email']).encode('utf-8')
    hug.commit(message=rev['message'].encode('utf-8'), date=rev['date'].encode('utf-8'))


def build_repo(prepdir):
    '''
    '''
    prepdir = os.path.abspath(prepdir)
    assert os.path.exists(prepdir)
    assert os.path.isdir(prepdir)
    assert os.path.exists(os.path.join(prepdir, 'users.xml'))
    assert os.path.exists(os.path.join(prepdir, 'revlog.xml'))

    # delete a previous attempt, if required
    destdir = os.path.join(prepdir, 'repo')
    if os.path.exists(destdir):
        # I know it's a little sloppy, but it's also a fast stand-in!
        return_code = subprocess.call(['rm', '-fR', destdir])
        if return_code != 0:
            print('Failed to remove existing "repo" output directory?')
            raise SystemExit(1)

    # initialize the repository
    os.mkdir(destdir)
    hug = mercurial.Hug(destdir, safe=True)

    # load in the users and revlog
    users = load_users(prepdir)
    revlog = load_revlog(prepdir)

    # build the repository
    for revnumber in range(len(revlog)):
        make_revision(prepdir, hug, users, revlog, revnumber)


def main():
    '''
    '''
    # TODO: make this proper?
    build_repo('.')


if __name__ == '__main__':
    main()

ShelfExtender
=============

Programmatically fake a Mercurial repository.

Need to convince your boss that you've been working on a project for four months---definitely not
just since last night? Or perhaps you need a colourful document history to help demonstrate the
amazing version control capabilities of your new web app. "Let's just make a Mercurial repository
with false revlog data," your colleagues said, and sent you to figure out how to do it. You've
searched long and hard for the elusive tool that helps you create a repository from false data...
well here it is!

Check out the "demo" directory for an example use case.


About the Name
^^^^^^^^^^^^^^

Sending a new employee to look for the "shelf extender" is an initiation ritual practised in some
workplaces. It's a joke, because a shelf extender *seems* like something that could exist, but it
doesn't. If you want a longer shelf, you don't use a shelf extender, you just put up more sheves!
There's no need for a separate product to exist. But you don't know that if you just started at
your company; maybe they have shelf extenders, right?

Similar idea with this *ShelfExtender* program. When I realized I needed to create a Mercurial
repository that appeared to show a months-long collaborative document editing process, it felt like
I was looking for a metaphorical shelf extender. If you want to make a revlog, you don't use a
revlog-faker, you just make the revisions!

**UNTIL TODAY.**


How It Works: Users and Revision History
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You provide two configuration files, and a collection of subdirectories indicating the desired
state of the repository after every revision. *ShelfExtender* uses these data to create a repository
with the users, dates, messages, and files you provide.

For example:

.. sourcecode:: xml

    <!-- users.xml -->
    <users>
        <user userid="bs" name="Blanzifor Solle" email="bs@example.org"/>
        <user userid="fu" name="Fulgebrandt Urquhart" email="fu@example.org"/>
    </users>

.. sourcecode:: xml

    <!-- revlog.xml -->
    <revlog>
        <revision revnumber="0">
            <message>first commit!</message>
            <userid>bs</userid>
            <date>Sat Apr 30 23:09:54 2016 -0400</date>
        </revision>
        <revision revnumber="1">
            <message>fix a spelling mistake</message>
            <userid>bs</userid>
            <date>Tue Dec 08 01:25:03 2015 -0500</date>
        </revision>
        <revision revnumber="2">
            <message>add some more text</message>
            <userid>fu</userid>
            <date>Tue Mar 03 15:00:00 2015 -0500</date>
        </revision>
    </revlog>

Produces a revlog like this::

    changeset:   2:0a8e04b56145
    tag:         tip
    user:        Fulgebrandt Urquhart <fu@example.org>
    date:        Tue Mar 03 15:00:00 2015 -0500
    summary:     add some more text

    changeset:   1:833edfbc92da
    user:        Blanzifor Solle <bs@example.org>
    date:        Tue Dec 08 01:25:03 2015 -0500
    summary:     fix a spelling mistake

    changeset:   0:bca47dae8f7b
    user:        Blanzifor Solle <bs@example.org>
    date:        Sat Apr 30 23:09:54 2016 -0400
    summary:     first commit!

See how the dates make it look like the revisions go back in time? Did you think I was kidding? You
can make commits before Mercurial was written, before you were born, before computers existed---it
doesn't matter any more! NOTHING MEANS ANYTHING FOR SURE!!!

You must provide the @revnumber attribute on ``<revision>`` elements, and the enumeration must
start at 0. *ShelfExtender* ignores ``<revision>`` elements without a @revnumber attribute, and
stops working after one @revnumber is missing.


How It Works: Files in the Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make a directory with the revnumber of a changeset. The files in that directory are *copied over*
the files from the previous changeset, added to the repository, and committed. Therefore you don't
need to make a copy of the whole repository for every changeset: you only need to include the files
that change.

Consider the following directory layout::

    0 -
      a.txt
      b.txt
      c.txt
    1 -
      c.txt
    2 -
      d.txt

In this situation, revision 0 introduces three files; revision 1 *changes* one file, so there are
still three in the repository; revision 2 *adds* one file, so there are now four in the repository.


Limitations
^^^^^^^^^^^

These limitations currently apply. They're not technical problems, I just haven't implemented it
yet because I don't care. Yet.

- You can't delete a file from the repository.
- You can't make branches.
- You can't make tags.
- You can't ask *ShelfExtender* to apply a diff; you have to give it the whole file you want.


Run ShelfExtender
^^^^^^^^^^^^^^^^^

1. Install *ShelfExtender* and its requirements in a virtualenv.
1. Prepare the repository configuration as described above.
1. Put your shell into the directory with the configuration.
1. Run ``python -m shelfex``.
1. Profit!





a

..                                 utilia

.. This work is licensed under the Creative Commons Attribution 3.0 
   Unported License. To view a copy of this license, visit 

      http://creativecommons.org/licenses/by/3.0/ 

Installation Guide
==================

As the software released by the project is primarily based off of Python, it
probably should go without saying that you need to have a working Python
installation. The following instructions assume that you do.

Releases
--------

Currently no releases have been made available. 

.. todo::
   Mention listing on PyPI.

.. todo::
   Give examples of easy_install and pip.
   For both site-wide and user-specific installations.

Tracking Development
--------------------

To follow the latest development on the project, you will need a Git client if
you do not already have one.

General Git Clients: Linux, BSD, Solaris
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
You may have already have a Git cleint installed, if you are using a Linux or 
BSD-like OS distribution. If you need to install one and can acquire superuser 
privileges, then here are instructions for some popular distributions:
   
   http://www.git-scm.com/download/linux

or you can build from sources and install into whatever location for which you
have write permissions:
   
   https://github.com/git/git/tags

(You will probably want to download the latest tagged release which does not
have *rc* in its name.)

If you are running on another Unix-like OS, then building from sources may be
your only option.

General Git Clients: MacOS X
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are on MacOS X, then you can get a package to install from here:
   
   http://www.git-scm.com/download/mac

(If you do not have the necessary privileges to install the package, you can
also attempt to build from sources. Please the see the instructions for Linux
and the other Unix-like systems above.)

If you are using MacPorts, then you can also install Git using the installer
for that distribution.

General Git Clients: Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are on Windows, then you can get an installer from here:
   
   http://www.git-scm.com/download/win

or from here:

   http://msysgit.github.com

If you are a Windows user, familiar with Linux or another Unix-like operating
system, then *msysGit* is recommended.

There are also a number of GUI Git clients for Windows, such as:
   
   http://code.google.com/p/gitextensions/

   http://code.google.com/p/tortoisegit/

GitHub GUI Clients: MacOS X and Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The master software repository is hosted on GitHub. Several special Git 
clients exist for working with repositories on GitHub.

If you are on MacOS X, then you may wish to try:
   
   http://mac.github.com/

If you are on Windows, then you may wish to try:

   http://windows.github.com/

Working with Command-Line Git Clients
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many of the Git clients listed above are operated from a command shell.

Users of Unix-like operating systems probably need no instruction on how to 
access a command line.

If you are on MacOS X, then you may need the ``Terminal`` application located 
in the ``Utilities`` folder inside the ``Applications`` folder, shown in a 
Finder window.

If you are Windows, then you may have shortcut to start a command console; 
this shortcut is likely located in a folder created by your Git client's 
installer program under the ``All Programs`` folder off of the Start Menu. If
you are using *msysGit*, then you can also right-click in a folder displayed in
an Explorer window to get a context menu with some Git-related options, one of
which should be ``Git Bash``.

Once you have a command shell in front of you and you have navigated into
whatever directory you wish, then you should be able to use the following
command to clone the official software repository off of GitHub:

   .. code-block:: sh

      git clone http://github.com/utilia/utilia.git

From time-to-time, you may wish to update to the latest sources in the
directory where your clone of the official repository resides. You can use the
following command to accomplish this:

   .. code-block:: sh

      git pull

.. todo::
   Talk about tracking branches.

.. todo::
   Add repo tracking instructions for popular GUI clients.

.. todo::
   Detail procedure for building versions off of GitHub.

.. todo::
   Talk about virtual environments.

.. TODO: Once relevant, add subsection on building extensions.
         Include platform-specific notes, such as for x64 Windows.

.. vim: set ft=rst ts=3 sts=3 sw=3 et tw=79:

..                                utilia

.. This work is licensed under the Creative Commons Attribution 3.0 Unported
   License. To view a copy of this license, visit 

      http://creativecommons.org/licenses/by/3.0/ 

Modules Library
---------------

*  Enhanced support for finding and utilizing localization resources, such as
   translations.

*  Generic tester functions, which may be used with testing frameworks or for
   other purposes.

*  Unified parsing of command-line and config file options.

*  Extensions to the 
   :py:mod:`distutils.ccompiler <CPython2:distutils.ccompiler>` 
   module for proper support of standalone Mingw32 and Mingw64.

*  An extension to the :py:mod:`logging <CPython3:logging>` module, which
   allows for logging to GUI message boxes. (Useful for showing critical errors
   before intended GUI subsytem is initialized or when operating in a headless
   or minimized-to-tray mode, in some cases.) Would try toolkit for current
   window manager first, before attempting to fallback to others.

*  Wrapper for the `PDCurses <http://pdcurses.sourceforge.net/>`_ library to 
   provide a more-portable *curses* implementation with some interesting 
   back-end options (e.g., SDL).

*  Wrapper for the `AAlib <http://aa-project.sourceforge.net/aalib/>`_ or 
   `libcaca <http://caca.zoy.org/wiki/libcaca>`_ library.


Scripts Collections
-------------------

*  Replacement, augmentation, deletion, or creation of text blocks within all
   files matching a pattern within a directory hierarchy. Allow for lines,
   matching a regular expression, to be preserved during replacement.

*  Searching and reporting on inventories used by Sphinx's ``intersphinx``
   extension.

*  Exploration and searching of the PE-COFF format.


.. vim: set ft=rst ts=3 sts=3 sw=3 et tw=79:

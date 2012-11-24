..				   utilia

.. This work is licensed under the Creative Commons Attribution 3.0 
   Unported License. To view a copy of this license, visit 

      http://creativecommons.org/licenses/by/3.0/ 

.. include:: ../../README.rst.txt

Indices and Search Facility
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :ref:`search`
* :ref:`genindex`
* :ref:`modindex`

Modules Library
---------------

All of the modules in the library, provided by this project, are contained in 
the :py:mod:`utilia` package. The modules have a wide variety of purposes, but
are united by a common theme, which has the following features:

   * Compatibility across multiple implementations and versions of Python.
     This compatibility is maintained **without** the use of automatic code 
     translators, such as :file:`2to3`. Presently, compatibility with the
     following implementations and versions of Python is maintained:

     * CPython (http://www.python.org), versions 2.6 and 2.7 and all versions
       from the 3.x series

   * Well-documented programming interfaces, including examples.

   * Useful, general purpose functionality, not provided by the Python standard
     library or available as robust, stand-alone implementations by third
     parties.

   * Seamless interoperability amongst components, when such interoperability
     is desirable and meaningful.

The modules library currently provides the following:

   * Useful, portable data structures, such as ordered dictionaries.

   * Awareness of the standard filesystem layouts of various operating 
     systems; reporting of standard paths to configuration information, 
     application data stores, temporary spaces, saved documents, etc....

Much more functionality is planned (and already exists as less polished,
unreleased code). This includes:

   * Enhanced support for finding and utilizing localization resources, 
     such as translations.

   * Generic tester functions, which may be used with testing frameworks or 
     for other purposes.

   * Unified parsing of command-line and config file options.

Scripts Collection
------------------

The collected scripts serve a wide variety of purposes, but the following
features in common:

   * Written in Python with the same compatibility level as the 
     accompanying modules library.

   * Flexible execution in an OS-independent manner.

   * Well-documented invocation arguments and options, operations, and exit
     codes. Usage examples are also included in the documentation.

   * Useful, general purpose functionality.

   * Seamless interoperability amongst scripts, when such interoperability is
     desirable and meaningful.

Currently, no scripts exist in the collection, but ones implementing the 
following functionality are planned (some of which already exist in 
less-polished, unreleased forms):
   
   * Walking a source tree and updating the message catalogs corresponding to
     all translation domains found.

   * Searching inventories used by Sphinx's Intersphinx extension.


.. toctree::
   :maxdepth: 3
   :titlesonly:
   :hidden:

   install/index
   modules/SELF
   scripts/index
   develop/index
   legal/index
   contrib

.. vim: set ft=rst sts=3 sw=3 tw=79:

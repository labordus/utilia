..                                 utilia

.. This work is licensed under the Creative Commons Attribution 3.0 
   Unported License. To view a copy of this license, visit 

      http://creativecommons.org/licenses/by/3.0/ 

``utilia`` Package
==================

Overview
--------

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


Package Description
-------------------

.. automodule:: utilia

Exception Classes
-----------------

.. autoclass:: Exception_BASE
   :members:
   :inherited-members:

.. autoclass:: Error_BASE
   :members:
   :inherited-members:

.. autoclass:: Exception_WithReason
   :members:
   :inherited-members:

.. autoclass:: Exception_Exiting
   :members:
   :inherited-members:

.. autoclass:: InvalidKeyError
   :members:
   :inherited-members:

.. autoclass:: UnknownKeyError
   :members:
   :inherited-members:

.. autoclass:: InvalidValueError
   :members:
   :inherited-members:

.. autoclass:: InvokedAbstractMethodError
   :members:
   :inherited-members:

Subpackages and Modules
-----------------------

.. toctree::
   :titlesonly:

   compat/SELF
   config_parsers/SELF
   filesystem/SELF
   functional/SELF
   types/SELF

.. vim: set ft=rst ts=3 sts=3 sw=3 et tw=79:

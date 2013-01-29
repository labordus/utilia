###############################################################################
#                                  utilia                                     #
#-----------------------------------------------------------------------------#
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
#                                                                             #
###############################################################################

"""
    Provides a compatibility layer among the different implementations and
    versions of Python. This is achieved by providing access to modules,
    classes, and functions via a uniform naming convention.

    The following modules are available:
        
        * A :py:mod:`command-line argument parser <.argparse>` module, which
          provides a uniform implementation across Pythons, regardless of
          whether they have one in their standard library.

        * A :py:mod:`built-ins <.builtins>` module, which shadows the 
          appropriate Python one and provides missing pieces.

        * A shadow of the Python :py:mod:`collections <.collections>` module, 
          which provides missing pieces.

        * A :py:mod:`configuration file parser <.configparser>` module, which
          shadows the appropriate Python one.
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


from utilia import python_version


# Dictionary Iterators


if 3 == python_version.major:


    def iter_dict_keys( the_dict ):

        return iter( the_dict.keys( ) )


    def iter_dict_values( the_dict ):

        return iter( the_dict.values( ) )


    def iter_dict_items( the_dict ):
        
        return iter( the_dict.items( ) )


else: # Other than Python 3.
    

    def iter_dict_keys( the_dict ):
        
        return the_dict.iterkeys( )
    

    def iter_dict_values( the_dict ):
        
        return the_dict.itervalues( )
    

    def iter_dict_items( the_dict ):
        
        return the_dict.iteritems( )


# Add in-common docstrings.

iter_dict_keys.__doc__ = \
"""
    Returns an iterator which generates keys from the given dictionary.

    In Python 2, attempts a call to the :py:meth:`iterkeys
    <CPython2:dict.iterkeys>` method of an object.

    :param the_dict: an object conforming to the :py:class:`dictionary 
                     <CPython2:dict>` interface
    :rtype: a Python 2 dictionary iterator

    In Python 3, attempts a call to the :py:meth:`keys <CPython3:dict.keys>`
    method of an object and wraps the resulting view in an iterator.

    :param the_dict: an object conforming to the :py:class:`dictionary 
                     <CPython3:dict>` interface
    :rtype: a Python 3 dictionary iterator
"""

iter_dict_values.__doc__ = \
"""
    Returns an iterator which generates values from the given dictionary.

    In Python 2, attempts a call to the :py:meth:`itervalues
    <CPython2:dict.itervalues>` method of an object.

    :param the_dict: an object conforming to the :py:class:`dictionary 
                     <CPython2:dict>` interface
    :rtype: a Python 2 dictionary iterator

    In Python 3, attempts a call to the :py:meth:`values 
    <CPython3:dict.values>` method of an object and wraps the resulting view 
    in an iterator.

    :param the_dict: an object conforming to the :py:class:`dictionary 
                     <CPython3:dict>` interface
    :rtype: a Python 3 dictionary iterator
"""

iter_dict_items.__doc__ = \
"""
    Returns an iterator which generates key-value pairs from the given
    dictionary.

    In Python 2, attempts a call to the :py:meth:`iteritems
    <CPython2:dict.iteritems>` method of an object.

    :param the_dict: an object conforming to the :py:class:`dictionary 
                     <CPython2:dict>` interface
    :rtype: a Python 2 dictionary iterator

    In Python 3, attempts a call to the :py:meth:`items <CPython3:dict.items>`
    method of an object and wraps the resulting view in an iterator.

    :param the_dict: an object conforming to the :py:class:`dictionary 
                     <CPython3:dict>` interface
    :rtype: a Python 3 dictionary iterator
"""


# Abstract Base Classes


from abc import (
    ABCMeta,
)


if 2 == python_version.major:
    exec( # pylint: disable=W0122
        """class AbstractBase_BASE: __metaclass__ = ABCMeta"""
    )
else:
    exec( # pylint: disable=W0122
        """class AbstractBase_BASE( metaclass = ABCMeta ): pass"""
    )
# Note: Hack to make parse-only lint tools happy.
AbstractBase_BASE = vars( )[ "AbstractBase_BASE" ]

AbstractBase_BASE.__doc__ = \
"""
    Generalized abstract class, which has :py:class:`abc.ABCMeta
    <CPython3:abc.ABCMeta>` as its metaclass.

    Subclass this in any implementation of Python supported by the library to
    create abstract methods and properties and use the ``__subclasshook__``
    override and the subclass registration machinery from 
    :py:class:`abc.ABCMeta <CPython3:abc.ABCMeta>`.
"""


del ABCMeta


# Module Cleanup

del python_version


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

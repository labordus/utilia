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
    Provides common logic operators as functions.

    The functions come in two forms: *objective* and *boolean*. Objective
    functions work in a manner similar to the :py:keyword:`and <CPython3:and>`
    and :py:keyword:`or <CPython3:or>` operators, built in to Python, in that
    return one of the original objects provided as an operand. Boolean
    functions return boolean values rather than the original objects. The names
    of objective functions start with ``o_``.

    The names of all functions in the module end with ``f``, because some of
    the names would otherwise conflict with Python keywords. The ``f`` can be
    understood to mean *function* or *functional version* as opposed to an
    inline operator.

    None of the functions in this module perform true *short-circuit*
    evaluation like the Python :py:keyword:`and <CPython3:and>` and 
    :py:keyword:`or <CPython3:or>` operators do.  This is because any 
    expressions given as arguments to a function are evaluated before the 
    function is called.

    The documentation below and the 
    :ref:`SECTION-utilia.functional.logic-Examples` section provide more
    details.
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


def __DOCSTRING_FRAGMENTS( ):
    """
        Returns a dictionary of common docstring fragments.
    """
    return \
    {
        "posargs": \
    """
        :param posargs: Arbitrary number of positional arguments.
        :type posargs: objects of any type
    """,
        "RTYPE_any": \
    """
        :rtype: object of any type
    """,
        "RTYPE_boolean": \
    """
        :rtype: :py:func:`boolean <CPython3:bool>`
    """,
        "RAISES_TypeError (on missing argument)": \
    """
        :raises: :py:exc:`TypeError <CPython3:TypeError>`, if a required 
                 argument is missing.
    """,
    }


def andf( *posargs ):
    """
        If no arguments are supplied, returns True.
        Else, returns the result of calling the 
        :py:func:`all <CPython3:all>` built-in function on the sequence of 
        arguments.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\wedge q`"

           "``False``", "``False``",    "``False``"
           "``False``", "``True``",     "``False``"
           "``True``",  "``False``",    "``False``"
           "``True``",  "``True``",     "``True``"

    """

    return all( posargs )

andf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
andf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]


def nandf( *posargs ):
    """
        If no arguments are supplied, returns False.
        Else, returns the negated result of calling the 
        :py:func:`all <CPython3:all>` built-in function on the sequence of 
        arguments.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\uparrow q`"

           "``False``", "``False``",    "``True``"
           "``False``", "``True``",     "``True``"
           "``True``",  "``False``",    "``True``"
           "``True``",  "``True``",     "``False``"

    """

    return not all( posargs )

nandf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
nandf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]


def orf( *posargs ):
    """
        If no arguments are supplied, returns False.
        Else, returns the result of calling the 
        :py:func:`any <CPython3:any>` built-in function on the sequence of 
        arguments.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\vee q`"

           "``False``", "``False``",    "``False``"
           "``False``", "``True``",     "``True``"
           "``True``",  "``False``",    "``True``"
           "``True``",  "``True``",     "``True``"

    """

    return any( posargs )

orf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
orf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]


def norf( *posargs ):
    """
        If no arguments are supplied, returns True.
        Else, returns the negated result of calling the 
        :py:func:`any <CPython3:any>` built-in function on the sequence of 
        arguments.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\downarrow q`"

           "``False``", "``False``",    "``True``"
           "``False``", "``True``",     "``False``"
           "``True``",  "``False``",    "``False``"
           "``True``",  "``True``",     "``False``"

    """

    return not any( posargs )

norf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
norf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]


def xorf( *posargs ):
    """
        Converts sequence of arguments to booleans.
        If no arguments are supplied, raises an exception.
        Else, returns the result of reducing the sequence of arguments with a
        logical ``xor`` function.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\veebar q`"

           "``False``", "``False``",    "``False``"
           "``False``", "``True``",     "``True``"
           "``True``",  "``False``",    "``True``"
           "``True``",  "``True``",     "``False``"

    """

    return reduce( lambda p, q: p != q, map( bool, posargs ) )

xorf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
xorf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]
xorf.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_TypeError (on missing argument)" ]


def xnorf( *posargs ):
    """
        Converts sequence of arguments to booleans.
        If no arguments are supplied, raises an exception.
        Else, returns the result of reducing the sequence of arguments with a
        logical ``xnor`` function.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\Leftrightarrow q`"

           "``False``", "``False``",    "``True``"
           "``False``", "``True``",     "``False``"
           "``True``",  "``False``",    "``False``"
           "``True``",  "``True``",     "``True``"

    """

    return not reduce( lambda p, q: p != q, map( bool, posargs ) )

xnorf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
xnorf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]
xnorf.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_TypeError (on missing argument)" ]


def impliesf( *posargs ):
    """
        Converts sequence of arguments to booleans.
        If no arguments are supplied, raises an exception.
        Else, returns the result of reducing the sequence of arguments with a
        logical ``implies`` function.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\Rightarrow q`"

           "``False``", "``False``",    "``True``"
           "``False``", "``True``",     "``True``"
           "``True``",  "``False``",    "``False``"
           "``True``",  "``True``",     "``True``"

    """

    return reduce( lambda p, q: not p or q, map( bool, posargs ) )

impliesf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
impliesf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]
impliesf.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_TypeError (on missing argument)" ]


def nimpliesf( *posargs ):
    """
        Converts sequence of arguments to booleans.
        If no arguments are supplied, raises an exception.
        Else, returns the negated result of reducing the sequence of arguments 
        with a logical ``implies`` function.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\nRightarrow q`"

           "``False``", "``False``",    "``False``"
           "``False``", "``True``",     "``False``"
           "``True``",  "``False``",    "``True``"
           "``True``",  "``True``",     "``False``"

    """

    return not reduce( lambda p, q: not p or q, map( bool, posargs ) )

nimpliesf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
nimpliesf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]
nimpliesf.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_TypeError (on missing argument)" ]


def cimpliesf( *posargs ):
    """
        Converts sequence of arguments to booleans.
        If no arguments are supplied, raises an exception.
        Else, returns the result of reducing the sequence of arguments with a
        logical ``converse implies`` function.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\Leftarrow q`"

           "``False``", "``False``",    "``True``"
           "``False``", "``True``",     "``False``"
           "``True``",  "``False``",    "``True``"
           "``True``",  "``True``",     "``True``"

    """

    return reduce( lambda p, q: p or not q, map( bool, posargs ) )

cimpliesf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
cimpliesf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]
cimpliesf.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_TypeError (on missing argument)" ]


def cnimpliesf( *posargs ):
    """
        Converts sequence of arguments to booleans.
        If no arguments are supplied, raises an exception.
        Else, returns the negated result of reducing the sequence of arguments 
        with a logical ``converse implies`` function.

        Below is a truth table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\nLeftarrow q`"

           "``False``", "``False``",    "``False``"
           "``False``", "``True``",     "``True``"
           "``True``",  "``False``",    "``False``"
           "``True``",  "``True``",     "``False``"

    """

    return not reduce( lambda p, q: p or not q, map( bool, posargs ) )

cnimpliesf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
cnimpliesf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_boolean" ]
cnimpliesf.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_TypeError (on missing argument)" ]


def o_andf( *posargs ):
    """
        If no arguments are supplied, returns True.
        Else, returns the result of reducing the sequence of arguments with the
        logical :py:keyword:`and <CPython3:and>` operator.

        Below is a *truth-like* table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\wedge q`"

           "zeroish",       "zeroish",      ":math:`p`"
           "zeroish",       "non-zeroish",  ":math:`p`"
           "non-zeroish",   "zeroish",      ":math:`q`"
           "non-zeroish",   "non-zeroish",  ":math:`q`"
         
    """

    return reduce( lambda p, q: p and q, posargs, True )

o_andf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
o_andf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_any" ]


def o_orf( *posargs ):
    """
        If no arguments are supplied, returns False.
        Else, returns the result of reducing the sequence of arguments with the
        logical :py:keyword:`or <CPython3:or>` operator.

        Below is a *truth-like* table for this function with two arguments:

        .. csv-table::
           :header: ":math:`p`", ":math:`q`", ":math:`p \\\\vee q`"

           "zeroish",       "zeroish",      ":math:`q`"
           "zeroish",       "non-zeroish",  ":math:`q`"
           "non-zeroish",   "zeroish",      ":math:`p`"
           "non-zeroish",   "non-zeroish",  ":math:`p`"
         
    """

    return reduce( lambda p, q: p or q, posargs, False )

o_orf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "posargs" ]
o_orf.__doc__ += __DOCSTRING_FRAGMENTS( )[ "RTYPE_any" ]


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

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
    Provides a wide assortment of useful subpackages. The subpackages cover
    these areas:
        
        * :py:mod:`compatibility between Python implementations <.compat>`

        * :py:mod:`configuration parsing <.config_parsers>`

        * :py:mod:`file systems <.filesystem>`

        * :py:mod:`functional programming <.functional>`
        
        * :py:mod:`.types`
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


import sys
import collections
from os.path import (
    join                    as path_join,
)


# Get Python version.
PythonVersion = collections.namedtuple(
    "PythonVersion", "flavor major minor"
)
# Note: Access 'version_info' members by index rather than name for Python 2.6
#       compatibility.
python_version = PythonVersion(
    sys.subversion[ 0 ], sys.version_info[ 0 ], sys.version_info[ 1 ]
)


# Read the version info from config file.
# Note: If something goes wrong here, then just let the exception propagate.
if 2 == python_version.major:
    from ConfigParser import ( # pylint: disable=F0401
        SafeConfigParser        as __ConfigParser,
    )
else:
    from configparser import ( # pylint: disable=F0401
        SafeConfigParser        as __ConfigParser,
    )

__vinfo_CFG     = __ConfigParser( )
__vinfo_CFG.readfp( open( path_join( __path__[ 0 ], "version.cfg" ) ) )

__vinfo_release_type    = __vinfo_CFG.get( "control", "release_type" )
assert __vinfo_release_type in [ "bugfix", "candidate", "development" ]
__vinfo_numbers_DICT    = dict( __vinfo_CFG.items( "numbers" ) )
if   "bugfix" == __vinfo_release_type: # Stable Bugfix Release
    __version__ = \
    "{major}.{minor}.{bugfix}".format( **__vinfo_numbers_DICT )
elif "candidate" == __vinfo_release_type: # Release Candidate
    __version__ = \
    "{major}.{minor}.0rc{update}".format( **__vinfo_numbers_DICT )
elif "development" == __vinfo_release_type: # Development Release
    __vinfo_numbers_DICT[ "update" ] = \
    open( path_join( __path__[ 0 ], "dev-timestamp.dat" ) ).read( 12 )
    __version__ = \
    "{major}.{minor}.0dev{update}".format( **__vinfo_numbers_DICT )

del __ConfigParser, __vinfo_CFG, __vinfo_release_type, __vinfo_numbers_DICT


# Cleanup the module namespace.
del path_join, collections


# Utility Functions
# (Assorted functions used throughout the package.)


# Alias 'range' built-in function to 'xrange' for Python 2 compatibility.
if 3 == python_version.major:
    xrange = range # pylint: disable=W0622


def _autodoc_function_parameters( func, pdict ):
    """
        Automatically document a function's parameters, if
        the supplied dictionary has entries for their names.

        Note: This function assumes that the first entries of the 'co_varnames'
              tuple are the parameters passed on the stack.
    """

    for i in xrange( func.__code__.co_argcount ):
        docs = pdict.get( func.__code__.co_varnames[ i ], None )
        if docs: func.__doc__ += docs


def _TD_( s ):
    """
        Dummy translator function.

        Passes its argument through without translation at runtime, 
        but marks it to be collected into a message catalog during a scan for
        translatable strings. This allows for it to be translated when it is 
        referenced.

        One use for this is to collect exception messages to be translated
        without immediate display.
    """

    return s


# Exceptions


from abc import (
    ABCMeta,
)


if 2 == python_version.major:
    exec( # pylint: disable=W0122
        """class Exception_BASE: __metaclass__ = ABCMeta"""
    )
else:
    exec( # pylint: disable=W0122 
        """class Exception_BASE( metaclass = ABCMeta ): pass"""
    )
# Note: Hack to make parse-only lint tools happy.
Exception_BASE = vars( )[ "Exception_BASE" ]

Exception_BASE.__doc__ = \
"""
    Abstract base class for all :py:mod:`utilia` exceptions.

    Use this for your exception handler signature if you wish to catch any
    exception raised from within :py:mod:`utilia`.
"""


if 2 == python_version.major:
    exec( # pylint: disable=W0122
        """class Error_BASE: __metaclass__ = ABCMeta"""
    ) 
else:
    exec( # pylint: disable=W0122
        """class Error_BASE( metaclass = ABCMeta ): pass"""
    )
# Note: Hack to make parse-only lint tools happy.
Error_BASE = vars( )[ "Error_BASE" ]
Exception_BASE.register( Error_BASE )

Error_BASE.__doc__ = \
"""
    Abstract base class for all :py:mod:`utilia` exceptions 
    which are regarded as errors.

    Use this for your exception handler signature if you wish to catch any
    error condition raised from within :py:mod:`utilia`.
"""


class Exception_WithRC( object ): # pylint: disable=R0903
    """
        Mix-in class for all :py:mod:`utilia` exceptions which carry a return 
        code that could be supplied to a 
        :py:exc:`SystemExit <CPython3:SystemExit>` exception.

        Inherits from :py:class:`object <CPython3:object>`.

        Use this for your exception handler signature if you wish to catch any
        exception, which has a return code, raised from within
        :py:mod:`utilia`.
    """


    _rc              = 0


    def __init__( self, *posargs ): # pylint: disable=W0613
        """
            Sets the return code to carry with the exception.
        """

        super( Exception_WithRC, self ).__init__( )
        self._rc = 0


    def __repr__( self ):
        """
            Returns a string which can be used by :py:func:`eval
            <CPython3:eval>` to create an instance of the class.
        """

        return "Exception_WithRC( ) # rc = {0}".format( self._rc )


    def __str__( self ):
        """
            Returns the return code as a string.
        """

        return self._rc_str( )


    def _rc_str( self ):
        """
            Returns the return code as a string.

            Call this from a subclass if the return code is needed as a 
            string.
        """

        return str( self._rc )


    @property
    def rc( self ):
        """
            The return code.
        """

        return self._rc

Exception_BASE.register( Exception_WithRC )


class Exception_WithReason( object ):
    """
        Mix-in class for all :py:mod:`utilia` exceptions which carry a 
        translatable format string and a tuple of arguments for 
        substitution into the format string.

        Inherits from :py:class:`object <CPython3:object>`.

        Use this for your exception handler signature if you wish to catch any
        exception, which has a translatable reason string, raised from
        within :py:mod:`utilia`.
    """


    _reason_format       = ""
    _reason_args         = [ ]


    def __init__( self, reason_format, *reason_args ):
        """
            Sets the reason format string to carry with the exception.

            :param reason_format: Format string, containing zero or more 
                                  :py:func:`format <CPython3:format>`-style 
                                  substitution tokens, for presentation as the
                                  reason for the exception.
            :param *reason_args: Zero or more arguments to be substituted into
                                 the format string for presentation as the
                                 reason for the exception.
        """

        super( Exception_WithReason, self ).__init__( )
        self._reason_format  = reason_format
        self._reason_args    = reason_args


    def __repr__( self ):
        """
            Returns a string which can be used by :py:func:`eval
            <CPython3:eval>` to create an instance of the class.
        """

        args_fmt = \
        ", ".join( map(
            repr, [ self._reason_format ] + list( self._reason_args )
        ) )
        return "Exception_WithReason( {0} )".format( args_fmt )


    def __str__( self ):
        """
            Returns an untranslated string expressing the reason for the
            exception.
        """

        return self._reason_format.format( *self._reason_args )


    def translated( self, translator ):
        """
            Returns a translated string expressing the reason for the
            exception.
        """

        return translator( self._reason_format ).format( *self._reason_args )


    @property
    def reason_format( self ):
        """
            Format string, containing zero or more :py:func:`format
            <CPython3:format>`-style substitution tokens, for presentation as 
            the reason for the exception. The substitions come from
            :py:attr:`reason_args`.
        """

        return self._reason_format


    @property
    def reason_args( self ):
        """
            Arguments to be substituted into the format string for 
            presentation as the reason for the exception. The arguments are
            substituted into :py:attr:`reason_format`.
        """

        return self._reason_args

Exception_BASE.register( Exception_WithReason )


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

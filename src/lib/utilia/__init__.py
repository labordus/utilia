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
    from ConfigParser import (
        SafeConfigParser        as __ConfigParser,
    )
else:
    from configparser import (
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


# Exceptions


# Note: If something goes wrong here, then just let the exception propagate.
if 2 == python_version.major:
    from __builtin__ import (
        BaseException           as __builtins_BaseException,
        StandardError           as __builtins_BaseError,
    )
else:
    from builtins import (
        BaseException           as __builtins_BaseException,
        Exception               as __builtins_BaseError,
    )


class Exception_BASE( __builtins_BaseException ):
    """
        Base class for all :py:mod:`utilia` exceptions.
        
        Inherits from :py:exc:`BaseException <CPython3:BaseException>`.

        Use this for your exception handler signature if you wish to catch any
        exception raised from within :py:mod:`utilia`.
    """


    def __init__( self, *posargs ):
        """
            Invokes superclass initializers.
        """

        super( Exception_BASE, self ).__init__( *posargs )


class Error_BASE( Exception_BASE, __builtins_BaseError ):
    """
        Base class for all :py:mod:`utilia` exceptions which are regarded as
        errors.
        
        Inherits from :py:class:`Exception_BASE` and
        :py:exc:`StandardError <CPython2:exceptions.StandardError>`. 

        Use this for your exception handler signature if you wish to catch any
        error condition raised from within :py:mod:`utilia`.
    """


    def __init__( self, *posargs ):
        """
            Invokes superclass initializers.
        """

        super( Error_BASE, self ).__init__( *posargs )


class Error_WithRC( Error_BASE ):
    """
        Base class for all :py:mod:`utilia` exceptions which are regarded as
        errors and which carry a return code that could be supplied to a
        :py:exc:`SystemExit <CPython3:SystemExit>` exception.

        Inherits from :py:class:`Error_BASE`.

        Use this for your exception handler signature if you wish to catch any
        error condition, which has an exit code, raised from within
        :py:mod:`utilia`.
    """


    #: Return code to use as the exit status if the error is considered fatal.
    rc              = 0


    def __init__( self, *posargs ):
        """
            Invokes superclass initializers.
            Sets the return code to carry with the exception.
        """

        super( Error_WithRC, self ).__init__( *posargs )
        self.rc = 0


    def __str__( self ):
        """
            Provides a human-readable representation of the error, 
            including the return code it is carrying.
        """

        s = super( Error_WithRC, self ).__str__( )
        s += " <Return Code: {0}>".format( self.rc )
        return s


class Error_WithReason( Error_BASE ):
    """
        Base class for all :py:mod:`utilia` exceptions which are regarded as
        errors and which carry a translatable error reason format string and a
        tuple of arguments for substitution into the format string.

        Inherits from :py:class:`Error_BASE`.

        Use this for your exception handler signature if you wish to catch any
        error condition, which has a translatable reason string, raised from
        within :py:mod:`utilia`.
    """


    #: Terse format string explaining why the path was undetermined.
    #: The format string expects arguments to be supplied from
    #: :py:attr:`reason_args`.
    reason_format       = None
    #: Tuple of arguments to be substituted into :py:attr:`reason_format`.
    reason_args         = [ ]


    def __init__( self, reason_format, *reason_args ):
        """
            Invokes superclass initializers.
            Sets the reason format string to carry with the exception.

            :param reason_format: String containing zero or more 
                                  ``format``-style substitution tokens.
            :param *reason_args: Zero or more arguments to be substituted into
                                 the reason format string.
        """

        super( Error_WithReason, self ).__init__(
            reason_format, *reason_args
        )
        self.reason_format  = reason_format
        self.reason_args    = reason_args


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

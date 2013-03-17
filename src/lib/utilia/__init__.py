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

        * :py:mod:`.exceptions`

        * :py:mod:`file systems <.filesystem>`

        * :py:mod:`functional programming <.functional>`

        * :py:mod:`operating system interfaces <.os>`
        
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
    join                    as _join_path,
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
if 3 == python_version.major:
    if 2 <= python_version.minor:
        from configparser import ( # pylint: disable=F0401
            ConfigParser            as _ConfigParser,
        )
    else:
        from configparser import ( # pylint: disable=F0401
            SafeConfigParser        as _ConfigParser,
        )
else:
    from ConfigParser import ( # pylint: disable=F0401
        SafeConfigParser        as _ConfigParser,
    )

_path_to_config = _join_path( __path__[ 0 ], "version.cfg" )
_vinfo_CFG = _ConfigParser( )
if _path_to_config not in _vinfo_CFG.read( _path_to_config ):
    raise IOError(
        "Configuration file '{0}' expected but not found.".format(
            _path_to_config
        )
    )

_vinfo_release_type     = _vinfo_CFG.get( "control", "release_type" )
assert _vinfo_release_type in [ "bugfix", "candidate", "development" ]
_vinfo_numbers_DICT     = dict( _vinfo_CFG.items( "numbers" ) )
if   "bugfix" == _vinfo_release_type: # Stable Bugfix Release
    __version__ = \
    "{major}.{minor}.{bugfix}".format( **_vinfo_numbers_DICT )
elif "candidate" == _vinfo_release_type: # Release Candidate
    __version__ = \
    "{major}.{minor}.0rc{update}".format( **_vinfo_numbers_DICT )
elif "development" == _vinfo_release_type: # Development Release
    with open( _join_path( __path__[ 0 ], "dev-timestamp.dat" ) ) \
    as _ts_file:
        _vinfo_numbers_DICT[ "update" ] = _ts_file.read( 12 )
    __version__ = \
    "{major}.{minor}.0dev{update}".format( **_vinfo_numbers_DICT )

del _ConfigParser, _path_to_config
del _vinfo_CFG, _vinfo_release_type, _vinfo_numbers_DICT


# Cleanup the module namespace.
del _join_path, collections


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


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

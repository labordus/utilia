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
    Python *setuptools* script for configuring, building, testing, 
    installing, and distributing the software.

    If the :py:mod:`setuptools` package from the 'distribute' distribution is 
    not present, then that package is retrieved from the Internet 
    (if possible).

    The :py:mod:`nose` package is a requisite to provide the ``nosetests``
    subcommand for this script.

    Please see the accompanying :file:`setup.cfg` file for default options to
    this script.
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


# Ensure correct version of 'setuptools'.
import distribute_setup
distribute_setup.use_setuptools( )
from setuptools import (
    setup,
    find_packages,
)


# Load some useful modules and functions.
import sys
import collections
from os.path import (
    dirname,
    join                    as _join_path,
    exists                  as _path_exists,
)
# Record path to working directory of the script.
__pwd           = dirname( sys.argv[ 0 ] )
# Calculate path to the software library.
_path_to_lib   = _join_path( __pwd, "src", "lib", "utilia" )


# Get Python version.
_Version = collections.namedtuple( "_Version", "major minor" )
# Note: Access 'version_info' fields by index rather than name for Python 2.6 
#       compatibility.
_python_version = _Version( sys.version_info[ 0 ], sys.version_info[ 1 ] )
assert 2 <= _python_version.major


# Read the master package's version info from config file.
# If the release type is "development", then write out a new timestamp.
# Note: If something goes wrong here, then just let the exception propagate.
if 3 == _python_version.major:
    if 2 <= _python_version.minor:
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
from datetime import (
    datetime                as _DateTime,
)

_path_to_timestamp  = _join_path( _path_to_lib, "dev-timestamp.dat" )
_path_to_config     = _join_path( _path_to_lib, "version.cfg" )
_vinfo_CFG = _ConfigParser( )
if _path_to_config not in _vinfo_CFG.read( _path_to_config ):
    raise IOError(
        "Configuration file '{0}' expected but not found.".format(
            _path_to_config
        )
    )

_vinfo_release_type    = _vinfo_CFG.get( "control", "release_type" )
assert _vinfo_release_type in [ "bugfix", "candidate", "development" ]
_vinfo_numbers_DICT    = dict( _vinfo_CFG.items( "numbers" ) )
if   "bugfix" == _vinfo_release_type: # Stable Bugfix Release
    _version = "{major}.{minor}.{bugfix}".format( **_vinfo_numbers_DICT )
elif "candidate" == _vinfo_release_type: # Release Candidate
    _version = "{major}.{minor}.0rc{update}".format( **_vinfo_numbers_DICT )
elif "development" == _vinfo_release_type: # Development Release
    if      _vinfo_CFG.getboolean( "control", "frozen_timestamp" ) \
        and _path_exists( _path_to_timestamp ):
        _timestamp_STR = open( _path_to_timestamp ).read( 12 )
    else:
        _timestamp_STR = _DateTime.utcnow( ).strftime( "%Y%m%d%H%M" )
        print( _timestamp_STR, file = open( _path_to_timestamp, "w" ) )
    _vinfo_numbers_DICT[ "update" ] = _timestamp_STR
    _version = "{major}.{minor}.0dev{update}".format( **_vinfo_numbers_DICT )


# Fill out the metadata for the distribution.
setup_data = { }

setup_data[ "name" ]                = "utilia"
setup_data[ "version" ]             = _version
setup_data[ "description" ]         = \
    "An assorted collection of modules and scripts."
setup_data[ "long_description" ]    = \
    """
        The 'utilia' software is a collection of various useful Python modules
        and scripts. A sample of some of the functionality provided is:

            * Calculation of standard paths for configuration information, 
              data stores, and scratch spaces for a particular operating
              system.

            * Et cetera....
    """
setup_data[ "license" ]             = \
    "Apache 2.0 (software), CC BY 3.0 (documentation)"
setup_data[ "author" ]              = "Eric A. McDonald"
setup_data[ "author_email" ]        = "utilia@googlegroups.com"
setup_data[ "url" ]                 = \
    "https://utilia.readthedocs.org/en/latest/index.html"
# TODO: download_url

setup_data[ "classifiers" ]         = \
    [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Natural Language :: English",
        # TODO: Add more natural languages here, as appropriate.
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ]

# TODO: namespace_packages
setup_data[ "packages" ]            = find_packages( dirname( _path_to_lib ) )
setup_data[ "package_dir" ]         = { "": dirname( _path_to_lib ) }
# TODO: py_modules
# TODO: ext_modules
# TODO: scripts
# TODO: entry_points

# TODO: options
# TODO: keywords

# TODO: platforms
# TODO: data_files
# TODO: include_package_data
# TODO: exclude_package_data
setup_data[ "package_data" ]        = \
    {
        "utilia": [ "*.cfg", "*.dat", ],
    }
# TODO: zip_safe

# TODO: requires
# TODO: provides
# TODO: obsoletes
# TODO: dependency_links
setup_data[ "setup_requires" ]      = [ ]
# Only expose lint and translation tools in development mode.
if "development" == _vinfo_release_type:
    if 2 == _python_version.major:
        # Note: Needed for the 'flakes' command.
        setup_data[ "setup_requires" ].append( "setuptools_pyflakes >= 1.1.0" )
        # Note: Needed for the following commands:
        #           extract_messages, init_catalog, update_catalog,
        #           compile_catalog
        setup_data[ "setup_requires" ].append( "Babel >= 0.9.6" )
        # NOTE: Hard-wired hack for Babel.
        #       (Cannot get correct behavior from 'setup.cfg'.)
        #       (See 'setup.cfg' for details.)
        setup_data[ "message_extractors" ] = \
        {
            _path_to_lib: """[python: **.py]"""
        }
    # Note: Needed for the 'lint' command.
    setup_data[ "setup_requires" ].append( "setuptools-lint >= 0.1" )
# Note: Needed for the 'nosetests' command.
setup_data[ "setup_requires" ].append( "nose >= 1.2.1" )
# Note: Needed for the 'build_sphinx' command.
setup_data[ "setup_requires" ].append( "Sphinx >= 1.1.3" )
# TODO: extras_require
# TODO: tests_require
# TODO: install_requires

setup_data[ "test_suite" ]          = "nose.collector"
# TODO: test_loader
# TODO: eager_resources

setup( **setup_data )


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

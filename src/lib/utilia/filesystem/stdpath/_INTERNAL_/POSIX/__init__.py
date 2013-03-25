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
    Implementation of the standard path calculation logic for POSIX OS
    platforms.
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


import site
import functools
import re
from os import (
    environ                 as _envvars,
)
# TODO: Replace with POSIX-specific functions.
from os.path import (
    isabs                   as _is_absolute_path,
    join                    as _join_path,
    expanduser              as _expand_user_path,
)


from utilia import (
    _TD_,
)
from .. import (
    _OptionValidator,
    UndeterminedPathError,
    StandardPathContext_BASE,
    StandardPath_BASE,
)


class StandardPathContext( StandardPathContext_BASE ):
    """
        Auxiliary class, which provides a context for calculating standard
        paths for POSIX OS platforms.

        Inherits from :py:class:`StandardPathContext_BASE`.

        Provides these options:

        .. csv-table::
           :header: "Name", "Description"
           :widths: 20, 80

    """


    _option_validators = StandardPathContext_BASE._option_validators
    _option_validators[ "whitespace_to_underscore" ]    = \
    _OptionValidator(
        None, True,
        """
            (*Boolean*).
            Convert white spaces to underscores in paths calculated from 
            the name, provider, and version of a software package.
        """
    )
    _option_validators[ "XDG_standard" ]                = \
    _OptionValidator(
        None, True,
        """
            (*Boolean*).
            Follow the XDG Base Directory Specification, where relevant,
            when calculating paths.
        """
    )


    def __init__( self, **options ):
        """ """

        StandardPathContext_BASE.__init__( self, **options )

    __init__.__doc__ = StandardPathContext_BASE.__init__.__doc__


    def _calculate_path( self ):
        """ """

        error_on_none               = \
        self.get_with_default( "error_on_none" )
        whitespace_to_underscore    = \
        self.get_with_default( "whitespace_to_underscore" )
        software_name               = \
        self.get_with_default( "software_name" )
        software_provider_name      = \
        self.get_with_default( "software_provider_name" )
        software_version            = \
        self.get_with_default( "software_version" )
        
        if not software_name:
            if error_on_none:
                raise UndeterminedPathError(
                    _TD_( "Missing software name for calculated path." )
                )
            else: return None

        if whitespace_to_underscore:
            resub_whitespace_to_underscore  = \
            functools.partial( re.sub, r"\s+", "_" )
            software_name                   = \
            resub_whitespace_to_underscore( software_name )
            if software_provider_name:
                software_provider_name      = \
                resub_whitespace_to_underscore( software_provider_name )
            if software_version:
                software_version            = \
                resub_whitespace_to_underscore( software_version )

        return _join_path( *filter(
            None,
            [ software_provider_name, software_name, software_version ]
        ) )

    _calculate_path.__doc__ = \
    StandardPathContext_BASE._calculate_path.__doc__


#: Current standard path context.
_context = StandardPathContext( )

StandardPathContext.__doc__ += \
"\n".join(
    map(
        lambda k, v: \
        (" " * 10) + """ "{option_name}", "{option_help}" """.format(
            option_name = k, option_help = v
        ),
        (k for k, v in _context.iter_option_validators( )),
        (v.help for k, v in _context.iter_option_validators( ))
    )
)


def get_context( ):
    """
        Returns the current standard path context.
    """

    return _context


def set_context( new_context ):
    """
        Sets a new standard path context.
        Returns the old standard path context.
    """

    global _context     # pylint: disable=W0603

    old_context, _context = _context, new_context
    return old_context


class StandardPath( StandardPath_BASE ):
    """
        Calculates standard paths for POSIX OS platforms.
    """


    def __init__( self, context = get_context( ) ):
        """ """

        StandardPath_BASE.__init__( self, context )

    __init__.__doc__ = StandardPath_BASE.__init__.__doc__


    def whereis_temp( self, context = None ):
        """ """

        context = self._find_context( context )

        base_path, specific_path = \
        self._choose_common_path_parts( context )

        if base_path and context.get_with_default( "temp_on_base_path" ):
            base_path = _join_path( base_path, "tmp" )
        else: base_path = None

        if None is base_path:
            if context.get_with_default( "XDG_standard" ):
                base_path = _envvars.get( "XDG_CACHE_HOME" )
                if None is base_path:
                    base_path = \
                    _join_path( _whereis_user_home( ), ".cache" )
        if None is base_path: base_path = "/tmp"

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_temp.__doc__ = StandardPath_BASE.whereis_temp.__doc__


    # TODO: whereis_runtime_support


    def whereis_common_config( self, context = None ):
        """ """

        context = self._find_context( context )

        pythonic = context.get_with_default( "Pythonic" )
        if pythonic and context.get_with_default( "strictly_Pythonic" ):
            return _whereis_common_Python_package( context )

        base_path, specific_path = \
        self._choose_common_path_parts( context )

        if (None is base_path) and pythonic:
            base_path = context.get_with_default( "Python_prefix_path" )
        if None is base_path: base_path = "/usr/local"

        # TODO? Handle '/opt' as '/etc/opt'.
        # Note: '/' and '/usr' share '/etc' for config.
        if "/usr" == base_path: base_path = "/"
        base_path = _join_path( base_path, "etc" )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_common_config.__doc__ = \
    StandardPath_BASE.whereis_common_config.__doc__


    def whereis_common_resources( self, context = None ):
        """ """

        context = self._find_context( context )

        pythonic = context.get_with_default( "Pythonic" )
        if pythonic and context.get_with_default( "strictly_Pythonic" ):
            return _whereis_common_Python_package( context )

        base_path, specific_path = \
        self._choose_common_path_parts( context )

        if (None is base_path) and pythonic:
            base_path = context.get_with_default( "Python_prefix_path" )
        if None is base_path: base_path = "/usr/local"

        # Note: '/' cannot rely on the presence of '/usr/share'.
        #       '/etc' is thus assumed to be the location for resources.
        # TODO: Research handling of '/' more.
        if "/" == base_path:    base_path = "/etc"
        else:                   base_path = _join_path( base_path, "share" )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_common_resources.__doc__ = \
    StandardPath_BASE.whereis_common_resources.__doc__


    def whereis_common_programs( self, context = None ):
        """ """

        context = self._find_context( context )

        base_path = self._choose_common_path_parts( context )[ 0 ]

        if (None is base_path) and context.get_with_default( "Pythonic" ):
            base_path = context.get_with_default( "Python_prefix_path" )
        if None is base_path: base_path = "/usr/local"

        return _join_path( base_path, "bin" )

    whereis_common_programs.__doc__ = \
    StandardPath_BASE.whereis_common_programs.__doc__
    

    def whereis_user_config( self, context = None ):
        """ """

        context = self._find_context( context )

        pythonic = context.get_with_default( "Pythonic" )
        if pythonic and context.get_with_default( "strictly_Pythonic" ):
            return _whereis_user_Python_package( context )

        base_path, specific_path = \
        self._choose_user_path_parts( context )

        if base_path: base_path = _join_path( base_path, "etc" )

        if (None is base_path) and pythonic:
            base_path = _join_path( site.USER_BASE, "etc" )
        if None is base_path:
            if context.get_with_default( "XDG_standard" ):
                base_path = _envvars.get( "XDG_CONFIG_HOME" )
                if None is base_path:
                    base_path = \
                    _join_path( _whereis_user_home( ), ".config" )
        if None is base_path:
            if specific_path:
                return _join_path(
                    _whereis_user_home( ), "." + specific_path, "config"
                )
            else: return _whereis_user_home( )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_user_config.__doc__ = \
    StandardPath_BASE.whereis_user_config.__doc__
    

    def whereis_user_resources( self, context = None ):
        """ """

        context = self._find_context( context )

        pythonic = context.get_with_default( "Pythonic" )
        if pythonic and context.get_with_default( "strictly_Pythonic" ):
            return _whereis_user_Python_package( context )

        base_path, specific_path = \
        self._choose_user_path_parts( context )

        if base_path: base_path = _join_path( base_path, "share" )

        if (None is base_path) and pythonic:
            base_path = _join_path( site.USER_BASE, "share" )
        if None is base_path:
            if context.get_with_default( "XDG_standard" ):
                base_path = _envvars.get( "XDG_DATA_HOME" )
                if None is base_path:
                    base_path = \
                    _join_path( _whereis_user_home( ), ".local", "share" )
        if None is base_path:
            if specific_path:
                return _join_path(
                    _whereis_user_home( ), "." + specific_path, "resources"
                )
            else: return _whereis_user_home( )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_user_resources.__doc__ = \
    StandardPath_BASE.whereis_user_resources.__doc__

    def whereis_saved_data( self, context = None ):
        """ """

        context = self._find_context( context )

        base_path, specific_path = \
        self._choose_user_path_parts( context )

        # TODO: Consider on a per-desktop environment basis.
        #       Use 'Documents' directory as appropriate.
        if not base_path:
            if specific_path:
                return _join_path(
                    _whereis_user_home( ), "." + specific_path, "saved_data"
                )
            else: return _whereis_user_home( )

        if specific_path:
            specific_path = _join_path( specific_path, "saved_data" )
        else:
            base_path = _join_path( base_path, "saved_data" )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_saved_data.__doc__ = \
    StandardPath_BASE.whereis_saved_data.__doc__


    def _is_absolute_path( self, the_path ):
        """ """

        # TODO: Use POSIX-specific path tester rather than current OS one.
        return _is_absolute_path( the_path )

    _is_absolute_path.__doc__ = \
    StandardPath_BASE._is_absolute_path.__doc__


def _whereis_common_Python_package( context ):
    """
        Returns the path to a particular Python package relative to the primary
        site packages directory for a given Python installation and version.
    """

    python_package_name = context.get_with_default( "Python_package_name" )

    if None is python_package_name:
        context.raise_UndeterminedPathError(
            _TD_( "Python package" ), specify_software = True
        )

    # NOTE: The Ubuntu Linux distro seems to violate convention by using
    #       'dist-packages' instead of 'site-packages'.
    # TODO: Account for Ubuntu Linux in Linux-specific standard paths.
    return _join_path(
        context.get_with_default( "Python_prefix_path" ),
        "lib",
        "python" + context.get_with_default( "Python_version" ),
        "site-packages",
        python_package_name
    )


def _whereis_user_Python_package( context ):
    """
        Returns the path to a particular Python package relative to the user's
        site packages directory specified by :pep:`370` and provided by the
        :py:mod:`site <CPython3:site>` module.
    """

    python_package_name = context.get_with_default( "Python_package_name" )

    if None is python_package_name:
        context.raise_UndeterminedPathError(
            _TD_( "Python package" ), specify_software = True
        )

    return _join_path( site.USER_SITE, python_package_name )


def _whereis_user_home( ):
    """
        Returns the path to the current user's home directory, if it can be
        determined. Returns ``None``, otherwise.
    """

    user_id         = _envvars.get( "USER" )
    user_home_path  = _expand_user_path( "~" )

    if None is user_home_path:
        if None is user_id:
            raise UndeterminedPathError(
                _TD_(
                    "Undetermined path to home directory "
                    "because current user is unknown."
                )
            )
        else:
            raise UndeterminedPathError(
                _TD_(
                    "Undetermined path to home directory of user {0}."
                ),
                user_id
            )

    return user_home_path


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

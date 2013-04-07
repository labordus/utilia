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
    Implementation of the standard path calculation logic for MacOS X.
"""
# TODO: Consider any nuances of Fink, Homebrew, MacPorts, etc....


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


import re   as _re
# TODO: Replace with POSIX-specific functions.
from os.path import (
    join                    as _join_path,
    dirname                 as _dirname_of_path,
)


from .. import (
    _OptionValidator,
)
from . import (
    StandardPathContext     as POSIXStandardPathContext,
    StandardPath            as POSIXStandardPath,
)


class StandardPathContext( POSIXStandardPathContext ):
    """
        Auxiliary class, which provides a context for calculating standard
        paths for MacOS X platforms.

        Inherits from :py:class:`POSIX.StandardPathContext
        <POSIXStandardPathContext>`.

        Provides these options:

        .. csv-table::
           :header: "Name", "Description"
           :widths: 20, 80

    """


    _option_validators = POSIXStandardPathContext._option_validators
    _option_validators[ "XDG_standard" ]        = \
    _OptionValidator(
        _option_validators[ "XDG_standard" ].func, False,
        _option_validators[ "XDG_standard" ].help
    )


    def __init__( self, **options ):
        """ """

        POSIXStandardPathContext.__init__( self, **options )

    __init__.__doc__ = POSIXStandardPathContext.__init__.__doc__


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


class StandardPath( POSIXStandardPath ):
    """
        Calculates standard paths for MacOS X platforms.
    """


    def __init__( self, context = get_context( ) ):
        """ """

        POSIXStandardPath.__init__( self, context )

    __init__.__doc__ = POSIXStandardPath.__init__.__doc__


    def whereis_common_config( self, context = None ):
        """ """

        context = self._find_context( context )

        pythonic = context.get_with_default( "Pythonic" )
        if pythonic:
            return POSIXStandardPath.whereis_common_config( self, context )

        base_path, specific_path = \
        self._choose_common_path_parts( context )

        if base_path:
            base_path_trunc = \
            StandardPath._truncate_framework_path( base_path )
            if base_path == base_path_trunc:
                return POSIXStandardPath.whereis_common_config(
                    self, context
                )
            base_path = base_path_trunc
            if base_path.startswith( "/System" ): base_path = "/Library"
        else: base_path = "/Library"
        base_path = _join_path( base_path, "Preferences" )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_common_config.__doc__ = \
    POSIXStandardPath.whereis_common_config.__doc__


    def whereis_common_resources( self, context = None ):
        """ """

        context = self._find_context( context )

        pythonic = context.get_with_default( "Pythonic" )
        if pythonic:
            return POSIXStandardPath.whereis_common_resources( self, context )

        base_path, specific_path = \
        self._choose_common_path_parts( context )

        if base_path:
            base_path_trunc = \
            StandardPath._truncate_framework_path( base_path )
            if base_path == base_path_trunc:
                return POSIXStandardPath.whereis_common_resources(
                    self, context
                )
            base_path = base_path_trunc
            if base_path.startswith( "/System" ): base_path = "/Library"
        else: base_path = "/Library"
        base_path = _join_path( base_path, "Application Support" )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_common_resources.__doc__ = \
    POSIXStandardPath.whereis_common_resources.__doc__


    def whereis_user_config( self, context = None ):
        """ """

        context = self._find_context( context )

        fallback_to_POSIX = \
            context.get_with_default( "Pythonic" ) \
        or  context.get_with_default( "XDG_standard" )
        if fallback_to_POSIX:
            return POSIXStandardPath.whereis_user_config( self, context )

        base_path, specific_path = \
        self._choose_user_path_parts( context )

        if base_path:
            base_path_trunc = \
            StandardPath._truncate_framework_path( base_path )
            if base_path == base_path_trunc:
                return POSIXStandardPath.whereis_user_config(
                    self, context
                )
            base_path = base_path_trunc
        else: base_path = POSIXStandardPath._whereis_user_home( )
        base_path = _join_path( base_path, "Preferences" )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_user_config.__doc__ = \
    POSIXStandardPath.whereis_user_config.__doc__


    def whereis_user_resources( self, context = None ):
        """ """

        context = self._find_context( context )

        fallback_to_POSIX = \
            context.get_with_default( "Pythonic" ) \
        or  context.get_with_default( "XDG_standard" )
        if fallback_to_POSIX:
            return POSIXStandardPath.whereis_user_resources( self, context )

        base_path, specific_path = \
        self._choose_user_path_parts( context )

        if base_path:
            base_path_trunc = \
            StandardPath._truncate_framework_path( base_path )
            if base_path == base_path_trunc:
                return POSIXStandardPath.whereis_user_resources(
                    self, context
                )
            base_path = base_path_trunc
        else: base_path = POSIXStandardPath._whereis_user_home( )
        base_path = _join_path( base_path, "Application Support" )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_user_resources.__doc__ = \
    POSIXStandardPath.whereis_user_resources.__doc__


    def whereis_saved_data( self, context = None ):
        """ """

        context = self._find_context( context )

        base_path, specific_path = \
        self._choose_user_path_parts( context )

        if not base_path: base_path = POSIXStandardPath._whereis_user_home( )
        base_path = _join_path( base_path, "Documents" )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_saved_data.__doc__ = \
    POSIXStandardPath.whereis_saved_data.__doc__


    @staticmethod
    def _truncate_framework_path( path ):
        """
            If the Python path is for a MacOS X framework installation,
            then truncates the path components associated with the framework
            and returns the remainder of the path. Else, returns the path
            without any alteration.
        """

        match = _re.findall( r".*/Python\.framework/Versions/.*", path )
        if match:
            return reduce(
                lambda x, f: f( x ), [ _dirname_of_path ] * 4, path
            )

        return path


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

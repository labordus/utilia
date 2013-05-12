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
    Implementation of the standard path calculation logic for Windows.
"""
# TODO? Consider Cygwin, Mingw, and others....


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


import sys
import site
from os import (
    environ                 as _envvars,
)
# TODO: Replace with Windows-specific functions.
from os.path import (
    join                    as _join_path,
)


from utilia import (
    _TD_,
)
from . import (
    _OptionValidator,
    UndeterminedPathError,
    StandardPathContext_BASE,
    StandardPath_BASE,
)


class StandardPathContext( StandardPathContext_BASE ):
    """
        Auxiliary class, which provides a context for calculating standard
        paths for Windows platforms.

        Inherits from :py:class:`StandardPathContext_BASE`.

        Provides these options:

        .. csv-table::
           :header: "Name", "Description"
           :widths: 20, 80

    """


    _option_validators = StandardPathContext_BASE._option_validators


    def __init__( self, **options ):
        """ """

        StandardPathContext_BASE.__init__( self, **options )

    __init__.__doc__ = StandardPathContext_BASE.__init__.__doc__


    def _calculate_path( self ):
        """ """

        error_on_none               = \
        self.get_with_default( "error_on_none" )
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
        Calculates standard paths for Windows platforms.
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
            base_path = _join_path( base_path, "Temp" )
        else: base_path = None

        if None is base_path:
            base_path = _envvars.get( "TMP", _envvars.get( "TEMP" ) )
            if None is base_path:
                context.raise_UndeterminedPathError(
                    _TD_( "temporary storage" )
                )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_temp.__doc__ = StandardPath_BASE.whereis_temp.__doc__


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
        if None is base_path:
            # TEMP HACK: Satisfy '__str__'. Not an acutal Windows convention.
            # TODO: Need to raise exception if software name is not supplied. 
            #       And, need to think about how to handle '__str__' 
            #       representation of objects in this case.
            base_path = \
            _join_path(
                StandardPath._whereis_common_installation( context ),
                "Common Files"
            )
        else: base_path = _join_path( base_path, "Config" )

        if specific_path: return _join_path( base_path, specific_path )
        return base_path

    whereis_common_config.__doc__ = \
    StandardPath_BASE.whereis_common_config.__doc__


    @staticmethod
    def _whereis_common_installation( context ):
        """
            Returns path to the appropriate Windows "program files" folder in
            the context of the bit width for the Windows OS.
        """

        import platform

        os_bit_width    = 64 if "64bit" in platform.architecture( ) else 32
        app_bit_width   = 64 if sys.maxsize > 2 ** 32 else 32
        # TODO: Get desired bit widths from context, 
        #       setting context defaults as computed above.

        evname = None

        if 64 == os_bit_width:
            if 64 == app_bit_width: evname = "ProgramFiles"
            else:                   evname = "ProgramFiles(x86)"
        else:                       evname = "ProgramFiles"
        
        the_path = _envvars.get( evname )
        if None is the_path:
            context.raise_UndeterminedPathError(
                _TD_( "Windows common installation directory" )
            )

        return the_path


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

    return _join_path(
        context.get_with_default( "Python_prefix_path" ),
        "Lib",
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


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

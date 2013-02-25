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


# TODO: Support XDG environment variables.


# TODO: Replace with POSIX-specific functions.
from os.path import (
    isabs                   as is_absolute_path,
    join                    as join_path,
)


from . import (
    _OptionValidator,
    StandardPathContext_BASE,
    StandardPath_BASE,
)


class StandardPathContext( StandardPathContext_BASE ):
    """
        Auxiliary class, which provides a context for calculating standard
        paths on POSIX OS platforms.

        Inherits from :py:class:`StandardPathContext_BASE`.

        Provides these options:

        .. csv-table::
           :header: "Name", "Description"
           :widths: 20, 80

    """


    _option_validators = StandardPathContext_BASE._option_validators
    _option_validators.update( {
        "whitespace_to_underscore": \
        _OptionValidator(
            None, True,
            """
                (*Boolean*).
                Convert white spaces to underscores in paths calculated from 
                the name, provider, and version of a software package.
            """
        ),
        "XDG_Standard": \
        _OptionValidator(
            None, True,
            """
                (*Boolean*).
                Follow the XDG Base Directory Specification, where relevant,
                when calculating paths.
            """
        ),
    } )


    def __init__( self, **options ):
        """ """

        StandardPathContext_BASE.__init__( self, **options )

    __init__.__doc__ = StandardPathContext_BASE.__init__.__doc__


    def _calculate_path( self ):
        """ """

        # TODO: Implement.
        pass

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

    global _context

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

        base_path, specific_path = self._choose_path_parts( context )
        if None is base_path: base_path = "/tmp"

        if specific_path: return self._join_path( base_path, specific_path )
        return base_path

    whereis_temp.__doc__ = StandardPath_BASE.whereis_temp.__doc__


    def whereis_common_config( self, context = None ):
        """ """

        # TODO: Implement.
        pass

    whereis_common_config.__doc__ = \
    StandardPath_BASE.whereis_common_config.__doc__


    def whereis_common_resources( self, context = None ):
        """ """

        # TODO: Implement.
        pass

    whereis_common_resources.__doc__ = \
    StandardPath_BASE.whereis_common_resources.__doc__
    

    def whereis_user_config( self, context = None ):
        """ """

        # TODO: Implement.
        pass

    whereis_user_config.__doc__ = \
    StandardPath_BASE.whereis_user_config.__doc__
    

    def whereis_user_resources( self, context = None ):
        """ """

        # TODO: Implement.
        pass

    whereis_user_resources.__doc__ = \
    StandardPath_BASE.whereis_user_resources.__doc__


    def whereis_saved_data( self, context = None ):
        """ """

        # TODO: Implement.
        pass

    whereis_saved_data.__doc__ = \
    StandardPath_BASE.whereis_saved_data.__doc__


    def _is_absolute_path( self, the_path ):
        """ """

        # TODO: Use POSIX-specific path tester rather than current OS one.
        return is_absolute_path( the_path )

    _is_absolute_path.__doc__ = \
    StandardPath_BASE._is_absolute_path.__doc__
        

    def _join_path( self, *posargs ):
        """ """

        # TODO: Use POSIX-specific path joiner rather than current OS one.
        return join_path( *posargs )

    _join_path.__doc__ = \
    StandardPath_BASE._join_path.__doc__


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

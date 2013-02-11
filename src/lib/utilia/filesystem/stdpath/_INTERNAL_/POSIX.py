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
    <TODO: Insert module documentation here.>
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


# TODO: Support XDG environment variables.


from . import (
    _OptionValidator,
    StandardPathContext_BASE,
    StandardPath_BASE,
)


class StandardPathContext( StandardPathContext_BASE ):
    """
        <TODO: Insert class documentation here.> 
    """


    # TODO: Fill out help on option validators.
    _option_validators = StandardPathContext_BASE._option_validators
    _option_validators.update( {
        "whitespace_to_underscore": _OptionValidator( None, """ """ ),
        "XDG_Standard":             _OptionValidator( None, """ """ ),
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


class StandardPath( StandardPath_BASE ):
    """
        <TODO: Insert class documentation here.>
    """


    def __init__( self, context = None ):
        """ """

        StandardPath_BASE.__init__( self, context )

    __init__.__doc__ = StandardPath_BASE.__init__.__doc__


    def whereis_temp( self, context = None ):
        """ """

        # TODO: Implement.
        pass

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


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

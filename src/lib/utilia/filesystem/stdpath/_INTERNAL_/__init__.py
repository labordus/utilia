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


from utilia.compat import (
    iter_dict_keys,
    iter_dict_items,
)
from utilia.compat.collections import (
    MutableMapping,
)


class StandardPathContext( MutableMapping ):
    """
        Auxiliary class, which provides a context for calculating standard
        paths.

        Inherits from :py:class:`collections.MutableMapping
        <CPython3:collections.MutableMapping>`.
    """


    #: Name of the particular software product for this context.
    _software_name      = None
    #: Name of the organization providing the particular software product for
    #: this context.
    _provider_name      = None
    #: Version of the particular software product for this context.
    _version            = None
    #: Specific path to the particular software product for this context.
    _specific_path      = None
    #: Options for modifying the behavior of path calculations.
    _options_DICT       = { }


    def __init__(
        self,
        software_name = None, provider_name = None, version = None,
        specific_path = None,
        **options
    ):
        """
            :param software_name: Name of the particular software product for
                                  which this context is being created.
            :type software_name: :py:class:`string <CPython3:str>`
            :param provider_name: Name of the organization providing the
                                  particular software product for which this
                                  context is being created.
            :type provider_name: :py:class:`string <CPython3:str>`
            :param version: Version of the particular software product for
                            which this context is being created.
            :type version: :py:class:`string <CPython3:str>`
            :param specific_path: Specific path to the particular software
                                  product for which this context is being
                                  created.
            :type specific_path: :py:class:`string <CPython3:str>`
            :param **options: Zero or more keyword arguments to be used as
                              options for modifying the behavior of path
                              calculations.
        """

        for option_name, option_value in iter_dict_items( options ):
            self.__setitem__( option_name, option_value )

        self.software_name      = software_name
        self.provider_name      = provider_name
        self.version            = version
        self.specific_path      = specific_path


    def __iter__( self ):
        """
            Returns an iterator over the behavior options dictionary.
        """

        return iter_dict_keys( self._options_DICT )


    def __len__( self ):
        """
            Returns the number of entries in the behavior options dictionary.
        """

        return len( self._options_DICT )


    def __getitem__( self, key ):
        """
            Returns a value from the behavior options dictionary corresponding
            to the ``key`` argument.
        """

        return self._options_DICT[ key ]


    def __setitem__( self, key, value ):
        """
            Places the ``value`` argument into the behvaior options dictionary
            such that it corresponds to the ``key`` argument.
        """

        # TODO: Should be abstract here. Override on the basis of OS archtype
        #       or OS to filter for suitable options.
        # TEMP
        self._options_DICT[ key ] = value


    def __delitem__( self, key ):
        """
            Deletes the entry in the behavior options dictionary corresponding
            to the ``key`` argument.
        """

        del self._options_DICT[ key ]


    def _software_name_GETTER( self ):
        
        return self._software_name


    def _software_name_SETTER( self, software_name ):
        
        # TODO? Update calculated path cache.
        self._software_name = software_name


    def _software_name_DELETER( self ):
        
        # TODO? Update calculated path cache.
        self._software_name = None


    software_name = \
    property(
        _software_name_GETTER, _software_name_SETTER, _software_name_DELETER,
        """
            Name of the particular software product for this context.
        """
    )


    def _provider_name_GETTER( self ):
        
        return self._provider_name


    def _provider_name_SETTER( self, provider_name ):
        
        # TODO? Update calculated path cache.
        self._provider_name = provider_name


    def _provider_name_DELETER( self ):
        
        # TODO? Update calculated path cache.
        self._provider_name = None


    provider_name = \
    property(
        _provider_name_GETTER, _provider_name_SETTER, _provider_name_DELETER,
        """
            Name of the organization providing the particular software product
            for this context.
        """
    )


    def _version_GETTER( self ):
        
        return self._version


    def _version_SETTER( self, version ):
        
        # TODO? Update calculated path cache.
        self._version = version


    def _version_DELETER( self ):
        
        # TODO? Update calculated path cache.
        self._version = None


    version = \
    property(
        _version_GETTER, _version_SETTER, _version_DELETER,
        """
            Version of the particular software product for this context.
        """
    )


    def _specific_path_GETTER( self ):
        
        # TODO? Return value from calculated path cache, 
        #       if specific path not set.
        return self._specific_path


    def _specific_path_SETTER( self, specific_path ):

        # TODO? Check that the path is well-formed for given OS archtype.
        self._specific_path = specific_path


    def _specific_path_DELETER( self ):
        
        self._specific_path = None


    specific_path = \
    property(
        _specific_path_GETTER, _specific_path_SETTER, _specific_path_DELETER,
        """
            Specific path to the particular software product for this context.
        """
    )


class StandardPath( object ):
    """
        Abstract base class for the standard path classes of the various
        flavors of operating system archtypes.

        Inherits from :py:class:`object <CPython3:object>`.
    """


    #: Object containing the context with which to calculate paths.
    _context = None


    def __init__( self, context = StandardPathContext( ) ):
        """
            :param context: An object containing the context with which to
                            calculate paths.
            :type context: :py:class:`StandardPathContext`
        """

        super( StandardPath, self ).__init__( )

        self._context = context


    # TODO: Implement.


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

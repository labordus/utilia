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
    Basis for OS-dependent implementations of the standard path calculation 
    logic.
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


import sys
from abc import (
    abstractmethod,
)

from utilia import (
    _TD_,
    python_version          as _python_version,
)
from utilia.compat import (
    iter_dict_keys,
    iter_dict_values,
    iter_dict_items,
    AbstractBase_BASE,
)
from utilia.compat.builtins import (
    LookupError             as _builtins_LookupError,
    KeyError                as _builtins_KeyError,
)
from utilia.compat.collections import ( # pylint: disable=E0611
    MutableMapping,
    namedtuple,
    OrderedDict,
)
import utilia.os.exit_codes as _exit_codes
from utilia.exceptions import (
    Exception_Exiting,
    InvalidKeyError,
    UnknownKeyError,
    InvalidValueError,
    InvokedAbstractMethodError,
)
from utilia.filesystem import (
    Error_BASE              as FilesystemError_BASE,
)


class UndeterminedPathError( Exception_Exiting, _builtins_LookupError ):
    """
        Exception class representing the error condition where a path
        cannot be calculated for the given operating system and context.

        Inherits from :py:class:`Exception_Exiting` and 
        :py:exc:`LookupError <CPython3:LookupError>`.
    """


    def __init__( self, reason_format, *reason_args ):
        """ """

        super( UndeterminedPathError, self ).__init__(
            reason_format, *reason_args
        )

        self._class_name    = self.__class__.__name__
        self._rc            = _exit_codes.INTERNAL_SOFTWARE_ERROR( )

    __init__.__doc__ += Exception_Exiting.__init__.__doc__
        

FilesystemError_BASE.register( UndeterminedPathError )


_OptionValidator = namedtuple( "_OptionValidator", "func default help" )


class StandardPathContext_BASE( MutableMapping ):
    """
        Base for auxiliary classes, which provide a context for calculating 
        standard paths.

        Inherits from :py:class:`collections.MutableMapping
        <CPython3:collections.MutableMapping>`.
    """


    _option_validators  = OrderedDict( )
    _option_validators[ "error_on_none" ]           = \
    _OptionValidator(
        None, True,
        """
            (*Boolean*).
            Raise a :py:class:`UndeterminedPathError` if a standard path
            cannot be calculated with the given context for the OS platform.
        """
    )
    _option_validators[ "specific_common_path" ]    = \
    _OptionValidator(
        None, None,
        """
            (*String*).
            Use this path as the part of a full common installation root path
            which is specific to a particular software package. If this path
            is set, then it overrides any path calculated from the software
            name, vendor, and version. If this path is an absolute path on the
            OS platform corresponding to its context, then it overrides any
            base path supplied within the context.
        """
    )
    _option_validators[ "specific_user_path" ]      = \
    _OptionValidator(
        None, None,
        """
            (*String*).
            Use this path as the part of a full user installation root path
            which is specific to a particular software package. If this path
            is set, then it overrides any path calculated from the software
            name, vendor, and version. If this path is an absolute path on the
            OS platform corresponding to its context, then it overrides any
            base path supplied within the context.
        """
    )
    _option_validators[ "calculate_path" ]          = \
    _OptionValidator(
        None, False,
        """
            (*Boolean*).
            Attempt to calculate the part of a full path which is specific
            to a particular software package by using the name, provider, 
            and version of the software package, as available. If a 
            specific path to this software package is not directly set, 
            then the calculated path will be used.
        """
    )
    _option_validators[ "temp_on_base_path" ]       = \
    _OptionValidator(
        None, False,
        """
            (*Boolean*).
            If a base path is supplied, then calculate path to temporary
            storage relative to it.
        """
    )
    _option_validators[ "software_name" ]           = \
    _OptionValidator(
        None, None,
        """
            (*String*).
            The name of a software package which can be used to calculate
            the part of a full path that is specific to the software package.
        """
    )
    _option_validators[ "software_provider_name" ]  = \
    _OptionValidator(
        None, None,
        """
            (*String*).
            The name of the provider (author, vendor, etc...) of a software
            package which can be used to calculate the part of a full path
            that is specific to the software package.
        """
    )
    _option_validators[ "software_version" ]        = \
    _OptionValidator(
        None, None,
        """
            (*String*).
            The version of a software package which can be used to calculate
            the part of a full path that is specific to the software package.
        """
    )
    _option_validators[ "common_base_path" ]        = \
    _OptionValidator(
        None, None,
        """
            (*String*).
            Use this path as the part of a full path which is an alternative
            common installation root path to the default one for the OS 
            platform corresponding to the context.
        """
    )
    _option_validators[ "user_base_path" ]          = \
    _OptionValidator(
        None, None,
        """
            (*String*).
            Use this path as the part of a full path which is an alternative
            user installation root path to the default one for the OS 
            platform corresponding to the context.
        """
    )
    _option_validators[ "Pythonic" ]                = \
    _OptionValidator(
        None, False,
        """
            (*Boolean*).
            Calculate standard paths which comply with :pep:`370` and various
            Pythonic packaging conventions, where applicable.
        """
    )
    _option_validators[ "strictly_Pythonic" ]       = \
    _OptionValidator(
        None, False,
        """
            (*Boolean*).
            Calculate standard paths under the assumptions that:

            * common configuration information will be stored in the same
              directory as a package;
            * common resources will be stored in the same directory as a
              package.
        """
    )
    _option_validators[ "Python_prefix_path" ]      = \
    _OptionValidator(
        None, sys.prefix,
        """
            (*String*)
            Use this path as the Python installation root path.
        """
    )
    _option_validators[ "Python_version" ]          = \
    _OptionValidator(
        None,
        ".".join(
            map( str, [ _python_version.major, _python_version.minor ] )
        ),
        """
            (*String*)
            Use this version number when calculating the path to the primary
            site packages directory for a Python installation.
        """
    )
    _option_validators[ "Python_package_name" ]     = \
    _OptionValidator(
        None, None,
        """
            (*String*)
            Use this name when calculating the path to a particular Python
            package relative to the primary site packages directory for a
            Python installation.
        """
    )
    _options            = { }


    def __init__( self, **options ):
        """
            Initializes the options dictionary from supplied keyword 
            arguments.

            :param **options: Zero or more keyword arguments to be used as
                              options for modifying the behavior of path
                              calculations.
        """

        self._options = { }

        for option_name, option_value in iter_dict_items( options ):
            self.__setitem__( option_name, option_value )


    def __iter__( self ):
        """
            Returns an iterator over the options dictionary.
        """

        return iter_dict_keys( self._options )


    def __len__( self ):
        """
            Returns the number of entries in the options dictionary.
        """

        return len( self._options )


    def __getitem__( self, key ):
        """
            Gets an entry from the options dictionary.

            :param key: key into the options dictionary
        """

        try:
            value = self._options[ key ]
        except _builtins_KeyError:
            raise UnknownKeyError(
                _TD_( "Unknown option '{1}' for instance of '{0}'." ),
                self.__class__.__name__, key
            )
        return value


    def __setitem__( self, key, value ):
        """
            Sets an entry in the options dictionary.

            :param key: key into the options dictionary
            :param value: new value of the entry in the options dictionary
        """

        try:
            validator = self._option_validators[ key ]
        except _builtins_KeyError:
            raise InvalidKeyError(
                _TD_( "Invalid option '{1}' for instance of '{0}'." ),
                self.__class__.__name__, key
            )

        if callable( validator ):
            if validator( value ):
                self._options[ key ] = value
            else:
                raise InvalidValueError(
                    _TD_(
                        "Invalid value '{2}' for option '{1}' "
                        "for instance of '{0}'."
                    ),
                    self.__class__.__name__, key, value
                )
        else: self._options[ key ] = value


    def __delitem__( self, key ):
        """
            Deletes an entry in the options dictionary. 

            :param key: key into the options dictionary
        """

        try:
            del self._options[ key ]
        except _builtins_KeyError:
            raise UnknownKeyError(
                _TD_( "Unknown option '{1}' for instance of '{0}'." ),
                self.__class__.__name__, key
            )


    def __repr__( self ):
        """
            Returns a string which can be used by :py:func:`eval
            <CPython3:eval>` to create an instance of the class, having the
            same options as the current instance.
        """

        return "StandardPathContext( {0} )".format(
            ", ".join( map(
                lambda k, v: "{option_name} = {option_value}".format(
                    option_name = k, option_value = v
                ),
                (k for k in iter_dict_keys( self._options )),
                (repr( v ) for v in iter_dict_values( self._options ))
            ) )
        )


    def __str__( self ):
        """
            Returns a dictionary-like representation of the options, both
            default and customized.
        """

        options = OrderedDict( )
        for k, v in self.iter_option_validators( ):
            options[ k ] = v.default
        for k, v in iter_dict_items( self._options ):
            options[ k ] = v
        return "{{ {0} }} ".format(
            ", ".join( map(
                lambda k, v: "{option_name}: {option_value}".format(
                    option_name = k, option_value = v
                ),
                (repr( k ) for k in iter_dict_keys( options )),
                (repr( v ) for v in iter_dict_values( options ))
            ) )
        )


    @property
    def common_path( self ):
        """
            The common installation root path to the particular software 
            product, if specified.
        """

        options = self._options

        if "specific_common_path" in options:
            return options[ "specific_common_path" ]
        
        if "calculate_path" in options:
            return self._calculate_path( )

        if "error_on_none" in options:
            self.raise_UndeterminedPathError( )


    @property
    def user_path( self ):
        """
            The common installation root path to the particular software 
            product, if specified.
        """

        options = self._options

        if "specific_user_path" in options:
            return options[ "specific_user_path" ]
        
        if "calculate_path" in options:
            return self._calculate_path( )

        if "error_on_none" in options:
            self.raise_UndeterminedPathError( )


    def raise_UndeterminedPathError(
        self,
        location_class = None,
        specify_software = False, specify_os = False
    ):
        """
            Raises a UndeterminedPathError exception with a message for the
            context and, optionally, a location class.

            :param location_class: string containing a general name for a
                                   particular class of location in a 
                                   filesystem
            :param specify_software: boolean determining whether information
                                     about the software product should appear
                                     in the reason for the error
            :param specify_os: boolean determining whether information about
                               the operating system should appear in the reason
                               for the error

            :raises: :py:class:`UndeterminedPathError`
        """

        options = self._options

        for_whom = None
        if specify_software:
            software_option_names = \
            [ "software provider name", "software name", "software version", ]
            for_whom = \
            " ".join(
                [   options[ option_name ]
                    for option_name in software_option_names
                    if option_name in options
                ]
            )

        on_os = None
        if specify_os:
            os_option_names = \
            [ "operating system", " operating system version", ]
            on_os = \
            " ".join(
                [   options[ option_name ]
                    for option_name in os_option_names
                    if option_name in options
                ]
            )

        msg_format  = _TD_( "Undetermined path." )
        msg_args    = [ ]
        if   location_class:
            if   for_whom:
                if on_os:
                    msg_format  = \
                    _TD_( "Undetermined path to {0} for {1} on {2}." )
                    msg_args    = [ location_class, for_whom, on_os ]
                else:
                    msg_format  = _TD_( "Undetermined path to {0} for {1}." )
                    msg_args    = [ location_class, for_whom ]
            elif on_os:
                msg_format  = _TD_( "Undetermined path to {0} on {1}." )
                msg_args    = [ location_class, on_os ]
            else:
                msg_format  = _TD_( "Undetermined path to {0}." )
                msg_args    = [ location_class ]
        elif for_whom:
            if on_os:
                msg_format  = _TD_( "Undetermined path for {0} on {1}." )
                msg_args    = [ for_whom, on_os ]
            else:
                msg_format  = _TD_( "Undetermined path for {0}." )
                msg_args    = [ for_whom ]
        elif on_os:
            msg_format  = _TD_( "Undetermined path on {0}." )
            msg_args    = [ on_os ]

        raise UndeterminedPathError( msg_format, *msg_args )


    @abstractmethod
    def _calculate_path( self ):
        """
            Returns the path calculated from information about the software 
            product specified in the options dictionary.
        """

        pass


    def get_with_default( self, option_name, fallback_value = None ):
        """
            If the option, corresponding to the given name, has been customized
            in this instance of a standard path context, then returns the value
            of the customized option. Else if an option valdiator,
            corresponding to the given option name, exists, then return the 
            default value for the option. Else, return the fallback value, if
            one was provided, or ``None`` otherwise.
        """

        if option_name in self._options:
            return self._options[ option_name ]
        if option_name in self._option_validators:
            return self._option_validators[ option_name ].default
        return fallback_value


    def iter_option_validators( self ):
        """
            Returns an iterator over the available option validators.
            Each item returned is a tuple consisting of the validator function
            (or ``None``) and help on the corresponding option.

            This can be useful for getting help on the options in an
            interactive session.
        """

        return iter_dict_items( self._option_validators )


class StandardPath_BASE( AbstractBase_BASE ):
    """
        Abstract base class for the standard path classes of the various
        flavors of operating system archtypes.

        Inherits from :py:class:`AbstractBase_BASE`.
    """


    _context = None


    def __init__( self, context = None ):
        """
            :param context: an object containing the context with which to
                            calculate paths
            :type context: :py:class:`StandardPathContext`
        """

        self._context = context


    def __repr__( self ):
        """
            Returns a string which can be used by :py:func:`eval
            <CPython3:eval>` to create an instance of the class, having the
            same options as the current instance.
        """

        return "StandardPath( {0} )".format(
            repr( self._context ) if self._context is not None else ""
        )


    def __str__( self ):
        """
            Returns a dictionary-like representation of the various paths,
            calculated with the context currently in use.
        """

        path_methods = OrderedDict( [
            [ mn.replace( "whereis_", "", 1 ), mn ]
            for mn in dir( self ) if mn.startswith( "whereis_" )
        ] )
        return "{{ {0} }}".format(
            ", ".join( map(
                lambda k, v: "{path_type}: {path}".format(
                    path_type = repr( k ),
                    path = repr( getattr( self, v )( ) )
                ),
                iter_dict_keys( path_methods ),
                iter_dict_values( path_methods )
            ) )
        )


    # pylint: disable=W0613


    @abstractmethod
    def whereis_temp( self, context = None ):
        """
            Returns the path to the preferred temporary storage for 
            the software product, defined in ``context``.

            The path calculation relies on results from the
            :py:meth:`whereis_preferred_temp_base`.

        """

        raise InvokedAbstractMethodError(
            _TD_( "Invoked abstract method '{1}' in class '{0}'." ),
            self.__class__.__name__, "whereis_temp"
        )


    @abstractmethod
    def whereis_common_config( self, context = None ):
        """
            Returns the path to the directory where the shared or sitewide
            configuration information for the software product, defined in
            ``context``, is stored.

        """

        raise InvokedAbstractMethodError(
            _TD_( "Invoked abstract method '{1}' in class '{0}'." ),
            self.__class__.__name__, "whereis_common_config"
        )


    @abstractmethod
    def whereis_common_resources( self, context = None ):
        """
            Returns the path to the directory where the shared or sitewide
            resources for the software product, defined in ``context``, are
            stored.
        """

        raise InvokedAbstractMethodError(
            _TD_( "Invoked abstract method '{1}' in class '{0}'." ),
            self.__class__.__name__, "whereis_common_resources"
        )


    @abstractmethod
    def whereis_common_programs( self, context = None ):
        """
            Returns the path to the directory where the shared or sitewide
            programs for the software product, defined in ``context``, are
            stored.
        """

        raise InvokedAbstractMethodError(
            _TD_( "Invoked abstract method '{1}' in class '{0}'." ),
            self.__class__.__name__, "whereis_common_programs"
        )


    @abstractmethod
    def whereis_user_config( self, context = None ):
        """
            Returns the path to the directory where the current user's
            configuration information for the software product, defined in
            ``context`` is stored.
        
        """

        raise InvokedAbstractMethodError(
            _TD_( "Invoked abstract method '{1}' in class '{0}'." ),
            self.__class__.__name__, "whereis_user_config"
        )

    
    @abstractmethod
    def whereis_user_resources( self, context = None ):
        """
            Returns the path to the directory where the current user's
            resources for the software product, defined in ``context`` is 
            stored.

        """

        raise InvokedAbstractMethodError(
            _TD_( "Invoked abstract method '{1}' in class '{0}'." ),
            self.__class__.__name__, "whereis_user_resources"
        )


    @abstractmethod
    def whereis_saved_data( self, context = None ):
        """
            Returns the path to the directory where works, created by the
            current user with the software product, defined in ``context``,
            will be stored.

        """

        raise InvokedAbstractMethodError(
            _TD_( "Invoked abstract method '{1}' in class '{0}'." ),
            self.__class__.__name__, "whereis_saved_data"
        )


    @abstractmethod
    def _is_absolute_path( self, the_path ):
        """
            Tests whether the given path is an absolute path on the OS 
            platform for which standard paths are being derived rather 
            than the current OS platform.
        """

        raise InvokedAbstractMethodError(
            _TD_( "Invoked abstract method '{1}' in class '{0}'." ),
            self.__class__.__name__, "_is_absolute_path"
        )


    # pylint: enable=W0613


    def _find_context( self, context ):
        """
            Returns the first available standard path context found.
        """

        if not None is context: return context
        return self._context


    def _choose_common_path_parts( self, context ):
        """
            Returns common base path and specific path from standard path 
            context.
        """

        if      context.common_path \
            and self._is_absolute_path( context.common_path ):
            return context.common_path, None

        base_path = None
        if "common_base_path" in context:
            base_path = context[ "common_base_path" ]
        return base_path, context.common_path


    def _choose_user_path_parts( self, context ):
        """
            Returns user base path and specific path from standard path 
            context.
        """

        if      context.user_path \
            and self._is_absolute_path( context.user_path ):
            return context.user_path, None

        base_path = None
        if "user_base_path" in context:
            base_path = context[ "user_base_path" ]
        return base_path, context.user_path


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

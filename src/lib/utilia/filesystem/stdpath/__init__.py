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
    Provides functionality for calculating paths which are compliant with the 
    standard filesystem layout of a particular OS platform. Significant effort
    is made to comply with published filesystem standards as well as Python
    conventions. Currently, the following OS platforms are supported:

        * Linux [#]_, [#]_

        * MacOS X [#]_, [#]_

        * Windows [#]_, [#]_, [#]_

    The functions contained in this module follow a regular naming
    convention, which provides hints as to their purpose. This convention can
    be expressed as follows.
    
    * Functions, which return paths where the core OS files are 
      typically located, have the word **oscore** in their names.
    
    * Functions, which return paths where the OS distribution files are 
      typically located, have the word **osdist** in their names.

    * Functions, which return paths associated with the default locations 
      where a superuser or systems adminstrator would install software not 
      packaged as part of the OS distribution, have the word **common** in 
      their names.
    
    * The suffix **install_root** denotes that a returned path refers to a 
      top-level directory under which other directories for things, such as 
      configuration information and package resources, can be found.

    * The suffix **pythonic** denotes that a returned path is calculated in
      accordance with :pep:`370` and may rely upon the 
      :py:mod:`site <CPython3:site>` module.

    * The suffix **base** denotes that a returned path refers to an upper-level
      directory of a certain flavor, such as for configuration information or 
      package resources, which is potentially common to many pieces of 
      software and not tied to a particular one.
    
    * Functions, which return paths associated with the location of a 
      particular piece of software, have the word **my** in their names. 
    
    * Functions, which return paths relative to the current user's home 
      directory, have the word **user** in their names.

    Most of the functions can be instructed to operate in a *return None on
    failure* mode or a *raise exception on failure* mode. By default, these
    functions return ``None`` on failure to determine a path. However, all
    functions raise a :py:class:`UnsupportedFilesystemLayout` exception if they
    lack the logic necessary to support the filesystem layout of a particular OS
    platform.

    Here is a list of higher level functions, which users of this module will
    most likely be interested in:

    * :py:func:`whereis_my_user_config`

    * :py:func:`whereis_my_user_resources`

    * :py:func:`whereis_my_common_config`

    * :py:func:`whereis_my_common_resources`

    * :py:func:`whereis_my_temp`

    * :py:func:`whereis_my_saved_data`

    Please see their documentation and the
    :ref:`SECTION-utilia.filesystem.stdpath-Examples` section for details on 
    using them.
"""

# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


# TODO: Pass a context object instead of 'specific_path' strings.
#           XDG Base Paths vs. Traditional User Data Paths
#       Should carry software name for improved exception messages.
# TODO: Support XDG environment variables.


import sys
from os import (
    environ                 as envvars,
)
from os.path import (
    join                    as join_path,
    dirname                 as dirname_of_path,
    expanduser              as expand_user_path,
)
import platform
import site
import functools
import re


from utilia import (
    _autodoc_function_parameters,
    _TD_,
    Error_WithReason,
)
from utilia.compat.builtins import ( # pylint: disable=W0622
    reduce,
)
from .. import (
    Error_BASE              as FilesystemError_BASE,
)


# TODO: Move to another module.
def join_filtered_path( *posargs ):
    """
        Returns a path, composed of all of the supplied elements.
        Any empty elements are dropped prior to joining them.
    """

    return join_path( *filter( None, posargs ) )


def __DOCSTRING_FRAGMENTS( ):
    """
        Returns a dictionary of common docstring fragments.
    """
    return \
    {
        "error_on_none": \
    """
        :param error_on_none: If ``True``, cause an exception to be raised 
                              if the return value would be ``None``.
        :type error_on_none: :py:func:`boolean <CPython3:bool>`
    """,
        "software_name": \
    """
        :param software_name: Consider the name of this software product when
                              constructing a path fragment which identifies 
                              it.
        :type software_name: :py:class:`string <CPython3:str>`
    """,
        "vendor_name": \
    """
        :param vendor_name: Consider the name of this software vendor when 
                            constructing a path fragment which identifies a 
                            software product.
        :type vendor_name: :py:class:`string <CPython3:str>`
    """,
        "version": \
    """
        :param version: Consider this version string when constructing a path
                        fragment which identifies a software product.
        :type version: :py:class:`string <CPython3:str>`
    """,
        "base_path": \
    """
        :param base_path: Calculate path, using this path as the base.
        :type base_path: :py:class:`string <CPython3:str>`
    """,
        "specific_path": \
    """
        :param specific_path: Calculate path, using this path as the most
                              specific part.
        :type specific_path: :py:class:`string <CPython3:str>`
    """,
        "prefer_common": \
    """
        :param prefer_common: If ``True``, the common path, if it exists, 
                              will be preferred over the user path.
        :type prefer_common: :py:func:`boolean <CPython3:bool>`
    """,
        "RTYPE_string_or_None": \
    """
        :rtype: :py:class:`string <CPython3:str>` or ``None``
    """,
        "RAISES_Undetermined": \
    """
        :raises: :py:class:`UndeterminedFilesystemPath`, if a path could not 
                 be determined and the ``error_on_none`` argument is ``True``.
    """,
        "RAISES_Unsupported_and_Undetermined": \
    """
        :raises: 

                 * :py:class:`UnsupportedFilesystemLayout`, if there is no 
                   path determination logic for the filesystem layout.

                 * :py:class:`UndeterminedFilesystemPath`, if a path could not 
                   be determined and the ``error_on_none`` argument is 
                   ``True``.
    """,
    }


def __decorate_docstring( func ):
    """
        Appends additional documentation to a docstring.
    """

    docs_DICT = __DOCSTRING_FRAGMENTS( )

    _autodoc_function_parameters( func, docs_DICT )
    func.__doc__ += docs_DICT[ "RTYPE_string_or_None" ]
    func.__doc__ += docs_DICT[ "RAISES_Unsupported_and_Undetermined" ]

    return func


# Character Translators for Names
__whitespace_to_underscore  = functools.partial( re.sub, r"\s+", "_" )
__dot_to_underscore         = functools.partial( re.sub, r"\.{1,1}", "_" )


class UnsupportedFilesystemLayout( FilesystemError_BASE, Error_WithReason ):
    """
        Error if the standard filesystem layout associated with the current OS
        is unknown or unsupported.

        Inherits from :py:class:`utilia.filesystem.Error_BASE` and
        :py:class:`utilia.Error_WithReason`.
    """


    def __init__( self, reason_format, *reason_args ):
        """
            Invokes superclass initializers.

            :param reason_format: String containing zero or more 
                                  ``format``-style substitution tokens.
            :param *reason_args: Zero or more arguments to be substituted into
                                 the reason format string.
        """

        super( UnsupportedFilesystemLayout, self ).__init__(
            reason_format, *reason_args
        )
        # TODO: Set appropriate exit status.


class UndeterminedFilesystemPath( FilesystemError_BASE, Error_WithReason ):
    """
        Error if unable to ascertain a reasonably standard path for something.

        Inherits from :py:class:`utilia.filesystem.Error_BASE` and
        :py:class:`utilia.Error_WithReason`.
    """


    def __init__( self, reason_format, *reason_args ):
        """
            Invokes superclass initializers.

            :param reason_format: String containing zero or more 
                                  ``format``-style substitution tokens.
            :param *reason_args: Zero or more arguments to be substituted into
                                 the reason format string.
        """

        super( UndeterminedFilesystemPath, self ).__init__(
            reason_format, *reason_args
        )
        # TODO: Set appropriate exit status.


def __decide_upon_error_on_none(
    error_on_none, path,
    location, evname = None, specific_path = None
):
    """
        Raises an 'UndeterminedFilesystemPath' exception, if the
        'error_on_none' argument is true and the supplied path is empty.
    """

    if error_on_none and (None is path):

        if specific_path:
            if evname:
                error_reason_format = _TD_(
                    "Undetermined path to {0} for '{1}'."
                    " (Environment variable, '{2}', not set.)"
                )
                error_reason_args   = [ location, specific_path, evname ]
            else:
                error_reason_format = _TD_(
                    "Undetermined path to {0} for '{1}'."
                )
                error_reason_args   = [ location, specific_path ]
        else:
            if evname:
                error_reason_format = _TD_(
                    "Undetermined path to {0}."
                    " (Environment variable, '{1}', not set.)"
                )
                error_reason_args   = [ location, evname ]
            else:
                error_reason_format = _TD_( "Undetermined path to {0}." )
                error_reason_args   = [ location ]

        raise UndeterminedFilesystemPath(
            error_reason_format, *error_reason_args
        )


def __raise_UnsupportedFilesystemLayout( fsl ):
    """
        Raise an 'UnsupportedFilesystemLayout' error with a standard message.
    """

    raise UnsupportedFilesystemLayout(
        "Unimplemented path determination logic for {0}.", fsl
    )


# TODO: Return dictionary of values rather than simple string.
def which_fs_layout( ):
    """
        Returns a classification of the expected filesystem layout according 
        to the OS in use, if there is a classifier for that OS.

        The possible filesystem layout classifications are as follows:

        .. csv-table::
           :header: "Classification", "Operating Systems"
           :widths: 20, 80

           "POSIX",     "Linux"
           "MacOS X",   "Darwin"
           "Windows",   "Windows"

        :rtype: :py:class:`string <CPython3:str>`
        :raises: :py:class:`UnsupportedFilesystemLayout`, if there is no 
                 classifier implemented for the OS in use.
    """

    osa = platform.system( )

    if   osa in [ "Linux", ]:
        return "POSIX"
    elif osa in [ "Darwin", ]:
        return "MacOS X"
    elif osa in [ "Windows", ]:
        return "Windows"
    else:
        raise UnsupportedFilesystemLayout(
            "Unimplemented filesystem layout classifier for {0}.", osa
        )

_autodoc_function_parameters( which_fs_layout, __DOCSTRING_FRAGMENTS( ) )


def __computed_MacOS_X_python_prefix( prefix ):
    """
        If the Python prefix is for a MacOS X framework installation,
        then returns a truncated prefix, which can be used as a better base.
        Else, returns the prefix without alteration.
    """

    match = re.findall( r".*/Python\.framework/Versions/.*", prefix )
    if match:
        return reduce( lambda x, f: f( x ), [ dirname_of_path ] * 4, prefix )
    
    return prefix


def __computed_Windows_program_files_path( error_on_none = False ):
    """
        Returns the correct path to the "Program Files" directory, 
        depending on whether the OS is 32-bit or 64-bit and the running Python
        is 32-bit or 64-bit.
    """

    common_base_path    = None
    location            = _TD_( "Windows program files" )
    evname              = None

    if "64bit" in platform.architecture( ):
        if sys.maxsize > 2**32: evname = "ProgramFiles"
        else:                   evname = "ProgramFiles(x86)"
    else:                       evname = "ProgramFiles"
    common_base_path = envvars.get( evname, None )

    __decide_upon_error_on_none(
        error_on_none, common_base_path, location, evname
    )
    return common_base_path


@__decorate_docstring
def concatenated_software_path_fragment(
    software_name, vendor_name = None, version = None,
    error_on_none = False
):
    """
        Returns a concatenation of the name of a software product with an  
        optional name of the software product's vendor and an optional version 
        string for the software product as a filesystem path fragment typical
        for the operating system architecture.
    """

    # Note: Conversion of whitespaces to underscores is performed on POSIX
    #       operating systems to facilitate command-line navigation. 
    #       This is considered to be less important on the MacOS X and 
    #       Windows operating systems, which ship with Finder and Explorer 
    #       respectively.
    # Note: No conversion of decimal points to underscores is performed on
    #       Windows operating systems, because directory names are being
    #       returned rather than file names and so there are no concerns about
    #       name extensions.
    
    path_fragment       = None
    error_reason_format = _TD_( "Empty software-specific path fragment." )

    fsl = which_fs_layout( )

    if not software_name:
        error_reason_format = _TD_( "Software name is unspecified." )

    else:

        if vendor_name:
            vendor_name = vendor_name.strip( )
            if   fsl in [ "POSIX", ]:
                vendor_name = __whitespace_to_underscore( vendor_name )
            elif fsl in [ "MacOS X", ]: pass
            elif fsl in [ "Windows", ]: pass
            else: __raise_UnsupportedFilesystemLayout( fsl )
        
        software_name = software_name.strip( )
        if   fsl in [ "POSIX", ]:
            software_name = __whitespace_to_underscore( software_name )
        elif fsl in [ "MacOS X", ]: pass
        elif fsl in [ "Windows", ]: pass
        else: __raise_UnsupportedFilesystemLayout( fsl )
        
        if version:
            version = version.strip( )
            if   fsl in [ "POSIX", ]:
                version = __whitespace_to_underscore( version )
            elif fsl in [ "MacOS X", ]: pass
            elif fsl in [ "Windows", ]:  pass
            else: __raise_UnsupportedFilesystemLayout( fsl )
        
        path_fragment = \
        join_filtered_path( vendor_name, software_name, version )

    if error_on_none and (None is path_fragment):
        raise UndeterminedFilesystemPath( error_reason_format )
    return path_fragment


@__decorate_docstring
def whereis_oscore_install_root( error_on_none = False ):
    """
        Returns the path to the installation root for the core OS components,
        if it can be determined. Returns ``None``, otherwise.

        Environment variables or API calls may help determine this path on
        certain operating systems. In other cases, this path is fixed.
        
        Below is a table of typical paths by filesystem layout classification:

        .. csv-table::
           :header: "Classification", "Path"
           :widths: 20, 80

           "POSIX",     "/"
           "MacOS X",   "/"
           "Windows",   "C:\\\\Windows\\\\System32"
        
    """

    irp_evname          = None
    install_root_path   = None
    location            = _TD_( "OS core installation root" )

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", "MacOS X", ]:
        install_root_path = "/"
    elif fsl in [ "Windows", ]:
        irp_evname = "SystemRoot"
        install_root_path = envvars.get( irp_evname, None )
        if install_root_path:
            install_root_path = join_path( install_root_path, "System32" )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, install_root_path, location, irp_evname
    )
    return install_root_path


@__decorate_docstring
def whereis_osdist_install_root( error_on_none = False ):
    """
        Returns the path to the installation root of the OS distribution,
        if it can be determined. Returns ``None``, otherwise.

        Environment variables or API calls may help determine this path on
        certain operating systems. In other cases, this path is fixed.
        
        Below is a table of typical paths by filesystem layout classification:

        .. csv-table::
           :header: "Classification", "Path"
           :widths: 20, 80

           "POSIX",     "/usr"
           "MacOS X",   "/System"
           "Windows",   "C:\\\\Windows"
        
    """

    irp_evname          = None
    install_root_path   = None
    location            = _TD_( "OS distribution installation root" )

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", ]:   install_root_path = "/usr"
    elif fsl in [ "MacOS X", ]: install_root_path = "/System"
    elif fsl in [ "Windows", ]:
        irp_evname = "SystemRoot"
        install_root_path = envvars.get( irp_evname, None )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, install_root_path, location, irp_evname
    )
    return install_root_path


@__decorate_docstring
def whereis_common_install_root( error_on_none = False ):
    """
        Returns the path to the typical default root for a shared or sitewide 
        software installation by the superuser or systems administrator, 
        if it can be determined. Returns ``None``, otherwise.

        Environment variables or API calls may help determine this path on
        certain operating systems. In other cases, this path is fixed.
        
        Below is a table of typical paths by filesystem layout classification:

        .. csv-table::
           :header: "Classification", "Path"
           :widths: 20, 80

           "POSIX",     "/usr/local"
           "MacOS",     "/Library"
           "Windows",   "C:\\\\Program Files"
        
    """

    irp_evname          = None
    install_root_path   = None
    location            = _TD_( "common installation root" )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl:    install_root_path = "/usr/local"
    elif "MacOS X" == fsl:  install_root_path = "/Library"
    elif "Windows" == fsl:
        install_root_path = \
        __computed_Windows_program_files_path( error_on_none = error_on_none )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, install_root_path, location, irp_evname
    )
    return install_root_path


@__decorate_docstring
def whereis_oscore_config_base( error_on_none = False ):
    """
        Returns the path to the typical top-level directory under which the
        configuration information resides for the core OS components, 
        if it can be determined. Returns ``None``, otherwise.
        
        Below is a table of typical paths by filesystem layout classification:

        .. csv-table::
           :header: "Classification", "Path"
           :widths: 20, 80

           "POSIX",     "/etc"
           "MacOS X",   "/System/Preferences"
           "Windows",   "C:\\\\Windows\\\\System32\\\\Config"

    """

    cbp_evname          = None
    config_base_path    = None
    location            = _TD_( "OS core configuration information" )

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", ]:   config_base_path = "/etc"
    elif fsl in [ "MacOS X", ]: config_base_path = "/System/Preferences"
    elif fsl in [ "Windows", ]:
        cbp_evname = "SystemRoot"
        config_base_path = envvars.get( cbp_evname, None )
        if config_base_path:
            config_base_path = \
            join_path( config_base_path, "System32", "Config"  )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, config_base_path, location, cbp_evname
    )
    return config_base_path


@__decorate_docstring
def whereis_osdist_config_base( error_on_none = False ):
    """
        Returns the path to the typical top-level directory under which the
        configuration information resides for the core OS components, 
        if it can be determined. Returns ``None``, otherwise.
        
        Below is a table of typical paths by filesystem layout classification:

        .. csv-table::
           :header: "Classification", "Path"
           :widths: 20, 80

           "POSIX",     "/etc"
           "MacOS X",   "/System/Preferences"
           "Windows",   ""

    """

    cbp_evname          = None
    config_base_path    = None
    location            = _TD_( "OS distribution configuration information" )

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", ]:   config_base_path = "/etc"
    elif fsl in [ "MacOS X", ]: config_base_path = "/System/Preferences"
    elif fsl in [ "Windows", ]: pass
    else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, config_base_path, location, cbp_evname
    )
    return config_base_path


@__decorate_docstring
def whereis_common_config_base( error_on_none = False ):
    """
        Returns the path to the typical top-level directory under which the
        configuration information resides for software installed by the
        superuser or systems administrator, if it can be determined. Returns
        ``None``, otherwise.
        
        Below is a table of typical paths by filesystem layout classification:

        .. csv-table::
           :header: "Classification", "Path"
           :widths: 20, 80

           "POSIX",     "/usr/local/etc"
           "MacOS X",   "/Library/Preferences"
           "Windows",   ""

    """

    cbp_evname          = None
    config_base_path    = None
    location            = _TD_( "common configuration information" )

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", ]:   config_base_path = "/usr/local/etc"
    elif fsl in [ "MacOS X", ]: config_base_path = "/Library/Preferences"
    elif fsl in [ "Windows", ]: pass
    else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, config_base_path, location, cbp_evname
    )
    return config_base_path


@__decorate_docstring
def whereis_user_home( error_on_none = False ):
    """
        Returns the path to the current user's home directory, if it can be
        determined. Returns ``None``, otherwise.

    """

    user_id                 = None
    user_home_path          = None

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", "MacOS X", ]:
        user_id         = envvars.get( "USER", None )
        user_home_path  = expand_user_path( "~" )
        if "~" == user_home_path: user_home_path = None
    elif fsl in [ "Windows", ]:
        user_id         = envvars.get( "UserName", None )
        user_home_path  = envvars.get( "UserProfile", None )
    else: __raise_UnsupportedFilesystemLayout( fsl )
    
    if (None is user_home_path) and error_on_none:
        if user_id:
            error_reason_format = \
            _TD_( "Unknown home directory for user '{0}'." )
            error_reason_args   = [ user_id ]
        else:
            error_reason_format = _TD_( "Unknown ID of current user." )
            error_reason_args   = [ ]
        raise UndeterminedFilesystemPath( 
            error_reason_format, *error_reason_args
        )
    return user_home_path


@__decorate_docstring
def whereis_common_temp_base( error_on_none = False ):
    """
        Returns the path to the temporary storage area available for use by
        everyone on the system.
        
        Below is a table of typical paths by filesystem layout classification:

        .. csv-table::
           :header: "Classification", "Path"
           :widths: 20, 80

           "POSIX",     "/tmp"
           "MacOS X",   "/tmp"
           "Windows",   ""

    """

    temp_base_path  = None
    location        = _TD_( "common temporary storage area" )

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", "MacOS X" ]: temp_base_path = "/tmp"
    elif fsl in [ "Windows", ]:         pass
    else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, temp_base_path, location
    )
    return temp_base_path


@__decorate_docstring
def whereis_user_temp_base( error_on_none = False ):
    """
        Returns the path to the current user's temporary storage area.

    """

    utbp_evname     = None
    temp_base_path  = None
    location        = _TD_( "user-specific temporary storage area" )

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", "MacOS X", ]:    pass
    elif fsl in [ "Windows", ]:
        utbp_evname = "Temp"
        temp_base_path = envvars.get( utbp_evname, None )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, temp_base_path, location, utbp_evname
    )
    return temp_base_path


@__decorate_docstring
def whereis_preferred_temp_base(
    prefer_common = False,
    error_on_none = False
):
    """
        Returns:
        
        * the result from a call to :py:func:`whereis_common_temp_base`, 
          if it is not ``None`` and the ``prefer_common`` argument is 
          ``True``;
        
        * the result from a call to :py:func:`whereis_user_temp_base`, 
          if it is not ``None``;

        * the result from a call to :py:func:`whereis_common_temp_base`, 
          if it is not ``None``; 
        
        * or ``None``, if all else fails.

    """

    temp_base_path      = None
    error_reason_format = \
    _TD_( "Undetermined path to preferred temporary storage." )
    error_reason_args   = [ ]

    utbp = stbp = None

    try: utbp = whereis_user_temp_base( error_on_none = error_on_none )
    except UndeterminedFilesystemPath as exc:
        error_reason_format = exc.error_reason_format
        error_reason_args   = exc.error_reason_args 

    try: stbp = whereis_common_temp_base( error_on_none = error_on_none )
    except UndeterminedFilesystemPath as exc:
        error_reason_format = exc.error_reason_format
        error_reason_args   = exc.error_reason_args 

    if   stbp and prefer_common:    temp_base_path = stbp
    elif utbp:                      temp_base_path = utbp
    elif stbp:                      temp_base_path = stbp
    
    if (None is temp_base_path) and error_on_none:
        raise UndeterminedFilesystemPath(
            error_reason_format, *error_reason_args
        )
    return temp_base_path


@__decorate_docstring
def whereis_my_temp(
    specific_path = None, prefer_common = False, error_on_none = False
):
    """
        Returns the path to the preferred temporary storage for the specific
        software.

        The path calculation relies on results from the
        :py:func:`whereis_preferred_temp_base` and the 
        :py:func:`concatenated_software_path_fragment` functions.

    """

    base_path   = None
    full_path   = None
    evname      = None

    base_path = \
    whereis_preferred_temp_base(
        error_on_none = error_on_none, prefer_common = prefer_common
    )
    full_path = join_filtered_path( base_path, specific_path )
    
    __decide_upon_error_on_none(
        error_on_none, full_path, 
        _TD_( "temporary storage area" ), 
        evname, specific_path
    )
    return full_path


@__decorate_docstring
def whereis_my_common_config_at_base(
    base_path, specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the shared configuration
        information for the specific software is stored.

    """

    fsl         = which_fs_layout( )
    full_path   = None
    evname      = None

    if base_path:

        if   fsl in [ "POSIX", ]:
            if "/usr" == base_path: base_path = "/"
            full_path = \
            join_filtered_path( base_path, "etc", specific_path )
        elif fsl in [ "MacOS X", ]:
            base_path_orig = base_path
            base_path = __computed_MacOS_X_python_prefix( base_path )
            if base_path.startswith( "/System" ): base_path = "/Library"
            posix_flavor = \
            (base_path_orig == base_path) and ("/Library" != base_path)
            if posix_flavor:
                if "/usr" == base_path: base_path = "/"
                full_path = \
                join_filtered_path( base_path, "etc", specific_path )
            else:
                full_path = \
                join_filtered_path( base_path, "Preferences", specific_path )
        elif fsl in [ "Windows", ]:
            if specific_path:
                full_path = \
                join_filtered_path( base_path, specific_path, "Config" )
        else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, full_path,
        _TD_( "shared configuration information" ),
        evname, specific_path
    )
    return full_path


@__decorate_docstring
def whereis_my_common_config(
    specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the shared configuration
        information for the specific software is stored. (This path is 
        relative to the current OS platform's standard shared location for 
        configuration information.)

    """

    fsl         = which_fs_layout( )
    base_path   = whereis_common_install_root( error_on_none = error_on_none )

    if   fsl in [ "POSIX", ]:
        base_path = \
        whereis_common_install_root( error_on_none = error_on_none )
    elif fsl in [ "MacOS X", ]:
        base_path = \
        whereis_common_install_root( error_on_none = error_on_none )
    elif fsl in [ "Windows", ]:
        base_path = \
        whereis_common_install_root( error_on_none = error_on_none )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    return whereis_my_common_config_at_base(
        base_path, specific_path, error_on_none
    )


@__decorate_docstring
def whereis_my_common_config_pythonic(
    specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the shared configuration
        information for the specific software is stored. (This path is 
        relative to the current Python's current installation base directory.)

    """

    fsl         = which_fs_layout( )
    base_path   = sys.prefix
    full_path   = None
    evname      = None

    if base_path:

        # NOTE: Possible PEP 370 violation.
        if   fsl in [ "POSIX", ]:
            full_path = join_filtered_path( base_path, "etc", specific_path )
        elif fsl in [ "MacOS X", ]:
            base_path_orig = base_path
            base_path = __computed_MacOS_X_python_prefix( base_path )
            if base_path.startswith( "/System" ): base_path = "/Library"
            posix_flavor = \
            (base_path_orig == base_path) and ("/Library" != base_path)
            if posix_flavor:
                full_path = \
                join_filtered_path( base_path, "etc", specific_path )
            else:
                full_path = \
                join_filtered_path(
                    base_path, "Preferences", specific_path
                )
        elif fsl in [ "Windows", ]:
            full_path = \
            join_filtered_path( base_path, "Config", specific_path )
        else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, full_path,
        _TD_( "Pythonic shared configuration information" ),
        evname, specific_path
    )
    return full_path


@__decorate_docstring
def whereis_my_common_resources_at_base(
    base_path, specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the shared resources for the
        specific software are stored.

    """

    fsl         = which_fs_layout( )
    full_path   = None
    evname      = None

    if base_path:

        if   fsl in [ "POSIX", ]:
            if "/" == base_path:
                full_path = \
                join_filtered_path( base_path, "etc", specific_path )
            else:
                full_path = \
                join_filtered_path( base_path, "share", specific_path )
        elif fsl in [ "MacOS X", ]:
            base_path_orig = base_path
            base_path = __computed_MacOS_X_python_prefix( base_path )
            if base_path.startswith( "/System" ): base_path = "/Library"
            posix_flavor = \
            (base_path_orig == base_path) and ("/Library" != base_path)
            if posix_flavor:
                if "/" == base_path:
                    full_path = \
                    join_filtered_path( base_path, "etc", specific_path )
                else:
                    full_path = \
                    join_filtered_path( base_path, "share", specific_path )
            else:
                full_path = \
                join_filtered_path(
                    base_path, "Application Support", specific_path
                )
        elif fsl in [ "Windows", ]:
            if specific_path:
                full_path = \
                join_filtered_path( base_path, specific_path, "Resources" )
        else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, full_path,
        _TD_( "shared resources" ),
        evname, specific_path
    )
    return full_path


@__decorate_docstring
def whereis_my_common_resources(
    specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the shared resources for the
        specific software are stored. (This path is relative to the current OS
        platform's standard shared location for resources.)

    """

    fsl         = which_fs_layout( )
    base_path   = whereis_common_install_root( error_on_none = error_on_none )

    if   fsl in [ "POSIX", ]:
        base_path = \
        whereis_common_install_root( error_on_none = error_on_none )
    elif fsl in [ "MacOS X", ]:
        base_path = \
        whereis_common_install_root( error_on_none = error_on_none )
    elif fsl in [ "Windows", ]:
        base_path = \
        whereis_common_install_root( error_on_none = error_on_none )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    return whereis_my_common_resources_at_base(
        base_path, specific_path, error_on_none
    )


@__decorate_docstring
def whereis_my_common_resources_pythonic(
    specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the shared resources for the
        specific software are stored. (This path is relative to the current
        Python's current installation base directory.)

    """

    fsl         = which_fs_layout( )
    base_path   = sys.prefix
    full_path   = None
    evname      = None

    if base_path:

        # NOTE: Possible PEP 370 violation.
        if   fsl in [ "POSIX", ]:
            full_path = join_filtered_path( base_path, "share", specific_path )
        elif fsl in [ "MacOS X", ]:
            base_path_orig = base_path
            base_path = __computed_MacOS_X_python_prefix( base_path )
            if base_path.startswith( "/System" ): base_path = "/Library"
            posix_flavor = \
            (base_path_orig == base_path) and ("/Library" != base_path)
            if posix_flavor:
                full_path = \
                join_filtered_path( base_path, "share", specific_path )
            else:
                full_path = \
                join_filtered_path(
                    base_path, "Application Support", specific_path
                )
        elif fsl in [ "Windows", ]:
            full_path = \
            join_filtered_path( base_path, "Resources", specific_path )
        else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, full_path,
        _TD_( "Pythonic shared resources" ),
        evname, specific_path
    )
    return full_path


# TODO: whereis_my_site_programs
# TODO: whereis_my_site_docs


@__decorate_docstring
def whereis_my_user_config_at_base(
    base_path, specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the current user's configuration
        information for the specific software is stored.

    """

    fsl         = which_fs_layout( )
    full_path   = None
    evname      = None

    if base_path:

        if   fsl in [ "POSIX", ]:
            full_path = \
            join_filtered_path( base_path, ".config", specific_path )
        elif fsl in [ "MacOS X", ]:
            posix_flavor = \
            sys.prefix == __computed_MacOS_X_python_prefix( sys.prefix )
            if posix_flavor:    mid_path = ".config"
            else:               mid_path = "Preferences"
            full_path = \
            join_filtered_path( base_path, mid_path, specific_path )
        elif fsl in [ "Windows", ]:
            if specific_path:
                full_path = \
                join_filtered_path( base_path, specific_path, "Config" )
        else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, full_path,
        _TD_( "user-specific configuration information" ),
        evname, specific_path
    )
    return full_path


@__decorate_docstring
def whereis_my_user_config(
    specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the current user's configuration
        information for the specific software is stored. (This path is 
        relative to the current OS platform's standard per-user location for 
        configuration information.)

    """

    fsl         = which_fs_layout( )
    base_path   = None

    if   fsl in [ "POSIX", ]:
        base_path = whereis_user_home( error_on_none = error_on_none )
    elif fsl in [ "MacOS X", ]:
        uhp = whereis_user_home( error_on_none = error_on_none )
        if uhp:
            posix_flavor = \
            sys.prefix == __computed_MacOS_X_python_prefix( sys.prefix )
            if posix_flavor:    base_path = uhp
            else:               base_path = join_path( uhp, "Library" )
    elif fsl in [ "Windows", ]:
        base_path = envvars.get( "AppData", None )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    return whereis_my_user_config_at_base(
        base_path, specific_path, error_on_none
    )


@__decorate_docstring
def whereis_my_user_config_pythonic(
    specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the current user's configuration
        information for the specific software are stored. (This path is 
        relative to Python's user base directory, as specified by :pep:`370`.)

    """

    fsl         = which_fs_layout( )
    base_path   = site.USER_BASE
    full_path   = None
    evname      = None

    if base_path:

        # NOTE: Possible PEP 370 violation.
        if   fsl in [ "POSIX", ]:
            full_path = join_filtered_path( base_path, "etc", specific_path )
        elif fsl in [ "MacOS X", ]:
            posix_flavor = \
            sys.prefix == __computed_MacOS_X_python_prefix( sys.prefix )
            if posix_flavor:    mid_path = "etc"
            else:               mid_path = "Preferences"
            full_path = \
            join_filtered_path( base_path, mid_path, specific_path )
        elif fsl in [ "Windows", ]:
            full_path = \
            join_filtered_path( base_path, "Config", specific_path )
        else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, full_path,
        _TD_( "Pythonic user-specific configuration information" ),
        evname, specific_path
    )
    return full_path


@__decorate_docstring
def whereis_my_user_resources_at_base(
    base_path, specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the current user's resources for
        the specific software are stored.

    """

    fsl         = which_fs_layout( )
    full_path   = None
    evname      = None

    if base_path:

        if   fsl in [ "POSIX", ]:
            full_path = \
            join_filtered_path( base_path, ".local/share", specific_path )
        elif fsl in [ "MacOS X", ]:
            posix_flavor = \
            sys.prefix == __computed_MacOS_X_python_prefix( sys.prefix )
            if posix_flavor:    mid_path = ".local/share"
            else:               mid_path = "Application Support"
            full_path = \
            join_filtered_path( base_path, mid_path, specific_path )
        elif fsl in [ "Windows", ]:
            if specific_path:
                full_path = \
                join_filtered_path( base_path, specific_path, "Resources" )
        else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, full_path,
        _TD_( "user-specific resources" ),
        evname, specific_path
    )
    return full_path


@__decorate_docstring
def whereis_my_user_resources(
    specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the current user's resources for
        the specific software are stored. (This path is relative to the current
        OS platform's standard per-user location for resources.)

    """

    fsl         = which_fs_layout( )
    base_path   = None

    if   fsl in [ "POSIX", ]:
        base_path = whereis_user_home( error_on_none = error_on_none )
    elif fsl in [ "MacOS X", ]:
        uhp = whereis_user_home( error_on_none = error_on_none )
        if uhp:
            posix_flavor = \
            sys.prefix == __computed_MacOS_X_python_prefix( sys.prefix )
            if posix_flavor:    base_path = uhp
            else:               base_path = join_path( uhp, "Library" )
    elif fsl in [ "Windows", ]:
        base_path = envvars.get( "AppData", None )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    return whereis_my_user_resources_at_base(
        base_path, specific_path, error_on_none
    )


@__decorate_docstring
def whereis_my_user_resources_pythonic(
    specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory, where the current user's resources for
        the specific software are stored. (This path is relative to Python's
        user base directory, as specified by :pep:`370`.)

    """

    fsl         = which_fs_layout( )
    base_path   = site.USER_BASE
    full_path   = None
    evname      = None

    if base_path:

        # NOTE: Possible PEP 370 violation.
        if   fsl in [ "POSIX", ]:
            full_path = join_filtered_path( base_path, "share", specific_path )
        elif fsl in [ "MacOS X", ]:
            posix_flavor = \
            sys.prefix == __computed_MacOS_X_python_prefix( sys.prefix )
            if posix_flavor:    mid_path = "share"
            else:               mid_path = "Application Support"
            full_path = \
            join_filtered_path( base_path, mid_path, specific_path )
        elif fsl in [ "Windows", ]:
            full_path = \
            join_filtered_path( base_path, "Resources", specific_path )
        else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, full_path,
        _TD_( "Pythonic user-specific resources" ),
        evname, specific_path
    )
    return full_path


# TODO: whereis_my_user_docs


@__decorate_docstring
def whereis_my_saved_data_at_base(
    base_path, specific_path = None, error_on_none = False
):
    """
        Returns a path to the directory where works, created by the current
        user, will be stored.

    """
    
    fsl         = which_fs_layout( )
    full_path   = None
    evname      = None

    if base_path:

        if   fsl in [ "POSIX", ]:   pass
        elif fsl in [ "MacOS X", "Windows", ]:
            full_path = \
            join_filtered_path( base_path, "Documents", specific_path )
        else: __raise_UnsupportedFilesystemLayout( fsl )

    __decide_upon_error_on_none(
        error_on_none, full_path, _TD_( "saved data" ), evname, specific_path
    )
    return full_path


@__decorate_docstring
def whereis_my_saved_data( specific_path = None, error_on_none = False ):
    """
        Returns a path to the directory where works, created by the user of the
        specific software, will be stored.

        Uses :py:func:`.whereis_user_home` internally.

    """

    fsl         = which_fs_layout( )
    base_path   = None

    if   fsl in [ "POSIX", ]:   pass
    if   fsl in [ "MacOS X", "Windows", ]:
        base_path = whereis_user_home( error_on_none = error_on_none )
    else: __raise_UnsupportedFilesystemLayout( fsl )

    return whereis_my_saved_data_at_base(
        base_path, specific_path, error_on_none
    )


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

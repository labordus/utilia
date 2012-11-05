###############################################################################
#				   utilia				      #
#-----------------------------------------------------------------------------#
#									      #
#   Licensed under the Apache License, Version 2.0 (the "License");	      #
#   you may not use this file except in compliance with the License.	      #
#   You may obtain a copy of the License at				      #
#									      #
#       http://www.apache.org/licenses/LICENSE-2.0			      #
#									      #
#   Unless required by applicable law or agreed to in writing, software	      #
#   distributed under the License is distributed on an "AS IS" BASIS,	      #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and	      #
#   limitations under the License.					      #
#									      #
###############################################################################

"""
    Provides functionality for calculating paths which are compliant with the 
    standard filesystem layout of a particular OS platform. Significant effort
    is made to comply with published filesystem standards as well as Python
    conventions.

    Currently, the following OS platforms are supported:

    * Linux

    * MacOS X

    * Windows

    The functions contained in this module following a regular naming
    convention, which provides hints as to their function. This convention can
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
      configuration information and data stores, can be found.

    * The suffix **base** denotes that a returned path refers to an upper-level
      directory of a certain flavor, such as for configuration information or 
      data stores, which is potentially common to many pieces of software 
      and not tied to a particular one.
    
    * Functions, which return paths associated with the location of a 
      particular piece of software, have the word **my** in their names. 
    
    * Functions, which return paths relative to the current user's home 
      directory, have the word **user** in their names.

    * Functions, which return paths for shared or system-wide directories,
      associated with a particlar pieces of software, have the word **site** 
      in their names.

    Most of the functions can be instructed to operate in a *return None on
    failure* mode or a *raise exception on failure* mode. By default, these
    functions return ``None`` on failure to determine a path. However, all
    functions raise a :py:class:`UnsupportedFilesystemLayout` exception if they
    lack the logic necessary to support the filesystem layout of a particular OS
    platform.

    Here is a list of higher level functions, which users of this module will
    most likely be interested in:

    * :py:func:`whereis_my_user_config`

    * :py:func:`whereis_my_user_data`

    * :py:func:`whereis_my_site_config`

    * :py:func:`whereis_my_site_data`

    * :py:func:`whereis_my_temp`

    * :py:func:`whereis_my_saves`

    Please see their documentation and the
    :ref:`SECTION-utilia.filesystem.stdpath-Examples` section for details on 
    using them.
"""

# Note: Future imports must go before other imports.
from __future__ import (
    division		    as __FUTURE_division,
    absolute_import	    as __FUTURE_absolute_import,
    print_function	    as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


import sys
from os import (
    environ		    as envvars,
)
from os.path import (
    sep			    as path_dirsep,
    join		    as path_join,
    dirname		    as path_dirname,
    normpath		    as path_norm,
    abspath		    as path_xform_to_absolute,
    commonprefix	    as path_calc_common_prefix,
    expanduser		    as path_expanduser,
)
import platform
import site
import functools
import re


from utilia import (
    Error_WithReason,
)
from . import (
    Error_BASE		    as FilesystemError_BASE,
)


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
	:type error_on_none: boolean
    """,
	"software_name": \
    """
	:param software_name: Consider the name of this software product when
			      constructing a path fragment which identifies 
			      it.
	:type software_name: string
    """,
	"vendor_name": \
    """
	:param vendor_name: Consider the name of this software vendor when 
			    constructing a path fragment which identifies a 
			    software product.
	:type vendor_name: string
    """,
	"version": \
    """
	:param version: Consider this version string when constructing a path
			fragment which identifies a software product.
	:type version: string
    """,
	"alt_base_path": \
    """
	:param alt_base_path: Calculate path, using this base path as a prefix
			      rather than deriving a base path to use as a
			      prefix.
	:type alt_base_path: string
    """,
	"prefer_common": \
    """
	:param prefer_common: If ``True``, the common path, if it exists, 
			      will be preferred over the user path.
	:type prefer_common: boolean
    """,
	"append_path_fragment": \
    """
	:param append_path_fragment: If ``True``, a concatenation of the names
				     of the software vendor and the software,
				     along with the software version, will be
				     injected into the calculated path.
	:type append_path_fragment: boolean
    """,
	"use_python_prefix": \
    """
	:param use_python_prefix: If ``True``, cause the path calculation to
				  attempt adherence to the Python file system
				  standard rather than the standard for the 
				  OS distribution.
	:type use_python_prefix: boolean
    """,
	"RTYPE_string_or_None": \
    """
	:rtype: string or ``None``
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


# TODO: Move to a different module.
def __autodoc_function_parameters( func, pdict ):
    """
	Automatically document a function's parameters, if
	the supplied dictionary has entries for their names.

	Note: This function assumes that the first entries of the 'co_varnames'
	tuple are the parameters passed on the stack.
    """

    for i in xrange( func.func_code.co_argcount ):
	docs = pdict.get( func.func_code.co_varnames[ i ], None )
	if docs: func.__doc__ += docs


def __TD( s ):
    """
	Dummy translator function.

	Passes its argument through without translation at runtime, 
	but allows it to be collected into a message catalog during a scan for
	translatable strings. This allows for an active runtime translator to
	translate the string when it is encountered as the contents of a
	variable.
    """

    return s


# Character Translators for Names
__whitespace_to_underscore  = functools.partial( re.sub, "\s+", "_" )
__dot_to_underscore	    = functools.partial( re.sub, "\.{1,1}", "_" )


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


# TODO: Return dictionary of values rather than simple string.
def which_fs_layout( ):
    """
	Returns a classification of the expected filesystem layout according 
	to the OS in use, if there is a classifier for that OS.

	The possible filesystem layout classifications are as follows:

	.. csv-table::
	   :header: "Classification", "Operating Systems"
	   :widths: 20, 80

	   "POSIX",	"Linux"
	   "MacOS X",	"Darwin"
	   "Windows",	"Windows"

	:rtype: string
	:raises: :py:class:`UnsupportedFilesystemLayout`, if there is no 
		 classifier implemented for the OS in use.
    """

    osa = platform.system( )

    if	 osa in [ "Linux", ]:
	return "POSIX"
    elif osa in [ "Darwin", ]:
	return "MacOS X"
    elif osa in [ "Windows", ]:
	return "Windows"
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented filesystem layout classifier for {0}.", osa
	)

__autodoc_function_parameters( which_fs_layout, __DOCSTRING_FRAGMENTS( ) )


def __computed_MacOS_X_python_prefix( prefix ):
    """
	If the Python prefix is for a MacOS X framework installation,
	then returns a truncated prefix, which can be used as a better base.
	Else, returns the prefix without alteration.
    """

    match = re.findall( r".*/Python\.framework/Versions/.*", prefix )
    if match:
	return reduce( lambda x, f: f( x ), [ path_dirname ] * 4, prefix )
    
    return prefix


def __computed_Windows_program_files_path( error_on_none = False ):
    """
	Returns the correct path to the "Program Files" directory, 
	depending on whether the OS is 32-bit or 64-bit and the running Python
	is 32-bit or 64-bit.
    """

    common_base_path	    = None
    error_reason_foramat    = None
    error_reason_args	    = [ ]
    evname		    = None

    if "64bit" in platform.architecture( ):
	if sys.maxsize > 2**32:	evname = "ProgramFiles"
	else:			evname = "ProgramFiles(x86)"
    else:			evname = "ProgramFiles"
    common_base_path = envvars.get( evname, None )

    if error_on_none and (None is common_base_path):
	error_reason_format = \
	__TD( "Environment variable, '{0}', not set." )
	error_reason_args = [ evname, ]
	raise UndeterminedFilesystemPath( 
	    error_reason_format, *error_reason_args
	)
    return common_base_path


def concatenated_software_path_fragment(
    software_name, vendor_name = None, version = None,
    error_on_none = False
):
    """
	Returns a concatenation of the name of a software product with an  
	optional name of the software product's vendor and an optional version 
	string for the software product as a filesystem path fragment typical
	of the operating system architecture.
    """

    # Note: Conversion of whitespaces to underscores is performed on POSIX
    #	    operating systems to facilitate command-line navigation. 
    #	    This is considered to be less important on the MacOS X and 
    #	    Windows operating systems, which ship with Finder and Explorer 
    #	    respectively.
    # Note: No conversion of decimal points to underscores is performed on
    #	    Windows operating systems, because directory names are being
    #	    returned rather than file names and so there are no concerns about
    #	    name extensions.
    
    path_fragment	    = None
    error_reason_foramat    = None
    error_reason_args	    = [ ]

    fsl = which_fs_layout( )

    if not software_name:
	error_reason_format = "Software name is unspecified."

    else:

	if vendor_name:
	    vendor_name = vendor_name.strip( )
	    if	 fsl in [ "POSIX", ]:
		vendor_name = __whitespace_to_underscore( vendor_name )
	    elif fsl in [ "MacOS X", ]:	pass
	    elif fsl in [ "Windows", ]:	pass
	    else:
		raise UnsupportedFilesystemLayout(
		    "Unimplemented path determination logic for {0}.", fsl
		)
	
	software_name = software_name.strip( )
	if   fsl in [ "POSIX", ]:
	    software_name = __whitespace_to_underscore( software_name )
	elif fsl in [ "MacOS X", ]: pass
	elif fsl in [ "Windows", ]: pass
	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )
	
	if version:
	    version = version.strip( )
	    if	 fsl in [ "POSIX", ]:
		version = __whitespace_to_underscore( version )
	    elif fsl in [ "MacOS X", ]:	pass
	    elif fsl in [ "Windows", ]:  pass
	    else:
		raise UnsupportedFilesystemLayout(
		    "Unimplemented path determination logic for {0}.", fsl
		)
	
	path_fragment = \
	path_join( *filter( None, [ vendor_name, software_name, version ] ) )

    if error_on_none and (None is path_fragment):
	raise UndeterminedFilesystemPath( 
	    error_reason_format, *error_reason_args
	)
    return path_fragment

__autodoc_function_parameters(
    concatenated_software_path_fragment, __DOCSTRING_FRAGMENTS( )
)
concatenated_software_path_fragment.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
concatenated_software_path_fragment.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_user_home( error_on_none = False ):
    """
	Returns the path to the current user's home directory, if it can be
	determined. Returns ``None``, otherwise.

    """

    user_id		    = None
    user_home_path	    = None
    error_reason_foramat    = None
    error_reason_args	    = [ ]

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", "MacOS X", ]:
	user_id		= envvars.get( "USER", None )
	user_home_path	= path_expanduser( "~" )
	if "~" == user_home_path: user_home_path = None
    elif fsl in [ "Windows", ]:
	user_id		= envvars.get( "UserName", None )
	user_home_path	= envvars.get( "UserProfile", None )
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)
    
    if (None is user_home_path) and error_on_none:
	if user_id:
	    error_reason_format	= \
	    __TD( "Unknown home directory for user '{0}'." )
	    error_reason_args	= [ user_id, ]
	else:
	    error_reason_format = __TD( "Unknown ID of current user." )
	raise UndeterminedFilesystemPath( 
	    error_reason_format, *error_reason_args
	)
    return user_home_path

__autodoc_function_parameters( whereis_user_home, __DOCSTRING_FRAGMENTS( ) )
whereis_user_home.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_user_home.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_common_temp_base( error_on_none = False ):
    """
	Returns the path to the temporary storage area available for use by
	everyone on the system.
	
	Below is a table of typical paths by filesystem layout classification:

	.. csv-table::
	   :header: "Classification", "Path"
	   :widths: 20, 80

	   "POSIX",	"/tmp"
	   "MacOS X",	"/tmp"
	   "Windows",	""

    """

    temp_base_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", "MacOS X" ]:	temp_base_path = "/tmp"
    elif fsl in [ "Windows", ]:		pass
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is temp_base_path) and error_on_none:
	error_reason_format = \
	__TD( "Unknown path to common temporary storage area." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return temp_base_path

__autodoc_function_parameters(
    whereis_common_temp_base, __DOCSTRING_FRAGMENTS( )
)
whereis_common_temp_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_common_temp_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_user_temp_base( error_on_none = False ):
    """
	Returns the path to the current user's temporary storage area.

    """

    utbp_evname		= None
    user_temp_base_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", "MacOS X", ]:    pass
    elif fsl in [ "Windows", ]:
	utbp_evname = "Temp"
	user_temp_base_path = envvars.get( utbp_evname, None )
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is user_temp_base_path) and error_on_none:
	if utbp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ utbp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Unknown path to user's temporary storage area." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return user_temp_base_path

__autodoc_function_parameters(
    whereis_user_temp_base, __DOCSTRING_FRAGMENTS( )
)
whereis_user_temp_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_user_temp_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


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

    temp_base_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]

    utbp = stbp = None

    try: utbp = whereis_user_temp_base( error_on_none = error_on_none )
    except UndeterminedFilesystemPath as exc:
	error_reason_format = exc.error_reason_format
	error_reason_args   = exc.error_reason_args 

    try: stbp = whereis_common_temp_base( error_on_none = error_on_none )
    except UndeterminedFilesystemPath as exc:
	error_reason_format = exc.error_reason_format
	error_reason_args   = exc.error_reason_args 

    if	 stbp and prefer_common:    temp_base_path = stbp
    elif utbp:			    temp_base_path = utbp
    elif stbp:			    temp_base_path = stbp
    
    if (None is temp_base_path) and error_on_none:
	error_reason_format = \
	__TD( "Unknown path to preferred temporary storage." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return temp_base_path

__autodoc_function_parameters(
    whereis_preferred_temp_base, __DOCSTRING_FRAGMENTS( )
)
whereis_preferred_temp_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_preferred_temp_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


def whereis_my_temp(
    software_name, vendor_name = None, version = None,
    alt_base_path = None,
    prefer_common = False, append_path_fragment = True,
    error_on_none = False
):
    """
	Returns the path to the preferred temporary storage for the software
	specified by the ``software_name`` argument, if supplied, or else the
	:envvar:`UTILIA_SOFTWARE_NAME` environment variable, if set. Returns
	``None``, otherwise.

	The path calculation relies on results from the
	:py:func:`whereis_preferred_temp_base` and the 
	:py:func:`concatenated_software_path_fragment` functions.

    """

    temp_path		= None
    error_reason_format	= None
    error_reason_args	= [ ]

    if append_path_fragment:
	mtpf = \
	concatenated_software_path_fragment(
	    software_name   = software_name,
	    vendor_name	    = vendor_name,
	    version	    = version,
	    error_on_none   = error_on_none
	)
    else: mtpf = ""

    ptbp = alt_base_path
    if not ptbp:
	ptbp = \
	whereis_preferred_temp_base(
	    error_on_none = error_on_none,
	    prefer_common = prefer_common
	)
    if ptbp: temp_path = path_join( *filter( None, [ ptbp, mtpf ] ) )
    
    if (None is temp_path) and error_on_none:
	error_reason_format = \
	__TD( "Unknown path to temporary storage for '{0}'." )
	error_reason_args = [ software_name, ]
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return temp_path

__autodoc_function_parameters(
    whereis_my_temp, __DOCSTRING_FRAGMENTS( )
)
whereis_my_temp.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_temp.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


def whereis_my_site_config(
    software_name, vendor_name = None, version = None,
    alt_base_path = None, use_python_prefix = False,
    append_path_fragment = True,
    error_on_none = False
):
    """
	Returns a path to shared or site-wide configuration information 
	or preferences directory for the software product named by the
	``software_name`` argument.

    """

    my_site_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]
    fsl			= which_fs_layout( )
    msbp		= None
    msbp_evname		= None

    if append_path_fragment:
	mspf = \
	concatenated_software_path_fragment(
	    software_name   = software_name,
	    vendor_name	    = vendor_name,
	    version	    = version,
	    error_on_none   = error_on_none
	)
    else: mspf = ""

    if not msbp: msbp = alt_base_path
    if not msbp and use_python_prefix: msbp = sys.prefix
    if not msbp:
	if   fsl in [ "POSIX", ]:   msbp = "/usr/local"
	elif fsl in [ "MacOS X", ]: msbp = "/Library"
	elif fsl in [ "Windows", ]:
	    msbp = \
	    __computed_Windows_program_files_path(
		error_on_none = error_on_none
	    )
	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )

    if msbp:

	if   fsl in [ "POSIX", ]:
	    if "/usr" == msbp: msbp = "/"
	    my_site_path = \
	    path_join( *filter( None, [ msbp, "etc", mspf ] ) )

	elif fsl in [ "MacOS X", ]:
	    msbp_orig = msbp
	    msbp = __computed_MacOS_X_python_prefix( msbp )
	    if msbp.startswith( "/System" ): msbp = "/Library"
	    # MacOS X-flavored
	    if (mscbp_orig != msbp) or ("/Library" == msbp):
		my_site_path = \
		path_join( *filter( None, [ msbp, "Preferences", mspf ] ) )
	    # POSIX-flavored
	    else:
		my_site_path = \
		path_join( *filter( None, [ msbp, "etc", mspf ] ) )

	elif fsl in [ "Windows", ]:
	    # Python-flavored
	    if	 msbp == sys.prefix:
		my_site_path = \
		path_join( *filter( None, [ msbp, "Config", mspf ] ) )
	    # Windows-flavored
	    else:
		my_site_path = \
		path_join( *filter( None, [ msbp, mspf, "Config" ] ) )

	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )

    if (None is my_site_path) and error_on_none:
	if msbp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ msbp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Unknown path to site config info for '{0}'." )
	    error_reason_args = [ software_name, ]
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return my_site_path

__autodoc_function_parameters(
    whereis_my_site_config, __DOCSTRING_FRAGMENTS( )
)
whereis_my_site_config.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_site_config.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


def whereis_my_site_data(
    software_name, vendor_name = None, version = None,
    alt_base_path = None, use_python_prefix = False,
    append_path_fragment = True,
    error_on_none = False
):
    """
	Returns a path to the shared or site-wide data store or resources 
	directory for the software product named by the ``software_name`` 
	argument.

    """

    my_site_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]
    fsl			= which_fs_layout( )
    msbp		= None
    msbp_evname		= None

    if append_path_fragment:
	mspf = \
	concatenated_software_path_fragment(
	    software_name   = software_name,
	    vendor_name	    = vendor_name,
	    version	    = version,
	    error_on_none   = error_on_none
	)
    else: mspf = ""

    if not msbp: msbp = alt_base_path
    if not msbp and use_python_prefix: msbp = sys.prefix
    if not msbp:
	if   fsl in [ "POSIX", ]:   msbp = "/usr/local"
	elif fsl in [ "MacOS X", ]: msbp = "/Library"
	elif fsl in [ "Windows", ]:
	    msbp = \
	    __computed_Windows_program_files_path(
		error_on_none = error_on_none 
	    )
	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )

    if msbp:

	if   fsl in [ "POSIX", ]:
	    if "/" == msbp:
		my_site_path = \
		path_join( *filter( None, [ msbp, "etc", mspf ] ) )
	    else:
		my_site_path = \
		path_join( *filter( None, [ msbp, "share", mspf ] ) )

	elif fsl in [ "MacOS X", ]:
	    msbp_orig = msbp
	    msbp = __computed_MacOS_X_python_prefix( msbp )
	    if msbp.startswith( "/System" ): msbp = "/Library"
	    # MacOS X-flavored
	    if (msbp_orig != msbp) or ("/Library" == msbp):
		my_site_path = \
		path_join( *filter(
		    None,
		    [ msbp, "Application Support", mspf ]
		) )
	    # POSIX-flavored
	    else:
		if "/" == msbp:
		    my_site_path = \
		    path_join( *filter( None, [ msbp, "etc", mspf ] ) )
		else:
		    my_site_path = \
		    path_join( *filter( None, [ msbp, "share", mspf ] ) )

	elif fsl in [ "Windows", ]:
	    # Python-flavored
	    if	 msbp == sys.prefix:
		my_site_path = \
		path_join( *filter( None, [ msbp, "Data", mspf ] ) )
	    # Windows-flavored
	    else:
		my_site_path = \
		path_join( *filter( None, [ msbp, mspf, "Data" ] ) )

	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )

    if (None is my_site_path) and error_on_none:
	if msbp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ msbp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Unknown path to site data store for '{0}'." )
	    error_reason_args = [ software_name, ]
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return my_site_path

__autodoc_function_parameters(
    whereis_my_site_data, __DOCSTRING_FRAGMENTS( )
)
whereis_my_site_data.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_site_data.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


# TODO: whereis_my_site_programs
# TODO: whereis_my_site_docs


def whereis_my_user_config(
    software_name, vendor_name = None, version = None,
    alt_base_path = None, use_python_prefix = False,
    append_path_fragment = True,
    error_on_none = False
):
    """
	Returns a path to the user's configuration information or preferences
	directory for the software product named by the ``software_name`` 
	argument.

    """

    my_user_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]
    fsl			= which_fs_layout( )
    mubp		= None
    mubp_evname		= None

    if append_path_fragment:
	mupf = \
	concatenated_software_path_fragment(
	    software_name   = software_name,
	    vendor_name	    = vendor_name,
	    version	    = version,
	    error_on_none   = error_on_none
	)
    else: mupf = ""

    if not mubp: mubp = alt_base_path
    if not mubp and use_python_prefix: mubp = site.USER_BASE
    if not mubp:
	if   fsl in [ "POSIX", ]:
	    mubp = whereis_user_home( error_on_none = error_on_none )
	elif fsl in [ "MacOS X", ]:
	    uhp = whereis_user_home( error_on_none = error_on_none )
	    if uhp:
		# MacOS X-flavored
		if  sys.prefix \
		    != __computed_MacOS_X_python_prefix( sys.prefix ):
		    mubp = path_join( uhp, "Library" )
		# POSIX-flavored
		else: mubp = uhp
	elif fsl in [ "Windows", ]:
	    mubp_evname = "AppData"
	    mubp = envvars.get( mubp_evname, None )
	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )

    if mubp:

	if   fsl in [ "POSIX", ]:
	    if use_python_prefix:
		# NOTE: Possible PEP 370 violation.
		my_user_path = \
		path_join( *filter( None, [ mubp, "etc", mupf ] ) )
	    else:
		if not mupf: mupf = software_name
		my_user_path = \
		path_join( *filter( None, [ mubp, "." + mupf, "etc" ] ) )
	
	elif fsl in [ "MacOS X", ]:
	    # MacOS X-flavored
	    if  sys.prefix \
		!= __computed_MacOS_X_python_prefix( sys.prefix ):
		my_user_path = \
		path_join( *filter( None, [ mubp, "Preferences", mupf ] ) )
	    # POSIX-flavored
	    else:
		if use_python_prefix:
		    # NOTE: Possible PEP 370 violation.
		    my_user_path = \
		    path_join( *filter( None, [ mubp, "etc", mupf ] ) )
		else:
		    if not mupf: mupf = software_name
		    my_user_path = \
		    path_join( *filter( None, [ mubp, "." + mupf, "etc" ] ) )
	
	elif fsl in [ "Windows", ]:
	    if use_python_prefix:
		my_user_path = \
		path_join( *filter( None, [ mubp, "Config", mupf ] ) )
	    else:
		if not mupf: mupf = software_name
		my_user_path = \
		path_join( *filter( None, [ mubp, mupf, "Config" ] ) )

	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )

    if (None is my_user_path) and error_on_none:
	if mubp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ mubp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Unknown path to user config info for '{0}'." )
	    error_reason_args = [ software_name, ]
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return my_user_path

__autodoc_function_parameters(
    whereis_my_user_config, __DOCSTRING_FRAGMENTS( )
)
whereis_my_user_config.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_user_config.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


def whereis_my_user_data(
    software_name, vendor_name = None, version = None,
    alt_base_path = None, use_python_prefix = False,
    append_path_fragment = True,
    error_on_none = False
):
    """
	Returns a path to the user's resources or data store directory 
	for the software product named by the ``software_name`` argument.

    """

    my_user_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]
    fsl			= which_fs_layout( )
    mubp		= None
    mubp_evname		= None

    if append_path_fragment:
	mupf = \
	concatenated_software_path_fragment(
	    software_name   = software_name,
	    vendor_name	    = vendor_name,
	    version	    = version,
	    error_on_none   = error_on_none
	)
    else: mupf = ""

    if not mubp: mubp = alt_base_path
    if not mubp and use_python_prefix: mubp = site.getuserbase( )
    if not mubp:
	if   fsl in [ "POSIX", ]:
	    mubp = whereis_user_home( error_on_none = error_on_none )
	elif fsl in [ "MacOS X", ]:
	    uhp = whereis_user_home( error_on_none = error_on_none )
	    if uhp:
		# MacOS X-flavored
		if  sys.prefix \
		    != __computed_MacOS_X_python_prefix( sys.prefix ):
		    mubp = path_join( uhp, "Library" )
		# POSIX-flavored
		else: mubp = uhp
	elif fsl in [ "Windows", ]:
	    mubp_evname = "AppData"
	    mubp = envvars.get( mubp_evname, None )
	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )

    if mubp:

	if   fsl in [ "POSIX", ]:
	    if use_python_prefix:
		# NOTE: Possible PEP 370 violation.
		my_user_path = \
		path_join( *filter( None, [ mubp, "share", mupf ] ) )
	    else:
		if not mupf: mupf = software_name
		my_user_path = \
		path_join( *filter( None, [ mubp, "." + mupf, "share" ] ) )
	
	elif fsl in [ "MacOS X", ]:
	    # MacOS X-flavored
	    if  sys.prefix \
		!= __computed_MacOS_X_python_prefix( sys.prefix ):
		my_user_path = \
		path_join( *filter(
		    None,
		    [ mubp, "Application Support", mupf ]
		) )
	    # POSIX-flavored
	    else:
		if use_python_prefix:
		    # NOTE: Possible PEP 370 violation.
		    my_user_path = \
		    path_join( *filter( None, [ mubp, "share", mupf ] ) )
		else:
		    if not mupf: mupf = software_name
		    my_user_path = \
		    path_join( *filter( None, [ mubp, "." + mupf, "share" ] ) )
	
	elif fsl in [ "Windows", ]:
	    if use_python_prefix:
		my_user_path = \
		path_join( *filter( None, [ mubp, "Data", mupf ] ) )
	    else:
		if not mupf: mupf = software_name
		my_user_path = \
		path_join( *filter( None, [ mubp, mupf, "Data" ] ) )

	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )

    if (None is my_user_path) and error_on_none:
	if mubp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ mubp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Unknown path to user data store for '{0}'." )
	    error_reason_args = [ software_name, ]
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return my_user_path

__autodoc_function_parameters(
    whereis_my_user_data, __DOCSTRING_FRAGMENTS( )
)
whereis_my_user_data.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_user_data.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


# TODO: whereis_my_user_docs


def whereis_my_saves(
    software_name, vendor_name = None, version = None,
    alt_base_path = None, 
    append_path_fragment = True,
    error_on_none = False
):
    """
	Returns a path to the directory where works, created by the user of the
	software product, named by the ``software_name`` argument, will be
	stored.

    """

    my_saves_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]
    fsl			= which_fs_layout( )
    mdbp		= None
    mdbp_evname		= None

    if append_path_fragment:
	mdpf = \
	concatenated_software_path_fragment(
	    software_name   = software_name,
	    vendor_name	    = vendor_name,
	    version	    = version,
	    error_on_none   = error_on_none
	)
    else: mdpf = ""

    if not mdbp: mdbp = alt_base_path
    if not mdbp:
	if   fsl in [ "POSIX", "MacOS X", "Windows", ]:
	    mdbp = whereis_user_home( error_on_none = error_on_none )
	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )
    
    if mdbp:

	if   fsl in [ "POSIX", ]:
	    if not mdpf: mdpf = software_name
	    my_saves_path = \
	    path_join( *filter( None, [ mdbp, "." + mdpf, "saves" ] ) )
	
	elif fsl in [ "MacOS X", "Windows", ]:
	    my_saves_path = \
	    path_join( *filter( None, [ mdbp, "Documents", mdpf ] ) )

	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl
	    )

    if (None is my_saves_path) and error_on_none:
	if mdbp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ mdbp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Unknown path to saves directory for '{0}'." )
	    error_reason_args = [ software_name, ]
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return my_saves_path

__autodoc_function_parameters(
    whereis_my_saves, __DOCSTRING_FRAGMENTS( )
)
whereis_my_saves.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_saves.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


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

	   "POSIX",	"/"
	   "MacOS X",	"/"
	   "Windows",	"C:\\\\Windows\\\\System32"
	
    """

    irp_evname		= None
    install_root_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]

    fsl = which_fs_layout( )
    if	 fsl in [ "POSIX", "MacOS X", ]:
	install_root_path = "/"
    elif fsl in [ "Windows", ]:
	irp_evname = "SystemRoot"
	install_root_path = envvars.get( irp_evname, None )
	if install_root_path:
	    install_root_path = path_join( install_root_path, "System32" )
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is install_root_path) and error_on_none:
	if irp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ irp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Undetermined system installation root." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return install_root_path

__autodoc_function_parameters( 
    whereis_oscore_install_root, __DOCSTRING_FRAGMENTS( )
)
whereis_oscore_install_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_oscore_install_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


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

	   "POSIX",	"/usr"
	   "MacOS X",	"/System"
	   "Windows",	"C:\\\\Windows"
	
    """

    irp_evname		= None
    install_root_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]

    fsl = which_fs_layout( )
    if	 fsl in [ "POSIX", ]:	install_root_path = "/usr"
    elif fsl in [ "MacOS X", ]:	install_root_path = "/System"
    elif fsl in [ "Windows", ]:
	irp_evname = "SystemRoot"
	install_root_path = envvars.get( irp_evname, None )
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is install_root_path) and error_on_none:
	if irp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ irp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Undetermined system installation root." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return install_root_path

__autodoc_function_parameters( 
    whereis_osdist_install_root, __DOCSTRING_FRAGMENTS( )
)
whereis_osdist_install_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_osdist_install_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


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

	   "POSIX",	"/usr/local"
	   "MacOS",	""
	   "Windows",	"C:\\\\Program Files"
	
    """

    irp_evname		= None
    install_root_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]

    fsl = which_fs_layout( )
    if	 "POSIX" == fsl:    install_root_path = "/usr/local"
    elif "MacOS X" == fsl:  pass
    elif "Windows" == fsl:
	install_root_path = \
	__computed_Windows_program_files_path( error_on_none = error_on_none )
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is install_root_path) and error_on_none:
	if irp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ irp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Undetermined common installation root." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return install_root_path

__autodoc_function_parameters( 
    whereis_common_install_root, __DOCSTRING_FRAGMENTS( )
)
whereis_common_install_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_common_install_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_oscore_config_base( error_on_none = False ):
    """
	Returns the path to the typical top-level directory under which the
	configuration information resides for the core OS components, 
	if it can be determined. Returns ``None``, otherwise.
	
	Below is a table of typical paths by filesystem layout classification:

	.. csv-table::
	   :header: "Classification", "Path"
	   :widths: 20, 80

	   "POSIX",	"/etc"
	   "MacOS X",	"/System/Preferences"
	   "Windows",	"C:\\\\Windows\\\\System32\\\\Config"

    """

    cbp_evname		= None
    config_base_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", ]:	config_base_path = "/etc"
    elif fsl in [ "MacOS X", ]:	config_base_path = "/System/Preferences"
    elif fsl in [ "Windows", ]:
	cbp_evname = "SystemRoot"
	config_base_path = envvars.get( cbp_evname, None )
	if config_base_path:
	    config_base_path = \
	    path_join( config_base_path, "System32", "Config"  )
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is config_base_path) and error_on_none:
	if cbp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ cbp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Unknown path to OS core config info." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return config_base_path

__autodoc_function_parameters(
    whereis_oscore_config_base, __DOCSTRING_FRAGMENTS( )
)
whereis_oscore_config_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_oscore_config_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_osdist_config_base( error_on_none = False ):
    """
	Returns the path to the typical top-level directory under which the
	configuration information resides for the core OS components, 
	if it can be determined. Returns ``None``, otherwise.
	
	Below is a table of typical paths by filesystem layout classification:

	.. csv-table::
	   :header: "Classification", "Path"
	   :widths: 20, 80

	   "POSIX",	"/etc"
	   "MacOS X",	"/System/Preferences"
	   "Windows",	""

    """

    cbp_evname		= None
    config_base_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", ]:	config_base_path = "/etc"
    elif fsl in [ "MacOS X", ]:	config_base_path = "/System/Preferences"
    elif fsl in [ "Windows", ]:	pass
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is config_base_path) and error_on_none:
	if cbp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ cbp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Unknown path to OS distribution config info." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return config_base_path

__autodoc_function_parameters(
    whereis_osdist_config_base, __DOCSTRING_FRAGMENTS( )
)
whereis_osdist_config_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_osdist_config_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


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

	   "POSIX",	"/usr/local/etc"
	   "MacOS X",	"/Library/Preferences"
	   "Windows",	""

    """

    cbp_evname		= None
    config_base_path	= None
    error_reason_format	= None
    error_reason_args	= [ ]

    fsl = which_fs_layout( )
    if   fsl in [ "POSIX", ]:	config_base_path = "/usr/local/etc"
    elif fsl in [ "MacOS X", ]:	config_base_path = "/Library/Preferences"
    elif fsl in [ "Windows", ]: pass
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is config_base_path) and error_on_none:
	if cbp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{0}', not set." )
	    error_reason_args = [ cbp_evname, ]
	else:
	    error_reason_format = \
	    __TD( "Unknown path to common config info." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return config_base_path

__autodoc_function_parameters(
    whereis_common_config_base, __DOCSTRING_FRAGMENTS( )
)
whereis_common_config_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_common_config_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


###############################################################################
# vim: set ft=python sts=4 sw=4 tw=79:					      #

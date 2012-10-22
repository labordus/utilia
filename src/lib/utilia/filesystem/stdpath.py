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

    The functions contained in this module following a regular naming
    convention, which provides hints as to their function. This convention can
    be expressed as follows.
    
    * Functions, which return paths relative to the current user's home 
      directory, have the word **user** in them.
    
    * Functions, which return paths associated with where the OS
      distribution typically find files, have the word **system** in them.

    * Functions, which return paths associated with the default locations 
      where a superuser or systems adminstrator would install software not 
      packaged as part of the OS distribution, have the word **common** in them.
    
    * Functions, which return paths associated with the location of a 
      particular piece of software, have the word **my** in them. 
    
    * The suffix **install_root** denotes that a returned path refers to a 
      top-level directory under which other directories for things, such as 
      configuration information and data stores, can be found.

    * The suffix **base** denotes that a returned path refers to an upper-level
      directory of a certain flavor, such as for configuration information or 
      data stores, which is potentially common to many pieces of software 
      and not tied to a particular one.

    * Functions, which return paths which are either associated with an active
      development root for a particular piece of software or, failing that, 
      associated with an installation root for a particular piece of software,
      have the word **site** in them.

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
from platform import (
    system		    as which_os,
)


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
	:param software_name: Calculate path, using this name to provide
			      guidance. Note that this overrides the
			      :envvar:`UTILIA_SOFTWARE_NAME` environment
			      variable in any calculations.
	:type software_name: string
    """,
	"ignore_env": \
    """
	:param ignore_env: If ``True``, ignore relevant environment variables 
			   during calculation of the path.
	:type ignore_env: boolean
    """,
	"alt_base_path": \
    """
	:param alt_base_path: Calculate path, using this base path as a prefix
			      rather than deriving a base path to use as a
			      prefix.
	:type alt_base_path: string
    """,
	"with_version": \
    """
	:param with_version: Calculate path with this version injected into it.
	:type with_version: string
    """,
	"prefer_common": \
    """
	:param prefer_common: If ``True``, the common path, if it exists, 
			      will be preferred over the user path.
	:type prefer_common: boolean
    """,
	"search_heuristics": \
    """
	:param search_heuristics: Search for path roots using the heuristics
				  named in this list. The following names of
				  heuristics may appear in the list:
				  
				  * "script_path": Search up the directory
				    hierarchy for the nearest containing 
				    directory, named ``bin`` or ``scripts``,
				    case-insensitively, starting from the path
				    to the currently executing script. Sets the
				    search result to the parent directory of 
				    this directory, if found.

				  * "module_path": Search up the directory
				    hierarchy for the nearest containing
				    directory, named ``lib``,
				    case-insensitively, starting from the path
				    to the specified module, if determined. 
				    Sets the search result to the parent 
				    directory of this directory, if found.

				  * "common_path": Sets the search result to 
				    the result of a call to
				    :py:func:`whereis_common_install_root`. 

				  * "system_path": Sets the search result to 
				    the result of a call to
				    :py:func:`whereis_system_install_root`. 

	:type search_heuristics: list of strings
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


def __SEARCH_HEURISTICS_DEFAULT( ):
    """
	Returns list of default search heuristics to use.
    """

    return [ "script_path", "module_path", ]


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


def which_fs_layout( ):
    """
	Returns a classification of the expected filesystem layout according 
	to the OS in use, if there is a classifier for that OS.

	The possible filesystem layout classifications are as follows:

	.. csv-table::
	   :header: "Classification", "Operating Systems"
	   :widths: 20, 80

	   "POSIX", "Linux"

	:rtype: string
	:raises: :py:class:`UnsupportedFilesystemLayout`, if there is no 
		 classifier implemented for the OS in use.
    """

    osa = which_os( )

    if	 osa in [ "Linux", ]:
	return "POSIX"
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented filesystem layout classifier for {0}.", osa
	)

__autodoc_function_parameters( which_fs_layout, __DOCSTRING_FRAGMENTS( ) )


def whereis_user_home( error_on_none = False ):
    """
	Returns the path to the current user's home directory, if it can be
	determined. Returns ``None``, otherwise.

    """

    user_id		    = None
    user_home_path	    = None
    error_reason_foramat    = None
    error_reason_args	    = ( )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl:
	user_id		= envvars.get( "USER", None )
	user_home_path	= path_expanduser( "~" )
	if "~" == user_home_path: user_home_path = None
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)
    
    if (None is user_home_path) and error_on_none:
	if user_id:
	    error_reason_format	= __TD( "No home directory for user '{0}'." )
	    error_reason_args	= tuple( user_id )
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


def whereis_system_install_root( error_on_none = False ):
    """
	Returns the path to the installation root of the OS distribution, if it
	can be determined. Returns ``None``, otherwise.

	Environment variables or API calls may help determine this path on
	certain operating systems. In other cases, this path is fixed.
	
	Below is a table of typical paths by filesystem layout classification:

	.. csv-table::
	   :header: "Classification", "Path"
	   :widths: 20, 80

	   "POSIX", "/usr"
	
    """

    irp_evname			= None
    install_root_path		= None
    error_reason_format		= None
    error_reason_args		= ( )

    fsl = which_fs_layout( )
    if	 "POSIX" == fsl:
	install_root_path = "/usr"
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is install_root_path) and error_on_none:
	if irp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{1}', not set." )
	    error_reason_args = tuple( irp_evname )
	else:
	    error_reason_format = \
	    __TD( "Undetermined system installation root." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return install_root_path

__autodoc_function_parameters( 
    whereis_system_install_root, __DOCSTRING_FRAGMENTS( )
)
whereis_system_install_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_system_install_root.__doc__ += \
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

	   "POSIX", "/usr/local"
	
    """

    irp_evname			= None
    install_root_path	= None
    error_reason_format		= None
    error_reason_args		= ( )

    fsl = which_fs_layout( )
    if	 "POSIX" == fsl:
	install_root_path = "/usr/local"
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is install_root_path) and error_on_none:
	if irp_evname:
	    error_reason_format = \
	    __TD( "Environment variable, '{1}', not set." )
	    error_reason_args = tuple( irp_evname )
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


def __search_heuristic_script_path( script_path ):
    """
	Returns a path to the installation root as derived from the supplied
	path to a script file.
    """

    install_root_path  = None
    error_reason_format	    = None
    error_reason_args	    = ( )

    if not script_path:
	error_reason_format = \
	__TD( "Empty argument for 'script_path' search heuristic." )
	return ( None, error_reason_format, error_reason_args ) 

    sp = path_xform_to_absolute( path_norm( script_path ) )
    
    # If script is installed with Python interpreter,
    # then return the Python installation prefix.
    if sys.prefix == path_calc_common_prefix( sys.prefix, sp ):
	install_root_path = sys.prefix

    # If script is installed separately, 
    # then strip off all path elements back to and including 
    # nearest 'bin' or 'scripts' element. If neither of these elements
    # is present, then give up this search.
    else:
	
	# TODO: Factor path search-up logic into a separate function to be
	#	called from here.
	suffix_bin	= path_dirsep + "bin"
	suffix_scripts	= path_dirsep + "scripts"
	while	sp \
	    and (not sp.lower( ).endswith( suffix_bin )) \
	    and (not sp.lower( ).endswith( suffix_scripts )):
	    sp = path_dirname( sp )

	if sp: install_root_path = path_dirname( sp )
	else:
	    error_reason_format = \
	    __TD( "No path from 'script_path' search heuristic." )

    return ( install_root_path, error_reason_format, error_reason_args )


def __search_heuristic_module_path( module_name ):
    """
	Returns a path to the installation root as derived from the supplied
	path to a script file.
    """

    import imp

    install_root_path  = None
    error_reason_format	    = None
    error_reason_args	    = ( )

    if not module_name:
	error_reason_format = \
	__TD( "Empty argument for 'module_path' search heuristic." )
	return ( None, error_reason_format, error_reason_args )
    
    # Attempt to locate module by the given name.
    f, mp, desc = ( None, ) * 3
    try: ( f, mp, desc ) = imp.find_module( module_name )
    except ImportError: pass

    # If special module found,
    # then use installation root of Python interpreter.
    if	 (not mp) and (not None is desc):
	install_root_path = sys.prefix

    # If module found, 
    # then determine installation root from its path.
    elif mp:
	mp = path_xform_to_absolute( path_norm( mp ) )
	
	# If module is installed with Python interpreter,
	# then return the Python installation prefix.
	if sys.prefix == path_calc_common_prefix( sys.prefix, msp ):
	    install_root_path = sys.prefix

	# If module is installed separately, 
	# then strip off all path elements back to and including 
	# nearest 'lib' element. If no 'lib' element is present, then
	# give up this search.
	else:
	    
	    # TODO: Factor path search-up logic into a separate function to be
	    #	    called from here.
	    suffix = path_dirsep + "lib"
	    while mp and (not mp.lower( ).endswith( suffix )):
		mp = path_dirname( mp )

	    if mp: install_root_path = path_dirname( mp )
	    else:
		error_reason_format = \
		__TD( "No path from 'module_path' search heuristic." )

    else:
	error_reason_format = \
	__TD(
	    "No module, named '{0}', found for 'module_path' "
	    "search heuristic."
	)
	error_reason_args = tuple( module_name )

    return ( install_root_path, error_reason_format, error_reason_args )


def whereis_my_install_root(
    error_on_none = False,
    software_name = None,
    ignore_env = False,
    search_heuristics = __SEARCH_HEURISTICS_DEFAULT( )
):
    """
	Returns:
	
	* ``sys.prefix``, if the ``software_name`` argument is ``None`` and the
	  :envvar:`UTILIA_SOFTWARE_NAME` environment variable is unset;
	
	* the value of the :envvar:`software_name_INSTALL_PATH` environment
	  variable, if it set and either the ``software_name`` argument is not
	  ``None`` or the :envvar:`UTILIA_SOFTWARE_NAME` environment variable 
	  is set;
	
	* a path as determined by the available search heuristics, selected via
	  the ``search_heuristics`` argument;
	
	* or ``None``, if all else fails.
	
	Search heuristics are evaluated in the order in which they are
	encountered in the list supplied as the ``search_heuristics`` argument.
	When a search heuristic produces a path, no further heuristics are
	tried. Heuristics, which require the name of a module, are provided 
	this name from the ``software_name`` argument, if it is not ``None``, 
	or the value of the :envvar:`UTILIA_SOFTWARE_NAME` environment 
	variable, if it is set.

    """

    install_root_path  = None
    error_reason_format	    = None
    error_reason_args	    = ( )
    
    if (not ignore_env) and (None is software_name):
	software_name = envvars.get( "UTILIA_SOFTWARE_NAME", None )
    if None is software_name: install_root_path = sys.prefix
    else:
	
	# Attempt to get installation root from environment, if desired.
	if not ignore_env:
	    evname = software_name.upper( ) + "_INSTALL_PATH"
	    install_root_path = envars.get( evname, None )
	    if None is install_root_path:
		error_reason_format = \
		__TD( "'{1}' environment variable is not set." )
		error_reason_args = tuple( evname )
	# If path not in environment, 
	# then perform search using various heuristics.

	for sh in search_heuristics:
	    
	    if not None is install_root_path: break

	    if	 "script_path" == sh:
		( 
		    install_root_path,
		    error_reason_format, error_reason_args
		) = __search_heuristic_script_path( sys.argv[ 0 ] )

	    elif "module_path" == sh:
		(
		    install_root_path,
		    error_reason_format, error_reason_args
		) = __search_heuristic_module_path( software_name )

	    elif "common_path" == sh:
		install_root_path = whereis_common_install_root( )
		if None is install_root_path:
		    error_reason_format = \
		    __TD( "No path from 'common_path' search heuristic." )

	    elif "system_path" == sh:
		install_root_path = whereis_system_install_root( )
		if None is install_root_path:
		    error_reason_format = \
		    __TD( "No path from 'system_path' search heuristic." )

	    else:
		# TODO: Replace with a translatable "bad argument" 
		#	internal error.
		assert False, "Unknown search heuristic, '{0}.".format( sh )

    if (None is install_root_path) and error_on_none:
	raise UndeterminedFilesystemPath( 
	    error_reason_format, *error_reason_args
	)
    return install_root_path

__autodoc_function_parameters( 
    whereis_my_install_root, __DOCSTRING_FRAGMENTS( )
)
whereis_my_install_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_install_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


def whereis_my_devel_root( ):
    """
	Returns the path to the top level of the software development tree, if
	the :envvar:`UTILIA_SOFTWARE_NAME` and
	:envvar:`software_name_DEVEL_PATH` environment variables have been set.
	Returns ``None``, otherwise.

    """
    
    devel_root_path = None
    
    usn = envvars.get( "UTILIA_SOFTWARE_NAME", None )
    if usn:
	devel_root_path = \
	envvars.get( usn.upper( ) + "_DEVEL_PATH", None )
    
    return devel_root_path

__autodoc_function_parameters(
    whereis_my_devel_root, __DOCSTRING_FRAGMENTS( )
)
whereis_my_devel_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]


def whereis_user_temp_base( error_on_none = False ):
    """
	Returns the path to the current user's temporary storage area.

    """

    user_temp_base_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl: pass
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is user_temp_base_path) and error_on_none:
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


def whereis_my_user_org_root(
    error_on_none = False,
    software_name = None,
    with_version = None,
    ignore_env = False
):
    """
	Returns the path to the current user's top level organizational
	directory for the software specified by the ``software_name``
	argument, if supplied, or else the :envvar:`UTILIA_SOFTWARE_NAME`
	environment variable, if set. Returns ``None``, otherwise. 

	The path calculation relies on results from the
	:py:func:`whereis_user_home` function.

    """

    user_org_root_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    usn = software_name
    if (not ignore_env) and (None is software_name):
	usn = envvars.get( "UTILIA_SOFTWARE_NAME", None )
    if usn:

	fsl = which_fs_layout( )
	if   "POSIX" == fsl:
	    home_path = whereis_user_home( error_on_none = error_on_none )
	    if home_path:
		user_org_root_path = path_join( home_path, "." + usn )
	else:
	    raise UnsupportedFilesystemLayout(
		"Unimplemented path determination logic for {0}.", fsl	
	    )

	if not None in [ user_org_root_path, with_version ]:
	    user_org_root_path = \
	    path_join( user_org_root_path, with_version )
    
    else:
	error_reason_format = \
	__TD(
	    "'UTILIA_SOFTWARE_NAME' environment variable is not set "
	    "and 'software_name' argument is not supplied."
	)

    if (None is user_org_root_path) and error_on_none:
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return user_org_root_path

__autodoc_function_parameters(
    whereis_my_user_org_root, __DOCSTRING_FRAGMENTS( )
)
whereis_my_user_org_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_user_org_root.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_my_user_config(
    error_on_none = False,
    software_name = None,
    with_version = None,
    ignore_env = False
):
    """
	Returns the path to the current user's configuration information 
	for the software specified by the ``software_name`` argument, 
	if supplied, or else the :envvar:`UTILIA_SOFTWARE_NAME`
	environment variable, if set. Returns ``None``, otherwise. 

	The path calculation relies on results from the
	:py:func:`whereis_my_user_org_root` function.

    """

    user_config_path	= None
    error_reason_format	= None
    error_reason_args	= ( )
    
    org_root_path = \
    whereis_my_user_org_root(
	error_on_none = error_on_none, 
	software_name = software_name,
	with_version = with_version,
	ignore_env = ignore_env
    )
    if org_root_path: user_config_path = path_join( org_root_path, "config" )
    
    if (None is user_config_path) and error_on_none:
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return user_config_path

__autodoc_function_parameters(
    whereis_my_user_config, __DOCSTRING_FRAGMENTS( )
)
whereis_my_user_config.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_user_config.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


def whereis_my_user_data(
    error_on_none = False,
    software_name = None,
    with_version = None,
    ignore_env = False
):
    """
	Returns the path to the current user's data repository 
	for the software specified by the ``software_name`` argument, 
	if supplied, or else the :envvar:`UTILIA_SOFTWARE_NAME`
	environment variable, if set. Returns ``None``, otherwise. 

	The path calculation relies on results from the
	:py:func:`whereis_my_user_org_root` function.

    """

    user_data_path	= None
    error_reason_format	= None
    error_reason_args	= ( )
    
    org_root_path = \
    whereis_my_user_org_root(
	error_on_none = error_on_none, 
	software_name = software_name,
	with_version = with_version,
	ignore_env = ignore_env
    )
    if org_root_path: user_data_path = path_join( org_root_path, "data" )
    
    if (None is user_data_path) and error_on_none:
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return user_data_path

__autodoc_function_parameters(
    whereis_my_user_data, __DOCSTRING_FRAGMENTS( )
)
whereis_my_user_data.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_user_data.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


def whereis_common_temp_base( error_on_none = False ):
    """
	Returns the path to the temporary storage area available for use by
	everyone on the system.
	
	Below is a table of typical paths by filesystem layout classification:

	.. csv-table::
	   :header: "Classification", "Path"
	   :widths: 20, 80

	   "POSIX", "/tmp"

    """

    temp_base_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl: temp_base_path = "/tmp"
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


def whereis_system_config_base( error_on_none = False ):
    """
	Returns the path to the typical top-level directory under which the
	configuration information resides for software installed as part of the
	OS distribution, if it can be determined. Returns ``None``, otherwise.
	
	Below is a table of typical paths by filesystem layout classification:

	.. csv-table::
	   :header: "Classification", "Path"
	   :widths: 20, 80

	   "POSIX", "/etc"

    """

    config_base_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl: config_base_path = "/etc"
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is config_base_path) and error_on_none:
	error_reason_format = \
	__TD( "Unknown path to system configuration information." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return config_base_path

__autodoc_function_parameters(
    whereis_system_config_base, __DOCSTRING_FRAGMENTS( )
)
whereis_system_config_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_system_config_base.__doc__ += \
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

	   "POSIX", "/etc"

    """

    config_base_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl: config_base_path = "/etc"
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is config_base_path) and error_on_none:
	error_reason_format = \
	__TD( "Unknown path to common configuration information." )
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


def whereis_my_install_config_base(
    error_on_none = False,
    software_name = None,
    ignore_env = False,
    search_heuristics = __SEARCH_HEURISTICS_DEFAULT( )
):
    """
	Returns the path to the public top-level directory under which the 
	configuration information for the shared portion of the software, 
	specified by the ``software_name`` argument, if supplied, or else the 
	:envvar:`UTILIA_SOFTWARE_NAME` environment variable, if set, resides.
	Returns ``None``, otherwise. 

	The path calculation relies on results from the
	:py:func:`whereis_my_install_root` function, and, in some cases,
	results from other functions, such as
	:py:func:`whereis_system_config_base`, 
	:py:func:`whereis_common_config_base`,
	:py:func:`whereis_system_install_root`, and
	:py:func:`whereis_common_install_root`.

    """
	
    config_base_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    irp = \
    whereis_my_install_root( 
	error_on_none = error_on_none,
	software_name = software_name,
	ignore_env = ignore_env,
	search_heuristics = search_heuristics
    )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl:
	if	irp \
	     == whereis_system_install_root(
		    error_on_none = error_on_none
		):
	    config_base_path = \
	    whereis_system_config_base( error_on_none = error_on_none )
	elif	irp \
	     == whereis_common_install_root(
		    error_on_none = error_on_none
		):
	    config_base_path = \
	    whereis_common_config_base( error_on_none = error_on_none )
	elif irp: config_base_path = path_join( irp, "etc" )

    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is config_base_path) and error_on_none:
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return config_base_path

__autodoc_function_parameters(
    whereis_my_install_config_base, __DOCSTRING_FRAGMENTS( )
)
whereis_my_install_config_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_install_config_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_system_data_base( error_on_none = False ):
    """
	Returns the path to the typical top-level directory under which the
	data store resides for software installed as part of the
	OS distribution, if it can be determined. Returns ``None``, otherwise.
	
	Below is a table of typical paths by filesystem layout classification:

	.. csv-table::
	   :header: "Classification", "Path"
	   :widths: 20, 80

	   "POSIX", "/usr/share"

    """

    data_base_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl: data_base_path = "/usr/share"
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is data_base_path) and error_on_none:
	error_reason_format = \
	__TD( "Unknown path to system data store." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return data_base_path

__autodoc_function_parameters(
    whereis_system_data_base, __DOCSTRING_FRAGMENTS( )
)
whereis_system_data_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_system_data_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_common_data_base( error_on_none = False ):
    """
	Returns the path to the typical top-level directory under which the
	data store resides for software installed by the
	superuser or systems administrator, if it can be determined. Returns
	``None``, otherwise.
	
	Below is a table of typical paths by filesystem layout classification:

	.. csv-table::
	   :header: "Classification", "Path"
	   :widths: 20, 80

	   "POSIX", "/usr/share"

    """

    data_base_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl: data_base_path = "/usr/share"
    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is data_base_path) and error_on_none:
	error_reason_format = \
	__TD( "Unknown path to common data store." )
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return data_base_path

__autodoc_function_parameters(
    whereis_common_data_base, __DOCSTRING_FRAGMENTS( )
)
whereis_common_data_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_common_data_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_my_install_data_base(
    error_on_none = False,
    software_name = None,
    ignore_env = False,
    search_heuristics = __SEARCH_HEURISTICS_DEFAULT( )
):
    """
	Returns the path to the public top-level directory under which the 
	data store for the shared portion of the software, 
	specified by the ``software_name`` argument, if supplied, or else the 
	:envvar:`UTILIA_SOFTWARE_NAME` environment variable, if set, resides.
	Returns ``None``, otherwise. 

	The path calculation relies on results from the
	:py:func:`whereis_my_install_root` function, and, in some cases,
	results from other functions, such as
	:py:func:`whereis_system_data_base`, 
	:py:func:`whereis_common_data_base`,
	:py:func:`whereis_system_install_root`, and
	:py:func:`whereis_common_install_root`.

    """

    data_base_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    irp = \
    whereis_my_install_root( 
	error_on_none = error_on_none,
	software_name = software_name,
	ignore_env = ignore_env,
	search_heuristics = search_heuristics
    )

    fsl = which_fs_layout( )
    if   "POSIX" == fsl:
	if   irp in \
	     [
		"/",
		whereis_system_install_root(
		    error_on_none = error_on_none
		),
	     ]:
	    data_base_path = \
	    whereis_system_data_base( error_on_none = error_on_none )
	elif	irp \
	     ==	whereis_common_install_root(
		    error_on_none = error_on_none
		):
	    data_base_path = \
	    whereis_common_data_base( error_on_none = error_on_none )
	elif irp: data_base_path = path_join( irp, "share" )

    else:
	raise UnsupportedFilesystemLayout(
	    "Unimplemented path determination logic for {0}.", fsl	
	)

    if (None is data_base_path) and error_on_none:
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return data_base_path

__autodoc_function_parameters(
    whereis_my_install_data_base, __DOCSTRING_FRAGMENTS( )
)
whereis_my_install_data_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_install_data_base.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Unsupported_and_Undetermined" ]


def whereis_my_site_config(
    error_on_none = False,
    alt_base_path = None,
    software_name = None,
    with_version = None,
    ignore_env = False,
    search_heuristics = __SEARCH_HEURISTICS_DEFAULT( )
):
    """
	Returns the path to the directory in which the public portion of the 
	software, specified by the ``software_name`` argument, if supplied, 
	or else the :envvar:`UTILIA_SOFTWARE_NAME` environment variable, 
	if set, would typically be installed by the superuser or systems
	administrator, if it can be determined. Returns ``None``, otherwise. 

	The path calculation relies on results from the
	:py:func:`whereis_my_devel_root` and
	:py:func:`whereis_my_install_config_base` functions. The
	development root path, if present, is preferred over the installation 
	base path.

    """

    site_config_path	= None
    error_reason_format	= None
    error_reason_args	= ( )
    
    devp = whereis_my_devel_root( )
    if devp: site_config_path = path_join( devp, "config" )
    else:

	if not None is alt_base_path: bp = alt_base_path
	else:
	    bp = \
	    whereis_my_install_config_base( 
		error_on_none = error_on_none,
		software_name = software_name,
		ignore_env = ignore_env,
		search_heuristics = search_heuristics
	    )
	if bp:

	    usn = software_name
	    if (not ignore_env) and (None is usn):
		usn = envvars.get( "UTILIA_SOFTWARE_NAME", None )
	    if usn:

		site_config_path = path_join( bp, usn )

		if not None is with_version:
		    site_config_path = \
		    path_join( site_config_path, with_version )

	    else:
		error_reason_format = \
		__TD(
		    "'UTILIA_SOFTWARE_NAME' environment variable is not set "
		    "and 'software_name' argument is not supplied."
		)

    if (None is site_config_path) and error_on_none:
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return site_config_path

__autodoc_function_parameters(
    whereis_my_site_config, __DOCSTRING_FRAGMENTS( )
)
whereis_my_site_config.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_site_config.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


def whereis_my_site_data(
    error_on_none = False,
    alt_base_path = None,
    software_name = None,
    with_version = None,
    ignore_env = False,
    search_heuristics = __SEARCH_HEURISTICS_DEFAULT( )
):
    """
	Returns the path to the directory in which the public portion of the 
	software, specified by the ``software_name`` argument, if supplied, 
	or else the :envvar:`UTILIA_SOFTWARE_NAME` environment variable, 
	if set, would typically be installed by the superuser or systems
	administrator, if it can be determined. Returns ``None``, otherwise. 

	The path calculation relies on results from the
	:py:func:`whereis_my_devel_root` and
	:py:func:`whereis_my_install_data_base` functions. The
	development root path, if present, is preferred over the installation 
	base path.

    """

    site_data_path	= None
    error_reason_format	= None
    error_reason_args	= ( )
    
    devp = whereis_devel_root( )
    if devp: site_data_path = path_join( devp, "data" )
    else:

	if not None is alt_base_path: bp = alt_base_path
	else:
	    bp = \
	    whereis_site_data_base( 
		error_on_none = error_on_none,
		software_name = software_name,
		ignore_env = ignore_env,
		search_heuristics = search_heuristics
	    )
	if bp:

	    usn = software_name
	    if (not ignore_env) and (None is usn):
		usn = envvars.get( "UTILIA_SOFTWARE_NAME", None )
	    if usn:
		
		site_data_path = path_join( bp, usn )

		if not None is with_version:
		    site_data_path = \
		    path_join( site_data_path, with_version )

	    else:
		error_reason_format = \
		__TD(
		    "'UTILIA_SOFTWARE_NAME' environment variable is not set "
		    "and 'software_name' argument is not supplied."
		)
    
    if (None is site_data_path) and error_on_none:
	raise UndeterminedFilesystemPath(
	    error_reason_format, *error_reason_args
	)
    return site_data_path

__autodoc_function_parameters(
    whereis_my_site_data, __DOCSTRING_FRAGMENTS( )
)
whereis_my_site_data.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RTYPE_string_or_None" ]
whereis_my_site_data.__doc__ += \
__DOCSTRING_FRAGMENTS( )[ "RAISES_Undetermined" ]


def whereis_preferred_temp_base(
    error_on_none = False,
    alt_base_path = None,
    prefer_common = False
):
    """
	Returns:

	* if the ``prefer_common`` argument is ``True``, the path provided by 
	  the ``alt_base_path`` argument, if it is not ``None``, 
	  or failing that, the result from a call to 
	  :py:func:`whereis_common_temp_base`, if it is not ``None``;
	
	* the result from a call to :py:func:`whereis_user_temp_base`, if it is
	  not ``None``;
	
	* the path provided by the ``alt_base_path`` argument, if it is not
	  ``None``, or failing that, the result from a call to
	  :py:func:`whereis_common_temp_base`, if it is not ``None``;
	
	* or ``None``, if all else fails.

    """

    temp_base_path	= None
    error_reason_format	= None
    error_reason_args	= ( )

    utbp = stbp = None

    try: utbp = whereis_user_temp_base( error_on_none = error_on_none )
    except UndeterminedFilesystemPath as exc:
	error_reason_format = exc.error_reason_format
	error_reason_args   = exc.error_reason_args 

    if not None is alt_base_path: stbp = alt_base_path
    else:
	try: stbp = whereis_common_temp_base( error_on_none = error_on_none )
	except UndeterminedFilesystemPath as exc:
	    error_reason_format = exc.error_reason_format
	    error_reason_args   = exc.error_reason_args 

    if	 stbp and prefer_common:    temp_base_path = stbp
    elif utbp:			    temp_base_path = utbp
    elif stbp:			    temp_base_path = stbp
    
    if (None is temp_base_path) and error_on_none:
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
    error_on_none = False,
    alt_base_path = None,
    software_name = None,
    with_version = None,
    ignore_env = False
):
    """
	Returns the path to the preferred temporary storage for the software
	specified by the ``software_name`` argument, if supplied, or else the
	:envvar:`UTILIA_SOFTWARE_NAME` environment variable, if set. Returns
	``None``, otherwise.

	The path calculation relies on results from the
	:py:func:`whereis_preferred_temp_base` function.

    """

    temp_path		= None
    error_reason_format	= None
    error_reason_args	= ( )

    ptbp = \
    whereis_preferred_temp_base(
	error_on_none = error_on_none,
	alt_base_path = alt_base_path,
	prefer_common = prefer_common
    )
    if ptbp:

	usn = software_name
	if (not ignore_env) and (None is usn):
	    usn = envvars.get( "UTILIA_SOFTWARE_NAME", None )
	if usn:
	
	    temp_path = path_join( ptbp, usn )

	    if not None is with_version:
		temp_path = path_join( temp_path, with_version )

	else:
	    error_reason_format = \
	    __TD(
		"'UTILIA_SOFTWARE_NAME' environment variable is not set "
		"and 'software_name' argument is not supplied."
	    )
    
    if (None is temp_path) and error_on_none:
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


###############################################################################
# vim: set ft=python sts=4 sw=4 tw=79:					      #

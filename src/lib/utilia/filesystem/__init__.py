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
    Provides various utilities pertaining to file systems. These modules
    provide uniform interfaces for querying information about and 
    manipulating various aspects of file systems, regardless of file system 
    type or operating system.

    The following modules provide calculated paths:

	* :py:mod:`.stdpath`
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division		    as __FUTURE_division,
    absolute_import	    as __FUTURE_absolute_import,
    print_function	    as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


from .. import (
    Exception_BASE	    as __super_Exception_BASE,
    Error_BASE		    as __super_Error_BASE,
)


# Exceptions


class Exception_BASE( __super_Exception_BASE ):
    """
	Base class for all :py:mod:`utilia` filesystem exceptions. Inherits 
	from :py:class:`utilia.Exception_BASE`.

	Use this for your exception handler signature if you wish to catch any
	filesystem-related exception raised from within :py:mod:`utilia`.
    """

    
    def __init__( self, *posargs ):
	"""
	    Invokes superclass initializers.
	"""

	super( Exception_BASE, self ).__init__( *posargs )


class Error_BASE( Exception_BASE, __super_Error_BASE ):
    """
	Base class for all :py:mod:`utilia` filesystem exceptions which are
	regarded as errors. Inherits from :py:class:`Exception_BASE` and 
	:py:class:`utilia.Error_BASE`.

	Use this for your exception handler signature if you wish to catch any
	filesystem-related error condition raised from within :py:mod:`utilia`.
    """


    def __init__( self, *posargs ):
	"""
	    Invokes superclass initializers.
	"""

	super( Error_BASE, self ).__init__( *posargs )


###############################################################################
# vim: set ft=python sts=4 sw=4 tw=79:					      #

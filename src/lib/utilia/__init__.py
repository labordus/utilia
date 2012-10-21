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
    Provides the following subpackages:

    * :py:mod:`.filesystem`
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division		    as __FUTURE_division,
    absolute_import	    as __FUTURE_absolute_import,
    print_function	    as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


# Exceptions


from __builtin__ import (
    BaseException	    as __builtins_BaseException,
    StandardError	    as __builtins_StandardError,
)


class Exception_BASE( __builtins_BaseException ):
    """
	Base class for all :py:mod:`utilia` exceptions.
	
	Inherits from the Python built-in ``BaseException``.

	Use this for your exception handler signature if you wish to catch any
	exception raised from within :py:mod:`utilia`.
    """


    def __init__( self, *posargs ):
	"""
	    Invokes superclass initializers.
	"""

	super( Exception_BASE, self ).__init__( *posargs )


class Error_BASE( Exception_BASE, __builtins_StandardError ):
    """
	Base class for all :py:mod:`utilia` exceptions which are regarded as
	errors.
	
	Inherits from :py:class:`Exception_BASE` and the Python built-in
	``StandardError``.

	Use this for your exception handler signature if you wish to catch any
	error condition raised from within :py:mod:`utilia`.
    """


    def __init__( self, *posargs ):
	"""
	    Invokes superclass initializers.
	"""

	super( Error_BASE, self ).__init__( *posargs )


class Error_WithRC( Error_BASE ):
    """
	Base class for all :py:mod:`utilia` exceptions which are regarded as
	errors and which carry a return code that could be supplied to a
	``SystemExit`` exception.

	Inherits from :py:class:`Error_BASE`.

	Use this for your exception handler signature if you wish to catch any
	error condition, which has an exit code, raised from within
	:py:mod:`utilia`.
    """


    #: Return code to use as the exit status if the error is considered fatal.
    rc		    = 0


    def __init__( self, *posargs ):
	"""
	    Invokes superclass initializers.
	    Sets the return code to carry with the exception.
	"""

	super( Error_WithRC, self ).__init__( *posargs )
	self.rc = 0


    def __str__( self ):
	"""
	    Provides a human-readable representation of the error, 
	    including the return code it is carrying.
	"""

	s = super( Error_WithRC, self ).__str__( )
	s += " <Return Code: {0}>".format( self.rc )
	return s


class Error_WithReason( Error_BASE ):
    """
	Base class for all :py:mod:`utilia` exceptions which are regarded as
	errors and which carry a translatable error reason format string and a
	tuple of arguments for substitution into the format string.

	Inherits from :py:class:`Error_BASE`.

	Use this for your exception handler signature if you wish to catch any
	error condition, which has a translatable reason string, raised from
	within :py:mod:`utilia`.
    """


    #: Terse format string explaining why the path was undetermined.
    #: The format string expects arguments to be supplied from
    #: :py:attr:`reason_args`.
    reason_format	= None
    #: Tuple of arguments to be substituted into :py:attr:`reason_format`.
    reason_args		= ( )


    def __init__( self, reason_format, *reason_args ):
	"""
	    Invokes superclass initializers.
	    Sets the reason format string to carry with the exception.

	    :param reason_format: String containing zero or more 
				  ``format``-style substitution tokens.
	    :param *reason_args: Zero or more arguments to be substituted into
				 the reason format string.
	"""

	super( Error_WithReason, self ).__init__(
	    reason_format, *reason_args
	)
	self.reason_format  = reason_format
	self.reason_args    = reason_args


###############################################################################
# vim: set ft=python sts=4 sw=4 tw=79:					      #

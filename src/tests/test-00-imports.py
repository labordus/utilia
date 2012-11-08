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
    Implements the following tests:

    * Can the module be imported successfully?

    * Are the module contents what we expect?
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division		    as __FUTURE_division,
    absolute_import	    as __FUTURE_absolute_import,
    print_function	    as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


import functools


def __has_attr_of_type( o, aname, atype ):
    """
	Asserts that an attribute exists in a given object
	and that the attribute is of the supplied type.
    """

    assert hasattr( o, aname ), aname
    a = getattr( o, aname )
    assert atype is type( a ), a


def test_IMPORT_MODULE( ):
    """ Can module 'utilia' be successfully imported? """
    
    import utilia


def test_MODULE_ATTRIBUTES( ):
    """ Checks the list of attributes for the 'utilia' module. """

    import utilia

    type_of_function	= type( lambda: None )
    type_of_class	= type( object )

    for aname, atype in [
	[ "__FUTURE_division",		type( __FUTURE_division ) ],
	[ "__FUTURE_absolute_import",	type( __FUTURE_absolute_import ) ],
	[ "__FUTURE_print_function",	type( __FUTURE_print_function ) ],
	[ "__builtins_BaseException",	type( BaseException ) ],
	[ "__builtins_StandardError",	type( StandardError ) ],
	[ "__version__",		str ],
	[ "Exception_BASE",		type_of_class ],
	[ "Error_BASE",			type_of_class ],
	[ "Error_WithRC",		type_of_class ],
	[ "Error_WithReason",		type_of_class ],
    ]:

	f_decorated = \
	functools.partial( __has_attr_of_type, utilia, aname, atype )
	f_decorated.description = \
	"""Does module 'utilia' have an attribute '{aname}' """ \
	"""of type '{atypename}'?""" \
	"".format( aname = aname, atypename = atype.__name__ )

	yield f_decorated


###############################################################################
# vim: set ft=python sts=4 sw=4 tw=79:					      #
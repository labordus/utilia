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
    Provides various utilities pertaining to file systems. These modules
    provide uniform interfaces for querying information about and 
    manipulating various aspects of file systems, regardless of file system 
    type or operating system.

    The following modules provide calculated paths:

        * :py:mod:`.stdpath`
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


# Exceptions


from utilia.exceptions import (
    Exception_BASE	    as _Exception_BASE_SUPER,
    Error_BASE		    as _Error_BASE_SUPER,
)


class Exception_BASE( _Exception_BASE_SUPER ): # pylint: disable=W0232,R0903
    """
	Base class for all :py:mod:`utilia` filesystem exceptions.

	Use this for your exception handler signature if you wish to catch any
	filesystem-related exception raised from within :py:mod:`utilia`.
    """

    pass


class Error_BASE( _Error_BASE_SUPER ): # pylint: disable=W0232,R0903
    """
	Base class for all :py:mod:`utilia` filesystem exceptions which are
	regarded as errors.

	Use this for your exception handler signature if you wish to catch any
	filesystem-related error condition raised from within :py:mod:`utilia`.
    """

    pass


###############################################################################
# vim: set ft=python sts=4 sw=4 tw=79:                                        #

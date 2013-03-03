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
    Uniform list of exit codes with values that may vary according to any
    prevailing standards for a given platform [1]_, [2]_.
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


# Note: The Windows platform does not appear to have a consistent standard for
#       application exit codes, aside from 0 indicating success.
#       If a divergent standard for Windows or another platform is discovered,
#       then this module may need to split into multiple, internal back-end
#       implementations. For now, the exit codes specified by ISO and BSD are
#       used.


def SUCCESS( ):
    """
        Successful completion of process.
    """

    return 0


def FAILURE( ):
    """
        Unsuccessful completion of process without error.

        (Example: POSIX :command:`grep` returns 1 when no lines are matched.)
    """

    return 1


def ERROR( ):
    """
        Exiting process because of a general error.

        (Example: POSIX :command:`grep` returns 2 on error.)
    """

    return 2


def INTERNAL_SOFTWARE_ERROR( ):
    """
        Exiting process because the software failed an internal consistency
        check or assertion, encountered an unimplemented virtual method, 
        etc....
    """

    return 70


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

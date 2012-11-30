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
    Provides a uniform means to access the 
    :py:mod:`module <CPython:__builtin__>` containing Python built-ins 
    across the various implementations and versions of Python supported by 
    this project.
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


from utilia import (
    python_version,
)


if   3 == python_version.major:
    from builtins import *
    __doc__ += \
    """

    The following compatibility enhancements have been made:
    """

    # NOTE: Project internals should use 'utilia.Error_BASE'.
    # Note: All error exceptions inherit from 'Exception' rather than
    #       'StandardError' in Python 3.
    StandardError   = Exception
    __doc__ += \
    """

        * :py:exc:`StandardError <CPython:exceptions.StandardError>` is 
          aliased to :py:exc:`Exception <CPython:exceptions.Exception>`.
    """

    # Note: The 'range' function of Python 3 behaves as the 'xrange' function
    #       of Python 2.
    xrange          = range
    __doc__ += \
    """
    
        * :py:func:`xrange` is aliased to :py:func:`range`.
    """

else:
    from __builtin__ import *


# Cleanup the module namespace.
del python_version

###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

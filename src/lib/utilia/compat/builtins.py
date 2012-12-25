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
    Imports the contents of the relevant 
    :py:mod:`built-ins <CPython3:builtins>` module for the current Python
    implementation and provides some things which may be missing from it.

    For Python 3, these augmentations are performed for 
    backward-compatibility:

        * :py:exc:`StandardError <CPython2:exceptions.StandardError>` is 
          aliased to :py:exc:`Exception <CPython3:Exception>`.

        * :py:func:`xrange <CPython2:xrange>` is aliased to 
          :py:class:`range <CPython3:range>`.

"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


from utilia import (
    python_version          as __python_version,
)


if   3 == __python_version.major:
    from builtins import *

    # NOTE: Project internals should use 'utilia.Error_BASE'.
    # Note: All error exceptions inherit from 'Exception' rather than
    #       'StandardError' in Python 3.
    StandardError   = Exception

    # Note: The 'reduce' function has been moved to the 'functools' module in 
    #       Python 3.
    from functools import reduce

    # Note: The 'range' function of Python 3 behaves as the 'xrange' function
    #       of Python 2.
    xrange          = range

else:
    from __builtin__ import *


# Cleanup the module namespace.
del __python_version

###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

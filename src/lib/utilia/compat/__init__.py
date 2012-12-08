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
    Provides a compatibility layer among the different implementations and
    versions of Python. This is achieved by providing access to modules,
    classes, and functions via a uniform naming convention.

    The following modules are available:

        * A :py:mod:`built-ins <.builtins>` module, which shadows the 
          appropriate Python one and provides missing pieces.

        * A shadow of the Python :py:mod:`collections <.collections>` module, 
          which provides missing pieces.

        * A :py:mod:`configuration file parser <.configparser>` module, which
          shadows the appropriate Python one.
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division                as __FUTURE_division,
    absolute_import         as __FUTURE_absolute_import,
    print_function          as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

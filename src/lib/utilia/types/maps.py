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
    Provides a collection of various map types with a consistent interface 
    across Python versions. The collection of map types consists of:
        
        * :py:class:`OrderedDict`
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


if [ python_version.major, python_version.minor ] in [ [ 2, 6 ], [ 3, 0 ] ]:
    from .OrderedDict   import OrderedDict
else:
    from collections    import OrderedDict


# Cleanup the module namespace.
del python_version

###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

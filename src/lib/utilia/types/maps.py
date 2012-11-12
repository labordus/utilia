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
    Provides various useful map types, using drop-in replacements for cases
    where they are not natively supported in the standard library for a
    particular version of Python.
"""


# Note: Future imports must go before other imports.
from __future__ import (
    division		    as __FUTURE_division,
    absolute_import	    as __FUTURE_absolute_import,
    print_function	    as __FUTURE_print_function,
) # Assumes Python version >= 2.6.


__docformat__ = "reStructuredText"


import sys


if 3 <= sys.version_info.major:
    from collections	import OrderedDict
else:
    # Note: Technically, Python 2.7 has OrderedDict, but it is not clear
    #	    whether that implementation will be absorbing new features which
    #	    the latest in the 3.x series might gain.
    from .OrderedDict	import OrderedDict


###############################################################################
# vim: set ft=python sts=4 sw=4 tw=79:					      #

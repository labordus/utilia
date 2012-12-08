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
    Imports the contents of the :py:mod:`collections <CPython3:collections>`
    module from the Python standard library and provides pieces which are 
    missing in some Python implementations.

    For Python 2.6 and 3.0, these missing classes are provided:

        * :py:class:`OrderedDict <CPython2:collections.OrderedDict>`

    .. note::
       The source code for the ``OrderedDict`` class comes from a recipe
       provided by a third party. This code or a near variant of it was
       included into Python 2.7 and Python 3.1 per acceptance of :pep:`372`.
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


from collections import *

if  [ __python_version.major, __python_version.minor ] \
    in [ [ 2, 6 ], [ 3, 0 ] ]:
    from utilia.types.ordered_dict import (
        OrderedDict,
    )


# Cleanup the module namespace.
del __python_version

###############################################################################
# vim: set ft=python ts=4 sts=4 sw=4 et tw=79:                                #

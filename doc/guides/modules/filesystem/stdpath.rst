..                                 utilia

.. This work is licensed under the Creative Commons Attribution 3.0 
   Unported License. To view a copy of this license, visit 

      http://creativecommons.org/licenses/by/3.0/ 

``stdpath`` Module
==================

Module Description
------------------

.. automodule:: utilia.filesystem.stdpath

Exception Classes
-----------------

.. autoclass:: UnsupportedFilesystemLayout
   :members:
   :inherited-members:

.. autoclass:: UndeterminedFilesystemPath
   :members:
   :inherited-members:

Elementary Functions
--------------------

.. autofunction:: which_fs_layout

.. autofunction:: concatenated_software_path_fragment

Public Base Paths
-----------------

.. autofunction:: whereis_oscore_install_root

.. autofunction:: whereis_osdist_install_root

.. autofunction:: whereis_common_install_root

.. autofunction:: whereis_common_temp_base

.. autofunction:: whereis_oscore_config_base

.. autofunction:: whereis_osdist_config_base

.. autofunction:: whereis_common_config_base

User Base Paths
---------------

.. autofunction:: whereis_user_home

.. autofunction:: whereis_user_temp_base

Other Base Paths
----------------

.. autofunction:: whereis_preferred_temp_base

Public Derived Paths
--------------------

.. autofunction:: whereis_my_common_config_at_base

.. autofunction:: whereis_my_common_config

.. autofunction:: whereis_my_common_config_pythonic

.. autofunction:: whereis_my_common_resources_at_base

.. autofunction:: whereis_my_common_resources

.. autofunction:: whereis_my_common_resources_pythonic

User Derived Paths
------------------

.. autofunction:: whereis_my_user_config_at_base

.. autofunction:: whereis_my_user_config

.. autofunction:: whereis_my_user_config_pythonic

.. autofunction:: whereis_my_user_resources_at_base

.. autofunction:: whereis_my_user_resources

.. autofunction:: whereis_my_user_resources_pythonic

Other Derived Paths
-------------------

.. autofunction:: whereis_my_saved_data_at_base

.. autofunction:: whereis_my_saved_data

.. autofunction:: whereis_my_temp


.. _SECTION-utilia.filesystem.stdpath-Examples:

Examples
--------

.. todo::
   Create examples.

References
----------

.. [#] `Linux Filesystem Hierarchy Standard 2.3`_

.. _Linux Filesystem Hierarchy Standard 2.3:
   http://www.pathname.com/fhs/pub/fhs-2.3.html

.. [#] `XDG Base Directory Specification 0.8`_

.. _XDG Base Directory Specification 0.8:
   http://standards.freedesktop.org/basedir-spec/0.8/

.. [#] `Mac OS X and iOS File System Basics`_

.. _Mac OS X and iOS File System Basics:
   http://developer.apple.com/library/mac/#documentation/FileManagement/Conceptual/FileSystemProgrammingGUide/FileSystemOverview/FileSystemOverview.html

.. [#] `BSD Filesystem Hierarchy for Darwin`_

.. _BSD Filesystem Hierarchy for Darwin:
   https://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man7/hier.7.html

.. [#] `Windows XP Command Shell Overview`_

.. _Windows XP Command Shell Overview:
   http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/ntcmds_shelloverview.mspx?mfr=true

.. [#] `Windows CSIDL Values`_

.. _Windows CSIDL Values:
   http://msdn.microsoft.com/en-us/library/windows/desktop/bb762494(v=vs.85).aspx

.. [#] `Windows KNOWNFOLDERID Reference`_

.. _Windows KNOWNFOLDERID Reference:
   http://msdn.microsoft.com/en-us/library/windows/desktop/dd378457(v=vs.85).aspx

.. vim: set ft=rst ts=3 sts=3 sw=3 et tw=79:

..				   utilia

.. This work is licensed under the Creative Commons Attribution 3.0 
   Unported License. To view a copy of this license, visit 

      http://creativecommons.org/licenses/by/3.0/ 

*utilia* Environment Variables
==============================

.. envvar:: UTILIA_SOFTWARE_NAME

   Provides extra, optional guidance to the logic which determines paths to 
   use with the named software package. (For examples of what logic in the
   :py:mod:`utilia` package is affected by this environment variable, see 
   :py:mod:`utilia.filesystem.stdpath`, in particular.)

   Typically, the program using *utilia* should set this environment variable by
   manipulating ``os.environ``. For example, a piece of software, named ``foo``,
   would do this within its own code before using functions from the
   :py:mod:`utilia` package::
      
      import os
      from utilia.filesystem.stdpath import whereis_my_site_data

      os.environ[ "UTILIA_SOFTWARE_NAME" ] = "foo"

      sdp = whereis_my_site_data( )

.. envvar:: software_name_INSTALL_PATH

   Provides extra, optional guidance to the logic which determines paths to 
   use with the named software package. (For examples of what logic in the
   :py:mod:`utilia` package is affected by this environment variable, see 
   :py:mod:`utilia.filesystem.stdpath`, in particular.)

   Please note that this is a template for the actual variable name. The actual
   variable name is determined by the :envvar:`UTILIA_SOFTWARE_NAME` environment
   variable within the *utilia* logic. For example, a piece of software, named
   ``foo``, would have a corresponding environment variable, named
   ``FOO_INSTALL_PATH``. Typically, if it is deemed that this variable needs to
   be set, a systems administrator or the software installer will ensure that it
   is set in the sitewide environment. On Unix, a hypothetical Bourne shell 
   init file, :file:`/etc/profile.d/foo.sh`, might contain:

   .. sourcecode:: sh

      FOO_INSTALL_PATH="/opt/foo/1.2.3"
      export FOO_INSTALL_PATH

   On Windows, a hypothetical batch file, might contain:

   .. sourcecode:: bat

      set FOO_INSTALL_PATH="C:\Program Files\Foo\1.2.3"

   At a Unix high performance computing center, a hypothetical environment
   module might contain:

   .. sourcecode:: tcl

      set install_base "/opt/sftw"
      set pkg_name "foo"
      set pkg_version "1.2.3"
      set python_version "2.7"
      set prefix "$install_base/$pkg_name/$pkg_version"
      setenv FOO_INSTALL_PATH "$prefix"
      prepend-path PYTHONPATH "$prefix/lib/$python_version/site-packages"

.. envvar:: software_name_DEVEL_PATH

   Provides extra, optional guidance to the logic which determines paths to 
   use with the named software package. (For example of what logic in the
   :py:mod:`utilia` package is affected by this environment variable, see 
   :py:mod:`utilia.filesystem.stdpath`, in particular.)

   Please note that this is a template for the actual variable name. The actual
   variable name is determined by the :envvar:`UTILIA_SOFTWARE_NAME` environment
   variable within the *utilia* logic. For example, a piece of software, named
   ``foo``, would have a corresponding environment variable, named
   ``FOO_DEVEL_PATH``. Typically, shell scripts and batch files should be
   provided with a checkout of the software's sources from version control. The
   appropriate shell script or batch file should then be sourced or executed 
   by a developer before loading the software's packages into a Python 
   interpreter or running any accompanying scripts. A hypothetical Bourne shell
   script might look like:

   .. sourcecode:: sh

      FOO_DEVEL_PATH="`pwd`"
      export FOO_DEVEL_PATH

      if [ -z "$PYTHONPATH" ]
      then
         PYTHONPATH="${FOO_DEVEL_PATH}/src/lib"
      else
         PYTHONPATH="${FOO_DEVEL_PATH}/src/lib:$PYTHONPATH"
      fi
      export PYTHONPATH


.. vim: set ft=rst sts=3 sw=3 tw=79:

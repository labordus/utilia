..                                 utilia

.. This work is licensed under the Creative Commons Attribution 3.0 
   Unported License. To view a copy of this license, visit 

      http://creativecommons.org/licenses/by/3.0/ 

Tuples
------

The :py:class:`tuple <CPython3:tuple>` type is somewhat controversial 
in Python. The following discussion is not intended to be an attack on this 
type, but will highlight some of the elements of the controversy.

Versus Lists
~~~~~~~~~~~~

From a strictly functional perspective, the major difference between a
:py:class:`tuple <CPython3:tuple>` and a :py:class:`list <CPython3:list>` is
that a :py:class:`tuple <CPython3:tuple>` contains an immutable sequence
whereas a :py:class:`list <CPython3:list>` does not. Beyond this, some people
in the Python community claim that the :py:class:`list <CPython3:list>` type is
intended for homogeneous collections whereas the 
:py:class:`tuple <CPython3:tuple>` type is intended for heterogeneous 
collections with a fixed ordering. For example, see the discussions at:

  http://third-bit.com/blog/archives/000450.html#comment-380

  http://news.e-scribe.com/397

However, the Python language does not enforce the distinction between
homogeneity and heterogeneity for the two types. Pretending that it is actually
there seems a bit like wearing the emperor's new clothes. Furthermore, most
examples cited to support the alleged fixed ordering property rely upon the 
immutability of the sequence to enforce this. But, as is often the case, the 
semantics of something is in the eye of the beholder.

Named Tuples
~~~~~~~~~~~~

In Python 2.6, the :py:func:`namedtuple <CPython3:collections.namedtuple>` 
type factory was introduced into the :py:mod:`collections` package of the 
standard library. Types, created with this factory, contain collections with 
a fixed ordering. Thus, the claims made about this property of the 
:py:class:`tuple <CPython3:tuple>` type can be enforced in types out 
of the :py:func:`namedtuple <CPython3:collections.namedtuple>` factory. 
Therefore, if you need the fixed ordering property, it is recommended that 
you create types with this factory and use them. These types can be used in
nearly any situation in which a plain :py:class:`tuple <CPython3:tuple>` can 
be used.

Types, created with :py:func:`namedtuple <CPython3:collections.namedtuple>`,
have some additional advantages over the :py:class:`tuple <CPython3:tuple>`
type:

   * They are named, and their names are reflected in the strings returned by
     functions such as :py:func:`repr <CPython3:repr>` and 
     :py:func:`type <CPython3:type>`.

   * They can be instantiated with positional or keyword arguments, where the
     keywords are the names of their sequence members.

   * Sequence members of their instances can be accessed by name as well as 
     by index.

Here are some examples of preferred and avoided usages:

   .. code-block:: python

      from collections import namedtuple
      Point = namedtuple( "Point", "x y" )
      OneTuple = namedtuple( "OneTuple", "u" )

      some_dict = { Point( 3, 4 ): "foo" }   # prefer
      some_dict = { ( 3, 4 ): "foo" }        # avoid

      p = Point( 5, 12 ); p.x**2 + p.y**2       # prefer
      p = Point( 5, 12 ); p[ 0 ]**2 + p[ 1 ]**2 # avoid
      p = ( 5, 12 ); p[ 0 ]**2 + p[ 1 ]**2      # avoid

      OneTuple( 42 ) # sequence containing an integer
      ( 42 )         # uncontained integer
      tuple( 42 )    # ERROR

Syntactic Sugar
~~~~~~~~~~~~~~~

Avoid the syntactic sugar for tuples (parentheses) whenever possible, because 
of the following reasons:

   * Parentheses are already used for expression grouping and invoking
     callables. Too many parentheses can make source code harder to read.

   * The initialization of a 1-tuple cannot be disambiguated from a grouped
     expression, except with the inclusion of a trailing comma. Programming 
     error can creep in when the size of a tuple initializer is reduced to 
     one element from a higher number of elements or increased to one element 
     from no elements, as the trailing comma may be forgotten.

Here are some examples of preferred and avoided usages:

   .. code-block:: python
      
      [ ]         # prefer
      tuple( )    # prefer if sequence immutability is desired
      ( )         # avoid
      
      [ 1 ]          # prefer
      tuple( [ 1 ] ) # prefer if sequence immutability is desired
      ( 1, )         # avoid
      
      [ 1, 2, 4 ]          # prefer
      tuple( [ 1, 2, 4 ] ) # prefer if sequence immutability is desired
      ( 1, 2, 4 )          # avoid

      return "a", 1, foo      # prefer
      return ( "a", 1, foo )  # avoid
      
      from utilia.compat import iter_dict_items
      for key, val in iter_dict_items( some_dict )       # prefer
      for ( key, val ) in iter_dict_items( some_dict )   # avoid

If you care about linguistic symmetry or code aesthetics, then consider the
following contrasts:

   .. code-block:: python
      
      [ 42 ]   # asymmetric with tuple, symmetric with set
      ( 42, )  # asymmetric with list and set
      { 42 }   # asymmetric with tuple, symmetric with list
      # Note: Sugar for set is only available in Python 2.7 and 3.x.

      tuple( [ 1, 2, 4 ] )      # symmetric with set
      set( [ 1, 2, 4 ] )        # symmetric with tuple

Lists
-----

Lists Of Tuples
~~~~~~~~~~~~~~~

An :py:class:`OrderedDict <CPython2:collections.OrderedDict>` can be used to
accumulate key-value pairs in an order-preserving manner. These accumulated
pairs can later be retrieved as tuples via a standard iteration method. This is
cleaner than appending tuples to a list.

   .. code-block:: python
      
      from utilia.compat import iter_dict_items
      from utilia.compat.collections import OrderedDict

      od = OrderedDict( )
      od[ "foo" ] = 1
      od[ "bar" ] = 2
      # ...
      od[ "baz" ] = 3
      
      for key, value in iter_dict_items( od ):
         # Do stuff.

In cases where lists of tuples can be generated automatically, then the use of
a tuple type, produced by the 
:py:func:`namedtuple <CPython3:collections.namedtuple>` factory, is preferred. 
If anonymity and mutability are acceptable, then using a list of lists is
preferred.

   .. code-block:: python
      
      from collections import namedtuple

      # prefer: list of named tuples
      Pair = namedtuple( "Pair", "x y" )
      [ Pair( x, y ) for x in xrange( 10 ) for y in xrange( 10 ) ]
      # prefer: list of lists
      [ [ x, y ] for x in xrange( 10 ) for y in xrange( 10 ) ]
      # avoid
      [ tuple( [ x, y ] ) for x in xrange( 10 ) for y in xrange( 10 ) ]
      # avoid
      [ ( x, y ) for x in xrange( 10 ) for y in xrange( 10 ) ]

Sets
----

Syntactic Sugar
~~~~~~~~~~~~~~~

As the present aim is to support Python 2.6 in addition to higher versions, we
cannot use the syntactic sugar for the :py:class:`set <CPython3:set>` type, 
which is available in Python 2.7 and 3.x. Therefore:

   .. code-block:: python
      
      set( [ 1, 2, 4 ] )        # use
      { 1, 2, 4 }               # do not use

.. vim: set ft=rst ts=3 sts=3 sw=3 et tw=79:

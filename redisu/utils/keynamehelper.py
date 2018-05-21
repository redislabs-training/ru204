"""Utilities to generate key & field names based on the variadic parameters
passed.
e.g., by default , gievn the values "foo" and "bar" as parameters, the functions
will generate
  "foo:bar"

Todo:
  * Deal with non-string values, rather than rely upon the caller to make
into strings
"""
__prefix__ = ""
__sep__ = ":"

def set_prefix(ch):
  """Set the prefix to use. This is typically the course or unit number"""
  global __prefix__
  __prefix__ = ch

def get_prefix():
  """Return the current prefix"""
  return __prefix__

def set_sep(ch):
  """Set the seperator to use, the default is dfined in the initialization of
  this script."""
  global __sep__
  __sep__ = ch

def get_sep():
  """Return the current seperator."""
  return __sep__

def create_key_name(*vals):
  """Create the key name based on the following format

     [ prefix + sepatartor] + [ [ separator + value] ]
  """
  return ((__prefix__ + __sep__) if (__prefix__ != "") else "")\
         + "%s" % __sep__.join(vals)

def create_field_name(*vals):
  """Create the field name based on the following format

     [ [ separator + value] ]

  Typically used for field names in a has, where you don't need the prefix
  added, because the returned value is used in the content of a key.
  """
  return "%s" % __sep__.join(vals)

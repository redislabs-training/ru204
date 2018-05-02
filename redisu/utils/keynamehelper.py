"""Utility to generate key names based on the variadic parameters passed. The
key name is generated as follows
	* prefix
	* seperator
	* [ value seperator ]

e.g., buy default , gievn the values "foo" and "bar" passed will generate
	"foo:bar"

Todo:
	* Deal with non-string values, rather than rely upon the caller to make
into strings
"""
__prefix__ = ""
__sep__ = ":"

def set_prefix(ch):
	global __prefix__
	__prefix__ = ch

def set_sep(ch):
	global __sep__
	__sep__ = ch


def create_key_name(*vals):
	return ((__prefix__ + __sep__ ) if (__prefix__ != "") else "") + "%s" % __sep__.join(vals)

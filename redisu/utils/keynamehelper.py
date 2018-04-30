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

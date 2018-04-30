__prefix__ = ""

def set_prefix(ch):
	global __prefix__
	__prefix__ = ch

def create_key_name(*vals):
	return __prefix__ + "%s" % ':'.join(vals)
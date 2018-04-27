__chapter_prefix__ = ""

def set_prefix(ch):
	__chapter_prefix__ = ch

def create_key_name(*vals):
	return __chapter_prefix__ + "%s" % ':'.join(vals)
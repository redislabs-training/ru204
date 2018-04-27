from faker import Faker

fake = Faker()

def cust_id():
	return fake.pystr(min_chars=8, max_chars=8).upper()

def sku():
	return "{0}-{1}-{2}-{3}".format(fake.pystr(min_chars=4, max_chars=4), fake.pystr(min_chars=4, max_chars=4), 
																	fake.pystr(min_chars=4, max_chars=4), fake.pystr(min_chars=4, max_chars=4)).upper()

def order_id():
	return "{0}-{1}".format(fake.pystr(min_chars=6, max_chars=6), fake.pystr(min_chars=4, max_chars=6)).upper()

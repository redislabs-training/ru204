"""Helper functions to create fake identifiers in various formats"""
from faker import Faker

__fake__ = Faker()

def cust_id():
  """Generate customer id in the format AAAAAAAA"""
  return __fake__.pystr(min_chars=8, max_chars=8).upper()

def sku():
  """ Generate sku in the format AAAA-AAAA-AAAA-AAAA"""
  return "{0}-{1}-{2}-{3}".format(__fake__.pystr(min_chars=4, max_chars=4),
                                  __fake__.pystr(min_chars=4, max_chars=4),
                                  __fake__.pystr(min_chars=4, max_chars=4),
                                  __fake__.pystr(min_chars=4, max_chars=4)
                                 ).upper()

def order_id():
  """ Generate fake order id's in the format AAAAAA-AAAAAA"""
  return "{0}-{1}".format(__fake__.pystr(min_chars=6, max_chars=6),
                          __fake__.pystr(min_chars=6, max_chars=6)).upper()

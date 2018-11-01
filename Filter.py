
import decimal

class Filter (object):
    def __init__(self):
        self.currencies = {}
        self.vendors = {}
        self.unknown_vendor_penalty = decimal.Decimal("10.0")
        self.must_be_authorized = True



import sys
import decimal

class PriceBreak (object):
    def __init__(self, currency=None, price=None, quantity=None, minimum=None, multiple=None):
        self.currency = currency
        self.price = decimal.Decimal(price)
        self.quantity = quantity
        self.minimum = minimum
        self.multiple = multiple

    def __repr__(self):
        return "<PriceBreak cur=%s price=%s quant=%s min=%s mul=%s>" % (
            self.currency,
            self.price,
            self.quantity,
            self.minimum,
            self.multiple
        )

    def orderQuantity(self, needed_quantity):
        print(repr(needed_quantity), repr(self.minimum), file=sys.stderr)
        quantity = max(needed_quantity, self.minimum)
        quantity = ((quantity + (self.multiple - 1)) // self.multiple) * self.multiple
        return quantity

    def orderPrice(self, needed_quantity):
        order_quantity = self.orderQuantity(needed_quantity)
        print(repr(self.price), repr(order_quantity), file=sys.stderr)
        return self.price * order_quantity


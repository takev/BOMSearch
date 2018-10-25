
import sys
import decimal

class PriceBreak (object):
    def __init__(self, currency, currency_conversion, price, quantity, minimum, multiple):
        self.currency = currency
        self.price = decimal.Decimal(price)
        self.currency_conversion = currency_conversion
        self.quantity = quantity
        self.minimum = minimum
        self.multiple = multiple

    def __repr__(self):
        return "<PriceBreak price=%s %s, price=%s EUR, quant=%s, min=%s, mul=%s>" % (
            self.price,
            self.currency,
            self.localPrice(),
            self.quantity,
            self.minimum,
            self.multiple
        )

    def localPrice(self):
        return (self.price * self.currency_conversion).quantize(decimal.Decimal("0.00001"))

    def orderQuantity(self, needed_quantity):
        quantity = max(needed_quantity, self.minimum)
        quantity = max(quantity, self.quantity)
        quantity = ((quantity + (self.multiple - 1)) // self.multiple) * self.multiple
        return quantity

    def orderPrice(self, needed_quantity):
        return self.localPrice() * self.orderQuantity(needed_quantity)

    def orderPricePer(self, needed_quantity):
        return self.orderPrice(needed_quantity) / needed_quantity

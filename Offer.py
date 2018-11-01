
import sys
import decimal

class Offer (object):
    def __init__(
        self, brand, manufacturer, mpn, vendor, vendor_penalty, sku,
        is_authorized, in_stock_quantity, currency, currency_conversion,
        price, quantity, minimum, multiple
    ):
        self.brand = brand
        self.manufacturer = manufacturer
        self.mpn = mpn
        self.vendor = vendor
        self.vendor_penalty = vendor_penalty
        self.sku = sku
        self.is_authorized = is_authorized
        self.in_stock_quantity = in_stock_quantity
        self.currency = currency
        self.currency_conversion = currency_conversion
        self.price = price
        self.quantity = quantity
        self.minimum = minimum
        self.multiple = multiple

    def __repr__(self):
        return "<Offer mpn=%s:%s sku=%s:%s price=%s %s, price=%s EUR, quant=%s, min=%s, mul=%s>" % (
            self.brand, self.mpn,
            self.vendor, self.sku,
            self.price, self.currency,
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

    def orderPriceWithPenalty(self, needed_quantity):
        return self.orderPrice(needed_quantity) * self.vendor_penalty

    def orderPricePer(self, needed_quantity):
        return self.orderPrice(needed_quantity) / needed_quantity


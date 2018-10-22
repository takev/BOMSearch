
import utils

class PartOffer (object):
    def __init__(self):
        self.price_breaks = []

    def __repr__(self):
        s = "<PartOffer seller=%s sku=%s quantity=%i authorized=%s" % (
            self.seller,
            self.stock_keeping_unit,
            self.in_stock_quantity,
            "yes" if self.is_authorized else "no"
        )

        s+= utils.indentReprList(self.price_breaks)
        s+= ">"
        return s

    def add(self, price_break):
        self.price_breaks.append(price_break)

    def findBestPriceBreak(self, needed_quantity, currency, must_be_authorized):
        if needed_quantity < self.in_stock_quantity:
            return None
        if must_be_authorized and not self.is_authorized:
            return None

        best_price_break = None
        for price_break in self.price_breaks:
            if price_break.currency != currency:
                continue

            if best_price_break is None or price_break.orderPrice(needed_quantity) < best_price_break.orderPrice(needed_quantity):
                best_price_break = price_break

        return best_price_break

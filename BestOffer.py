

class BestOffer (object):
    def __init__(self, needed_quantity, part, offer, price_break):
        self.needed_quantity = needed_quantity
        self.part = part
        self.offer = offer
        self.price_break = price_break

    def __eq__(self, other):
        return self.price_break.orderPrice(self.needed_quantity) == other.price_break.orderPrice(self.needed_quantity)

    def __lt__(self, other):
        return self.price_break.orderPrice(self.needed_quantity) < other.price_break.orderPrice(self.needed_quantity)


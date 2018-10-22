
import utils
import BestOffer

class Part (object):
    def __init__(self):
        self.offers = []

    def __repr__(self):
        s = "<Part brand=%s/%s mpn=%s" % (self.manufacturer, self.brand, self.manufacturer_part_number)
        s += utils.indentReprList(self.offers)
        s += ">"
        return s

    def add(self, offer):
        self.offers.append(offer)

    def findBestOffer(self, needed_quantity, currency, must_be_authorized=True):
        best_offer = None

        for offer in self.offers:
            price_break = offer.findBestPriceBreak(needed_quantity, currency, must_be_authorized)
            if price_break:
                tmp = BestOffer.BestOffer(needed_quantity, self, offer, price_break, currency)

                if best_offer is None or tmp < best_offer:
                    best_offer = tmp

        return best_offer




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

    def hasOffers(self):
        return len(self.offers) > 0

    def findBestOffer(self, needed_quantity):
        best_offer = None

        for offer in self.offers:
            price_break = offer.findBestPriceBreak(needed_quantity)
            if price_break:
                tmp = BestOffer.BestOffer(needed_quantity, self, offer, price_break)

                if best_offer is None or tmp < best_offer:
                    best_offer = tmp

        return best_offer



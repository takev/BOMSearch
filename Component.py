
import sys
import utils
import decimal

import PartQueries
import PartQuery

class Component (object):
    def __init__(self):
        self.quantity = 0
        self.locations = []
        self.type = None
        self.value = None
        self.datasheet = None
        self.description = None
        self.characteristics = ""
        self.queries = PartQueries.PartQueries()
        self.parts = []
        self.best_offers = {}

    def __repr__(self):
        s = "<Component MFP=%s quantity=%i value=%s refs=%s" % (self.queries, self.quantity, repr(self.value), self.refs())
        s += utils.indentReprList(self.parts)
        s += ">"
        return s

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name.startswith("mfp") or name.startswith("mfn"):
            suffix = name[3:]

            if hasattr(self, "mfn" + suffix) and hasattr(self, "mfp" + suffix):
                brand_name = getattr(self, "mfn" + suffix)
                part_number = getattr(self, "mfp" + suffix)

                if not part_number and not brand_name:
                    # Neither part_number nor brand_name, is okay
                    pass

                elif part_number and brand_name:
                    query = PartQuery.PartQuery(brand_name, part_number)
                    self.queries.add(query)

                else:
                    print("Missing brand name or part number for component %s" % (repr(self)), file=sys.stderr)

    def addQuantity(self, quantity):
        self.quantity += quantity

    def addLocation(self, location):
        self.locations.append(location)

    def refs(self):
        refs = [x.ref for x in self.locations]
        refs.sort()
        return ",".join(refs)

    def findParts(self, catalogue, filter):
        for query in self.queries:
            self.parts += catalogue.findOffers(query=query, filter=filter)

    def findBestOffers(self, nrProducts):
        for currency in ["EUR", "USD"]:
            best_offer = None
            for part in self.parts:
                tmp = part.findBestOffer(needed_quantity=self.quantity * nrProducts)
                if tmp and (best_offer is None or tmp < best_offer):
                    best_offer = tmp

            self.best_offer = best_offer

    def shoppingList(self, nrProducts, vendor):
        if self.best_offer is None:
            return ("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
                self.type,
                self.refs(),
                repr(self.value),
                repr(self.characteristics),
                repr(self.description),
                "",
                "",
                "",
                "",
                self.quantity * nrProducts,
                "",
                "",
                ""
            ), decimal.Decimal("0.0"))

        else:
            return ("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
                self.type,
                self.refs(),
                repr(self.value),
                repr(self.characteristics),
                repr(self.description),
                repr(self.best_offer.part.brand),
                repr(self.best_offer.part.manufacturer_part_number),
                repr(self.best_offer.offer.seller),
                repr(self.best_offer.offer.stock_keeping_unit),
                self.quantity * nrProducts,
                self.best_offer.price_break.orderQuantity(self.quantity * nrProducts),
                self.best_offer.price_break.orderPricePer(self.quantity * nrProducts),
                self.best_offer.price_break.orderPrice(self.quantity * nrProducts)
            ), self.best_offer.price_break.orderPrice(self.quantity * nrProducts))




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
        self.offers = []

    def __repr__(self):
        s = "<Component MFP=%s quantity=%i value=%s refs=%s" % (self.queries, self.quantity, repr(self.value), self.refs())
        s += utils.indentReprList(self.offers)
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
        self.offers = catalogue.findOffers(queries=self.queries, filter=filter)

    @classmethod
    def shoppingListHeader(cls):
        return [
            "type",
            "refs",
            "value",
            "characteristics",
            "description",
            "brand",
            "mpn",
            "vendor",
            "sku",
            "quant",
            "order quant",
            "unit price",
            "order price"
        ]

    def shoppingListComponent(self, nr_units):
        return {
            "type": self.type,
            "refs": self.refs(),
            "value": self.value,
            "characteristics": self.characteristics,
            "description": self.description,
            "quant": self.quantity * nr_units
        }

    def shoppingListOffer(self, nr_units, vendor):
        offers = []
        for offer in self.offers:
            if offer.orderQuantity(self.quantity * nr_units) > offer.in_stock_quantity:
                continue

            offers.append(offer)

        offers.sort(key=lambda x: x.orderPriceWithPenalty(self.quantity * nr_units))

        if offers:
            best_offer = offers[0]
            return {
                "brand": best_offer.brand,
                "mpn": best_offer.mpn,
                "vendor": best_offer.vendor,
                "sku": best_offer.sku,
                "order quant": best_offer.orderQuantity(self.quantity * nr_units),
                "unit price" : best_offer.orderPricePer(self.quantity * nr_units),
                "order price" : best_offer.orderPrice(self.quantity * nr_units)
            }
        else:
            return {"order price": decimal.Decimal("0.0")}

    def shoppingList(self, nr_units, vendor):
        d = self.shoppingListComponent(nr_units=nr_units)
        d.update(self.shoppingListOffer(nr_units=nr_units, vendor=vendor))
        return d



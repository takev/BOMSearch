
import sys
import utils
import PartQueries
import PartQuery

class Component (object):
    def __init__(self):
        self.count = 0
        self.locations = []
        self.value = None
        self.datasheet = None
        self.description = None
        self.queries = PartQueries.PartQueries()
        self.parts = []
        self.best_offers = {}

    def __repr__(self):
        refs = [x.ref for x in self.locations]
        refs.sort()
        s = "<Component MFP=%s count=%i value=%s refs=%s" % (self.queries, self.count, repr(self.value), repr(refs))
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

    def addCount(self, count):
        self.count += count

    def addLocation(self, location):
        self.locations.append(location)

    def findParts(self, part_dict):
        for query in self.queries:
            self.parts += part_dict[query]

    def findBestOffers(self):
        self.best_offers = {}
        for currency in ["EUR", "USD"]:
            best_offer = None
            for part in self.parts:
                tmp = part.findBestOffer(needed_quantity=self.count, currency=currency, must_be_authorized=True)
                if tmp and (best_offer is None or tmp < best_offer):
                    best_offer = tmp

            self.best_offers[currency] = best_offer




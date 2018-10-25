
import utils
import decimal

class Components (object):
    def __init__(self):
        self.components = {}

    def __repr__(self):
        s = "<Components"
        s += utils.indentReprList(self.components.values())
        s += ">"
        return s

    def add(self, component):
        queries = component.queries

        if queries in self.components:
            old_component = self.components[queries]
            old_component.addQuantity(component.quantity)
            for location in component.locations:
                old_component.addLocation(location)

        else:
            self.components[queries] = component

    def merge(self, other):
        for component in other.components.values():
            self.add(component)

    def findParts(self, catalogue, filter):
        for component in self.components.values():
            component.findParts(catalogue=catalogue, filter=filter)

    def findBestOffers(self, nrProducts):
        for component in self.components.values():
            component.findBestOffers(nrProducts)

    def shoppingList(self, nrProducts, vendor=None):
        components = list(self.components.values())
        components.sort(key=lambda x: x.type + ":" + x.value + ":" + x.description)

        lines = ["type;refs;value;characteristics;description;brand;mpn;seller;sku;quant;order quant;unit price;order price"]
        total_price = decimal.Decimal("0.0")
        for component in components:
            line, order_price = component.shoppingList(nrProducts=nrProducts, vendor=vendor)
            lines.append(line)

            total_price += order_price

        lines.append(";;;Total;;;;;;;;%s" % total_price)

        return "\n".join(lines) + "\n"




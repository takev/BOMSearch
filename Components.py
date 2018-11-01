
import utils
import decimal
import csv

import Component

class RealExcelDialect (csv.Dialect):
    delimiter = ";"
    quoting = csv.QUOTE_NONNUMERIC
    quotechar = "'"
    lineterminator = "\r\n"
    escapechar = "\\"

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

    def shoppingList(self, fd, nr_units, vendor=None):
        components = list(self.components.values())
        components.sort(key=lambda x: x.type + ":" + x.value + ":" + x.description)

        header = Component.Component.shoppingListHeader()
        writer = csv.DictWriter(fd, header, dialect=RealExcelDialect)
        writer.writeheader()

        total_price = decimal.Decimal("0.0")
        for component in components:
            component_offer = component.shoppingList(nr_units=nr_units, vendor=vendor)
            writer.writerow(component_offer)

            total_price += component_offer["order price"]

        writer.writerow({"description": "Total", "order price": total_price})


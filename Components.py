
import utils

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
            old_component.addCount(component.count)
            for location in component.locations:
                old_component.addLocation(location)

        else:
            self.components[queries] = component

    def merge(self, other):
        for component in other.components.values():
            self.add(component)

    def findParts(self, parts_dict):
        for component in self.components.values():
            component.findParts(parts_dict)

    def findBestOffers(self):
        for component in self.components.values():
            component.findBestOffers()


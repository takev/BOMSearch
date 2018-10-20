
import Parts

class Components (object):
    def __init__(self):
        self.components = []

    def __repr__(self):
        s = "<Components\n"
        for component in self.components:
            s += " " + repr(component) + "\n"
        s += ">"
        return s

    def add(self, component):
        self.components.append(component)

    def merge(self, other):
        self.components += other.components

    def parts(self):
        parts = Parts.Parts()

        for component in self.components:
            parts.addComponent(component)

        return parts


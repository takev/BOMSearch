
import sys
import doctest
import xml.sax
import xml.sax.handler

import Components
import Component

class KiCadExportParser (xml.sax.handler.ContentHandler):
    def __init__(self, filename_or_stream):
        """
        >>> p = KiCadExportParser("KiCadExportParser_test.xml")
        """
        xml.sax.parse(filename_or_stream, self)

    def popContent(self):
        if self.stack and isinstance(self.stack[-1], str):
            return self.stack.pop()
        else:
            return ""

    def startDocument(self):
        self.stack = []

    def endDocument(self):
        if self.stack:
            raise IndexError("XML stack is not empty at end of document.")

    def characters(self, content):
        content = content.strip()
        if not content:
            return

        if self.stack and isinstance(self.stack[-1], str):
            s = self.stack.pop() + " "
        else:
            s = ""

        self.stack.append(s + content)

    def startElement(self, name, attrs):
        method_name = "_start_%s" % name
        try:
            method = getattr(self, method_name)
            method(**attrs)
        except AttributeError:
            pass

    def endElement(self, name):
        method_name = "_end_%s" % name
        try:
            method = getattr(self, method_name)
            method()
        except AttributeError:
            pass

        # Clear text on stack after a tag.
        self.popContent()

    def _start_components(self):
        components = Components.Components()
        self.stack.append(components)

    def _end_components(self):
        self.components = self.stack.pop()
        if not isinstance(self.components, Components.Components):
            raise TypeError("Expect instance of Components.Components got " + repr(self.components))

    def _start_comp(self, ref=None, count="1"):
        component = Component.Component(ref, int(count))
        self.stack.append(component)

    def _end_comp(self):
        component = self.stack.pop()
        if not isinstance(component, Component.Component):
            raise TypeError("Expect instance of Component.Component got " + repr(component))

        components = self.stack[-1]
        components.add(component)

    def _end_value(self):
        s = self.popContent()

        component = self.stack[-1]
        if not isinstance(component, Component.Component):
            raise TypeError("Expect instance of Component.Component got " + repr(component))
        component.value = s

    def _end_datasheet(self):
        s = self.popContent()

        component = self.stack[-1]
        if not isinstance(component, Component.Component):
            raise TypeError("Expect instance of Component.Component got " + repr(component))
        component.datasheet = s

    def _start_field(self, name):
        self.field_name = name

    def _end_field(self):
        s = self.popContent()

        if self.stack and isinstance(self.stack[-1], Component.Component):
            setattr(self.stack[-1], self.field_name.lower(), s)

        del self.field_name 

if __name__ == "__main__":
    p = KiCadExportParser("KiCadExportParser_test.xml")
    print(p.components)

    #import doctest
    #doctest.testmod()

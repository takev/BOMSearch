
import Part

class Parts (object):
    def __init__(self):
        self.parts_by_mfp = {}
        self.parts_by_ref = {}

    def __repr__(self):
        s = "<Parts\n"

        for part in self.parts_by_mfp.values():
            s += " %s\n" % repr(part)
        s+= ">"

        return s

    def addComponent(self, component):
        mfp = component.mfp()

        part = self.parts_by_mfp.setdefault(mfp, Part.Part(mfp))
        part.addToCount(component.count)

        self.parts_by_ref[component.ref] = part
        part.addRef(component.ref)

    def allMFPs(self):
        mfps = set()
        for mfp_key in self.parts_by_mfp.keys():
            for mfp in mfp_key:
                mfps.add(mfp)

        return mfps


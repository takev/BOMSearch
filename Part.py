

class Part (object):
    def __init__(self, mfp):
        self.mfp = mfp
        self.count = 0
        self.refs = set()

    def __repr__(self):
        return "<Part mfp=%s count=%i refs=%s>" % (repr(self.mfp), self.count, repr(self.refs))

    def addToCount(self, count):
        self.count += count

    def addRef(self, ref):
        if ref:
            self.refs.add(ref)



class Component (object):
    def __init__(self, ref, count=1):
        self.ref = ref
        self.count = count
        self.value = None
        self.datasheet = None

    def __repr__(self):
        s = "<Component ref=%s count=%i value=%s MFP=%s>" % (self.ref, self.count, repr(self.value), self.mfp())
        return s

    def mfp(self):
        mfp_list = []

        for key in self.__dict__.keys():
            if key.startswith("mfp"):
                value = getattr(self, key)
                if value:
                    mfp_list.append(value)

        mfp_list.sort()
        return tuple(mfp_list)


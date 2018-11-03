
class PartQuery (object):
    def __init__(self, brand_name, part_number):
        self.brand_name = brand_name
        self.part_number = part_number

    def __repr__(self):
        return "'%s':'%s'" % (self.brand_name, self.part_number)

    def __hash__(self):
        return hash(self.brand_name) ^ hash(self.part_number)

    def __eq__(self, other):
        return self.brand_name == other.brand_name and self.part_number == other.part_number

    def __lt__(self, other):
        if self.brand_name == other.brand_name:
            return self.part_number < other.part_number

        return self.brand_name < other.brand_name

    def octopartQuery(self):
        return {"brand": self.brand_name, "mpn": self.part_number}

    def manualQuery(self):
        return "%s:%s" % (self.brand_name, self.part_number)

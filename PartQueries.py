
class PartQueries (object):
    def __init__(self):
        self.queries = set()

    def __repr__(self):
        queries = list(self.queries)
        queries.sort()

        s = "{"
        s += ", ".join([repr(x) for x in queries])
        s += "}"
        return s

    def __len__(self):
        return len(self.queries)

    def __iter__(self):
        return iter(self.queries)

    def __hash__(self):
        h = 0
        for query in self.queries:
            h ^= hash(query)

        return h

    def __eq__(self, other):
        return self.queries == other.queries and not isinstance(other, NoPart)

    def add(self, query):
        self.queries.add(query)

class NoPart (PartQueries):
    def __hash__(self):
        return PartQueries.__hash__(self)

    def __eq__(self, other):
        return isinstance(other, NoPart)


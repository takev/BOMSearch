
import pickle
import json
import urllib
import sys
import time

class Octopart (object):
    def __init__(self, api_key):
        self.api_key = api_key
        try:
            fd = open(".octopart_cache.pickle", "rb")
            self.cache = pickle.load(fd)
            fd.close()
        except FileNotFoundError:
            print("Could not open octopart cache.", file=sys.stderr)
            self.cache = {}

    def __getitem__(self, key):
        return self.cache[key]

    def save(self):
        fd = open(".octopart_cache.pickle", "wb")
        pickle.dump(self.cache, fd)
        fd.close()

    def populate(self, keys):
        """Populate cache with information about keys.
        """
        keys = list(keys)
        keys.sort()

        for key in keys:
            if key not in self.cache:
                print("Quering octopart for %s." % repr(key), file=sys.stderr)
                queries = json.dumps([{"mpn": key}])

                url = 'http://octopart.com/api/v3/parts/match?queries=%s&apikey=%s' % (
                    urllib.parse.quote_plus(queries, safe="{}:,\""),
                    self.api_key
                )
                context = urllib.request.urlopen(url)
            
                code = context.getcode()
                if code != 200:
                    raise RuntimeError("Unexpected HTTP code %i" % code)

                text = context.read().decode("utf-8")
                objects = json.loads(text)
                self.cache[key] = objects

                self.save()
                time.sleep(1)



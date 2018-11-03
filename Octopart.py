
import pickle
import json
import urllib
import sys
import time
import decimal

import Offer

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

    def findOffers(self, queries, filter):
        offers = []
        for query in queries:
            self.populate(query)
            if query not in self.cache:
                raise KeyError(query)

            for item in self.cache[query]:
                for offer in item["offers"]:
                    for currency, price_breaks in offer["prices"].items():
                        for (quantity, price) in price_breaks:
                            currency_conversion=filter.currencies.get(currency, None)
                            is_authorized=offer["is_authorized"]
                            vendor = offer["seller"]["name"]
                            vendor_penalty = filter.vendors.get(vendor, filter.unknown_vendor_penalty)
                            in_stock_quantity = offer["in_stock_quantity"]
                            minimum = 1 if not offer["moq"] else offer["moq"]
                            multiple = 1 if not offer["order_multiple"] else offer["order_multiple"]

                            offer_obj = Offer.Offer(
                                brand=item["brand"]["name"],
                                manufacturer=item["manufacturer"]["name"],
                                mpn=item["mpn"],
                                vendor=vendor,
                                vendor_penalty=vendor_penalty,
                                sku=offer["sku"],
                                is_authorized=is_authorized,
                                in_stock_quantity=in_stock_quantity,
                                currency=currency,
                                currency_conversion=currency_conversion,
                                price=decimal.Decimal(price),
                                quantity=quantity,
                                minimum=minimum,
                                multiple=multiple
                            )

                            # Filter out price-breaks, offers or parts which we don't want.
                            if currency not in filter.currencies:
                                continue

                            if filter.must_be_authorized and not is_authorized:
                                continue

                            offers.append(offer_obj)

        return offers

    def save(self):
        fd = open(".octopart_cache.pickle", "wb")
        pickle.dump(self.cache, fd)
        fd.close()

    def populate(self, query):
        """Populate cache with information about keys.
        """
        if query not in self.cache:
            print("Quering octopart for %s." % repr(query), end=" ", flush=True, file=sys.stderr)
            queries = json.dumps([query.octopartQuery()])

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

            first_result = objects["results"][0]
            if "error" in first_result and first_result["error"] != None:
                print("Error '%s'." % first_result["error"], file=sys.stderr)

            elif not first_result["items"]:
                print("Not Found.", file=sys.stderr)
                self.cache[query] = []

            else:
                print("Found.", file=sys.stderr)
                self.cache[query] = first_result["items"]

            self.save()
            time.sleep(1)

        else:
            if self.cache[query]:
                #print("Cached octopart for %s. Found." % repr(query), flush=True, file=sys.stderr)
                pass
            else:
                print("Cached octopart for %s. Not Found." % repr(query), flush=True, file=sys.stderr)


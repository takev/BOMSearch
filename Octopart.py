
import pickle
import json
import urllib
import sys
import time

import Part
import PartOffer
import PriceBreak

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

    def findOffers(self, query, filter):
        self.populate(query)
        if query not in self.cache:
            raise KeyError(query)

        parts = []
        for item in self.cache[query]:
            part = Part.Part()
            part.brand = item["brand"]["name"]
            part.manufacturer = item["manufacturer"]["name"]
            part.manufacturer_part_number = item["mpn"]
            for offer in item["offers"]:
                part_offer = PartOffer.PartOffer()
                part_offer.seller = offer["seller"]["name"]
                part_offer.stock_keeping_unit = offer["sku"]
                part_offer.is_authorized = offer["is_authorized"]
                part_offer.in_stock_quantity = offer["in_stock_quantity"]

                minimum = 1 if not offer["moq"] else offer["moq"]
                multiple = 1 if not offer["order_multiple"] else offer["order_multiple"]
                for currency, price_breaks in offer["prices"].items():
                    for (quantity, price) in price_breaks:
                        # Filter out price-breaks, offers or parts which we don't want.
                        if currency not in filter.currencies:
                            continue

                        if filter.must_be_authorized and not part_offer.is_authorized:
                            continue

                        if part_offer.in_stock_quantity == 0:
                            continue

                        part_offer.add(PriceBreak.PriceBreak(
                            currency=currency,
                            currency_conversion=filter.currencies[currency],
                            price=price,
                            quantity=quantity,
                            minimum=minimum,
                            multiple=multiple
                        ))

                if part_offer.hasPriceBreaks():
                    part.add(part_offer)
           
            if part.hasOffers():
                parts.append(part)

        return parts

    def save(self):
        fd = open(".octopart_cache.pickle", "wb")
        pickle.dump(self.cache, fd)
        fd.close()

    def populate(self, query):
        """Populate cache with information about keys.
        """
        if query not in self.cache:
            print("Quering octopart for %s." % repr(query), end=" ", flush=True, file=sys.stderr)
            queries = json.dumps([query.OctopartQuery()])

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
            print("Cached octopart for %s." % repr(query), end=" ", flush=True, file=sys.stderr)
            if self.cache[query]:
                print("Found.", file=sys.stderr)
            else:
                print("Not Found.", file=sys.stderr)


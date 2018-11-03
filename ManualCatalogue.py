
import sys
import json
import Offer
import decimal

class ManualCatalogue (object):
    def __init__(self, filename):
        self.parts = json.load(open(filename, "r"))


    def findOffers(self, queries, filter):
        offers = []
        for query in queries:
            if query.manualQuery() not in self.parts:
                continue

            print("Found manual part for %s" % query, file=sys.stderr)

            for item in self.parts[query.manualQuery()]:
                for offer in item["offers"]:
                    for currency, price_breaks in offer["prices"].items():
                        for (quantity, price) in price_breaks:
                            currency_conversion=filter.currencies.get(currency, None)
                            is_authorized=offer["is_authorized"]
                            vendor = offer["vendor"]
                            vendor_penalty = filter.vendors.get(vendor, filter.unknown_vendor_penalty)
                            in_stock_quantity = offer["in_stock_quantity"]
                            minimum = 1 if not offer["moq"] else offer["moq"]
                            multiple = 1 if not offer["order_multiple"] else offer["order_multiple"]

                            offer_obj = Offer.Offer(
                                brand=item["brand"],
                                manufacturer=item["manufacturer"],
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


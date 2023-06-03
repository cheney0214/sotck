class Tests:
    def __init__(self, thdmalist, ofdmalist, fdmalist, prices):
        self.thdmalist = thdmalist
        self.ofdmalist = ofdmalist
        self.fdmalist = fdmalist
        self.prices = prices

        # The below get the latest numbers
        self.thd = self.thdmalist[len(self.thdmalist) - 1]
        self.ofd = self.ofdmalist[len(self.ofdmalist) - 1]
        self.fd = self.fdmalist[len(self.fdmalist) - 1]
        self.latestPrice = prices[len(prices) - 1]
        self.last52wksprices = prices[len(prices) - 253:len(prices)]
        self.fiftytwowkhigh = max(self.last52wksprices)
        self.fiftytwowklow = min(self.last52wksprices)

    def MAComparisonTest(self):
        result = False
        if self.thd < self.ofd < self.fd:
            result = True
        return result

    def PriceToMAComparisonTest(self):
        result = False
        if self.latestPrice > self.thd and self.latestPrice > self.ofd and self.latestPrice > self.fd:
            result = True
        return result

    def PriceToHighLowComparisonTest(self):
        result = False;
        lowTarget = 1.3 * self.fiftytwowklow;
        highTarget = .75 * self.fiftytwowkhigh;
        if self.latestPrice >= lowTarget and self.latestPrice >= highTarget:
            result = True;
        return result;

    def THDMATrendingUpTest(self, numMonths: int):
        limit = 21 * numMonths;
        testthdmalist = self.thdmalist[len(self.thdmalist) - limit: len(self.thdmalist)]
        result = True
        previous = -1
        for i in testthdmalist:
            if i <= previous:
                return False
            previous = i
        return result

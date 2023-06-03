from fixedlist import FixedList
import statistics as st
from Tests import Tests


class TrendTemplateTest:
    def __init__(self, symbol, prices, strength=None):
        self.symbol = symbol
        self.prices = prices
        self.strength = strength if strength is not None else 1
        self.result = False
        self.mact = None
        self.ptmact = None
        self.pthlct = None
        self.thdmatut = None

    def runTest(self):
        twohundredday = FixedList(200)
        onefiftyday = FixedList(150)
        fiftyday = FixedList(50)
        thdmalist = []
        ofdmalist = []
        fdmalist = []
        count = 0

        for i in self.prices:
            current = round(i, 2)
            twohundredday.append(current)
            onefiftyday.append(current)
            fiftyday.append(current)
            if count >= 50:
                fdmalist.append(round(st.mean(fiftyday), 2))
            if count >= 150:
                ofdmalist.append(round(st.mean(onefiftyday), 2))
            if count >= 200:
                thdmalist.append(round(st.mean(twohundredday), 2))
            count += 1

        if len(thdmalist) == 0:
            return False

        T = Tests(thdmalist, ofdmalist, fdmalist, self.prices)
        self.mact = T.MAComparisonTest()
        self.ptmact = T.PriceToMAComparisonTest()
        self.pthlct = T.PriceToHighLowComparisonTest()
        self.thdmatut = T.THDMATrendingUpTest(self.strength)

        if self.mact and self.ptmact and self.pthlct and self.thdmatut:
            self.result = True

        return self.result

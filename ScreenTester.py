from trendtemplatetest import TrendTemplateTest


def analyse_data(symbol, prices):
    t = TrendTemplateTest(symbol, prices)
    return t.runTest()


def write_results(symbol, name):
    r = open("./files/stock-passed.txt", "a")
    r.write(str(symbol) + "\t" + str(name) + "\n")
    r.close()

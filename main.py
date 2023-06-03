from multiprocessing import Pool
import os
import akshare as ak
import arrow
from ScreenTester import analyse_data
from ScreenTester import write_results


def init_stock_lists():
    code_name_df = ak.stock_info_a_code_name()
    lists = code_name_df.values

    filename = "./files/stock-lists.txt"
    with open(filename, "w") as f:
        for element in lists:
            symbol = element[0] + '\t' + element[1] + '\n'
            f.write(symbol)
        f.close()

    filename = "./files/stock-passed.txt"
    if os.path.exists(filename):
        os.remove(filename)


def analyse_stock_datas(pools):
    with open("./files/stock-lists.txt", "r") as f:
        for element in enumerate(f):
            index = element[0]
            code_name = element[1].strip().split('\t')
            symbol = code_name[0]
            name = code_name[1]

            try:
                pools.apply_async(analyse_stock_data, args=(index, symbol, name))
            except Exception as e:
                print(f" analyse stock error, code:{symbol} \t name:{name}, \t exception: {e}")
                continue


def analyse_stock_data(index, symbol, name):
    print(f"analyse stock data, current: {index} \t symbol: {symbol} \t name: {name}")

    today = arrow.now()
    yesterday = today.shift(days=-1).format('YYYYMMDD')
    two_year_day = today.shift(years=-3).format('YYYYMMDD')

    try:
        daily_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=two_year_day, end_date=yesterday,
                                           adjust="qfq")
        prices = daily_hist_df.get('收盘').values
        size = prices.size
        if prices.size < 400:
            return

        if (prices[size-1]-prices[size-51])/prices[size-51] > 0.35:
            return

        prices = prices[size - 400: size + 1]
        resp = analyse_data(symbol, prices)
        if resp:
            write_results(symbol, name)
    except Exception as e:
        print(f" analyse stock error, code:{symbol} \t name:{name}, \t exception: {e}")


def filter_stock():
    df = ak.stock_comment_em()

    filename = "./files/stock-passed.txt"
    with open(filename, "r") as f:
        print(f"code   \t {'name'.center(6)} \t  得分 \t 参与度 \t 排名 \t 换手率 \t 市盈率 \t 最新价")

        for element in f:
            code_name = element.strip().split('\t')
            symbol = code_name[0]
            name = code_name[1]

            # 绝对低量：小于1 %
            # 成交低靡：1 %——2 %
            # 成交温和：2 %——3 %
            # 成交活跃：3 %——5 % 相对活跃状态
            # 带量：5 %——8 %
            # 放量：8 %——15 % 高度活跃状态
            symbol_df = df.loc[df['代码'] == symbol, ['综合得分', '机构参与度', '目前排名', '换手率', '市盈率', '最新价']]
            if symbol_df.size >= 4:
                values = symbol_df.values[0]
                if values[0] > 60 and values[1] > 0.3 and 5 < values[3] < 15:
                    print(f"{symbol} \t {name.ljust(4)} \t {round(values[0],2)} \t {round(values[1],1)} \t \
{round(values[2],2)} \t {values[3]} \t \
{round(values[4],1)} \t {values[5]} ")


if __name__ == '__main__':
    init_stock_lists()
    pool = Pool(15)
    analyse_stock_datas(pool)
    pool.close()
    pool.join()
    filter_stock()

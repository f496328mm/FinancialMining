import os

import pandas as pd

from FinMind.data import DataLoader
from FinMind.data import FinMindApi

user_id = os.environ['FINMIND_USER']
password = os.environ['FINMIND_PASSWORD']


def test_api_login():
    api = FinMindApi()
    api.login_by_account(user_id, password)
    assert api._api_token is not None


def test_adj_price():
    stock_id = "2330"
    start_date = "2019-04-01"
    end_date = "2021-03-06"
    data_loader = DataLoader()
    data_loader.login_by_account(user_id, password)
    data = data_loader.stock_adj_price(stock_id=stock_id, start_date=start_date, end_date=end_date).iloc[0][
        ['open', 'close', 'max', 'min']]

    assert all(data == pd.Series({"open": 231.35, "close": 228.11, "max": 231.35, "min": 228.11}))


def test_api_data():
    dataset = "TaiwanStockPrice"
    stock_id = "2330"
    date = "2020-03-10"
    end_date = "2020-03-15"
    api = FinMindApi()
    api.login_by_account(user_id, password)
    api.api_version = "v3"
    data = api.get_data(
        dataset=dataset,
        stock_id=stock_id,
        date=date,
        end_date=end_date,
    )
    assert all(
        data
        == pd.DataFrame(
            {
                "date": [
                    "2020-03-10",
                    "2020-03-11",
                    "2020-03-12",
                    "2020-03-13",
                ],
                "stock_id": ["2330", "2330", "2330", "2330"],
                "Trading_Volume": [74869130, 64923710, 114173351, 151268148],
                "Trading_money": [
                    22727941511,
                    19913151529,
                    33544278206,
                    42448997546,
                ],
                "open": [301.5, 309.0, 299.0, 275.0],
                "max": [309.0, 310.5, 299.0, 294.0],
                "min": [301.0, 302.0, 287.0, 272.5],
                "close": [307.0, 302.0, 294.0, 290.0],
                "spread": [1.5, -5.0, -8.0, -4.0],
                "Trading_turnover": [30268, 27176, 56989, 71990],
            }
        )
    )


def test_get_datalist():
    dataset = "TaiwanExchangeRate"
    api = FinMindApi()
    api.login_by_account(user_id, password)
    api.api_version = "v3"
    data = api.get_datalist(dataset)
    assert data == [
        "AUD",
        "CAD",
        "CHF",
        "CNY",
        "EUR",
        "GBP",
        "HKD",
        "IDR",
        "JPY",
        "KRW",
        "MYR",
        "NZD",
        "PHP",
        "SEK",
        "SGD",
        "THB",
        "USD",
        "VND",
        "ZAR",
    ]


def test_translation():
    dataset = "Shareholding"
    api = FinMindApi()
    api.login_by_account(user_id, password)
    api.api_version = "v3"
    data = api.translation(dataset=dataset)
    assert all(
        data
        == pd.DataFrame(
            {
                "name": [
                    "外資及陸資共用法令投資上限比率",
                    "外資尚可投資股數",
                    "全體外資持有股數",
                    "法令投資上限比率",
                    "與前日異動原因(註)",
                    "發行股數",
                    "最近一次上櫃公司申報外資持股異動日期",
                    "證券代號",
                    "證券名稱",
                ],
                "english": [
                    "ChineseInvestmentUpperLimitRatio",
                    "ForeignInvestmentRemainingShares",
                    "ForeignInvestmentShares",
                    "ForeignInvestmentUpperLimitRatio",
                    "note",
                    "NumberOfSharesIssued",
                    "RecentlyDeclareDate",
                    "stock_id",
                    "stock_name",
                ],
            }
        )
    )
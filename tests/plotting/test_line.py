import pytest
import os

from FinMind import plotting
from FinMind.data import DataLoader
from FinMind.schema import LinePlotSchema

testdata_line = [
    ("1220", "2015-1M", "2020-1M"),
    ("2330", "2018-01-01", "2021-03-03"),
]


@pytest.mark.parametrize("stock_id, start_date, end_date", testdata_line)
def test_line(stock_id, start_date, end_date):
    user_id = os.environ.get("FINMIND_USER", "")
    password = os.environ.get("FINMIND_PASSWORD", "")
    data_loader = DataLoader()
    data_loader.login(user_id, password)
    df = data_loader.taiwan_stock_month_revenue(
        stock_id=stock_id, start_date=start_date, end_date=end_date
    )
    df["labels"] = (
        df[["revenue_year", "revenue_month"]]
        .astype(str)
        .agg(lambda date: f"{date[0]}-{date[1]}M", axis=1)
    )
    df["series"] = df["revenue"].agg(lambda value: round(value / 1e8, 2))
    line_plot_data = LinePlotSchema.df_convert(df)
    assert plotting.line(line_plot_data)

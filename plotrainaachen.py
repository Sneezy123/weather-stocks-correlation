import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
import sys

stock_name = sys.argv[1]
quotes = yf.Search(stock_name, max_results=10).quotes

quote = quotes[0]["symbol"]
if len(quotes) > 1:
    for idx, quote in enumerate(quotes):
        longname = "N/A"
        try:
            longname = quote["longname"]
        except KeyError:
            pass

        print(f"{idx + 1}) {quote['symbol']} ({longname})")

    inp = -1
    while True:
        try:
            inp = int(input("> "))
            break
        except Exception:
            continue
    quote = quotes[inp - 1]["symbol"]

file = pd.read_csv(
    "weatherdata.csv",
    sep=";",
    header=0,
    names=[
        "station_id",
        "measurement_datetime",
        "quality",
        "precipitation_height",
        "is_precipitation",
        "precipitation_form",
        "eor",
    ],
)

file["measurement_datetime"] = pd.to_datetime(
    file["measurement_datetime"], format="%Y%m%d%H"
)

file["measurement_datetime"] = file["measurement_datetime"].astype("datetime64[ns]")
file = file.sort_values("measurement_datetime")

start_str = file["measurement_datetime"].min() - pd.Timedelta(days=5)
start_str = start_str.strftime("%Y-%m-%d")
end_str = file["measurement_datetime"].max() + pd.Timedelta(days=1)
end_str = end_str.strftime("%Y-%m-%d")

ticker = yf.Ticker(quote)
stocks = ticker.history(start=start_str, end=end_str)
stocks = stocks.reset_index()

stocks["Date"] = stocks["Date"].dt.tz_localize(None).astype("datetime64[ns]")
stocks = stocks.sort_values("Date")

file = pd.merge_asof(
    file,
    stocks[["Date", "Close"]],
    left_on="measurement_datetime",
    right_on="Date",
    direction="backward",
)

# file["Close"] = file["Close"].ffill()
file = file.drop(columns=["Date"])


idx = file.index.to_list()
idx = file["measurement_datetime"].to_list()


pctD = file["precipitation_height"].diff()
pm = pctD.min()
pM = pctD.max()
pct = (pctD - pm) / (pM - pm)

summ = file["precipitation_height"].sum()
cumulative_normalized = file["precipitation_height"].cumsum().div(summ)

max = file["precipitation_height"].max()
height_normalized = file["precipitation_height"].div(max)

maxS = file["Close"].max()
minS = file["Close"].min()
stocks_close_normalized = file["Close"].subtract(minS).div(maxS - minS)

fig, (ax1, ax2) = plt.subplots(2)

fig.suptitle(
    f"Aachener Niederschlag im Vergleich zu {ticker.info['shortName']} ({quote})"
)
ax1.plot(idx, cumulative_normalized.to_list(), "r-")
ax1.plot(idx, stocks_close_normalized.to_list(), "b-")

ax2.plot(idx, height_normalized.to_list())
ax2.plot(idx, pct.to_list(), alpha=0.3)

for ax in fig.axes:
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m.%Y"))

fig.set_layout_engine("tight")
plt.show()
